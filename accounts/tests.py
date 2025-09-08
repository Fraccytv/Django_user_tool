from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from accounts.models import CustomUser, LoginAttempt
from accounts.helpers import get_safe_next_url
from accounts.services import (
    generate_salt, hash_password,  # hvis du registrerer via POST kan du undvære disse
    FAIL_LIMIT,
)
# Brug client til end-to-end (views) og RequestFactory til helperen.


class UserFlowTestCase(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def _create_user(self, username="testuser", email="test@example.com", pw="securepass123"):
        # Du kan også oprette via POST til register-view; her gør vi det direkte for hastighed
        salt = generate_salt()
        user = CustomUser.objects.create(
            username=username.lower(),
            email=email.lower(),
            salt=salt,
            encrypted_password=hash_password(pw, salt),
        )
        # sikre én række til lockout (hvis din service ikke gør get_or_create selv)
        # LoginAttempt.objects.get_or_create(
        #     user=user,
        #     defaults={"failed_attempts": 0, "last_attempt": timezone.now()}
        # )
        return user

    def test_register_login_logout_flow(self):
        # Registrér via view for at teste formularen end-to-end
        register_data = {
            "username": "formuser",
            "email": "form@example.com",
            "password": "FormPass123",
            "confirm_password": "FormPass123",
        }
        resp = self.client.post(reverse("register"), register_data)
        self.assertEqual(resp.status_code, 302)  # redirect to login
        self.assertTrue(CustomUser.objects.filter(username="formuser").exists())

        # Login
        login_data = {"username": "formuser", "password": "FormPass123"}
        resp = self.client.post(reverse("login"), login_data)
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(self.client.session.get("user_id"))

        # Logout
        resp = self.client.post(reverse("logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertIsNone(self.client.session.get("user_id"))

    def test_get_safe_next_url_cases(self):
        # 1) Ren intern sti
        req = self.rf.get("/login/", {"next": "/profile/"})
        self.assertEqual(get_safe_next_url(req), "/profile/")

        # 2) Protokol-relativ ekstern -> fallback til 'home'
        req = self.rf.get("/login/", {"next": "//evil.com/phish"})
        self.assertEqual(get_safe_next_url(req), reverse("home"))

        # 3) HTTPS request: http absolut på samme host må ikke accepteres -> fallback
        req_https = self.rf.get("/login/", {"next": "http://testserver/admin/"}, secure=True)
        self.assertEqual(get_safe_next_url(req_https), reverse("home"))

    def test_session_login_required_redirects_with_next(self):
        # Uden session -> adgang til 'home' skal redirecte til login med ?next=
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp.url)
        self.assertIn("next=", resp.url)

    def test_lockout_after_limit_and_reset_on_success(self):
        user = self._create_user()
        login_url = reverse("login")

        # Trigger fejl FAIL_LIMIT gange inden for vinduet
        for _ in range(FAIL_LIMIT):
            resp = self.client.post(login_url, {"username": user.username, "password": "WRONG"})
            # Bliv på siden med form-fejl (200) eller redirect tilbage til login (302) afhænger af din template/logik
            self.assertIn(resp.status_code, (200, 302))

        # Brugeren bør være låst nu
        la = LoginAttempt.objects.get(user=user)
        self.assertIsNotNone(la.locked_until)
        self.assertGreater(la.locked_until, timezone.now())

        # Forsøg med korrekt password under lockout -> stadig afvist
        resp = self.client.post(login_url, {"username": user.username, "password": "securepass123"})
        self.assertIn(resp.status_code, (200, 302))
        la.refresh_from_db()
        # Stadig låst
        self.assertIsNotNone(la.locked_until)

        # Udløb lockout manuelt og log ind igen korrekt -> nulstil tæller
        la.locked_until = timezone.now() - timedelta(minutes=1)
        la.save(update_fields=["locked_until"])

        resp = self.client.post(login_url, {"username": user.username, "password": "securepass123"})
        self.assertEqual(resp.status_code, 302)
        la.refresh_from_db()
        self.assertEqual(la.failed_attempts, 0)
        self.assertIsNone(la.locked_until)

    def test_failed_attempts_counter_starts_over_after_window(self):
        user = self._create_user()
        login_url = reverse("login")

        # 1. fejl
        self.client.post(login_url, {"username": user.username, "password": "WRONG"})
        la = LoginAttempt.objects.get(user=user)
        self.assertEqual(la.failed_attempts, 1)

        # Simulér at vinduet udløber
        la.last_attempt = timezone.now() - timedelta(minutes=60)
        la.save(update_fields=["last_attempt"])

        # Ny fejl efter udløb -> tæller starter forfra fra 1
        self.client.post(login_url, {"username": user.username, "password": "WRONG_AGAIN"})
        la.refresh_from_db()
        self.assertEqual(la.failed_attempts, 1)
