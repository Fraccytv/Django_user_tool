from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
import pprint

# 🔍 Status code explanations for debugging
STATUS_EXPLANATIONS = {
    200: "✅  OK – Page loaded successfully",
    302: "➡️  Redirect – Usually to login/home",
    400: "❌  Bad Request – Form or input error",
    403: "⛔  Forbidden – Not allowed",
    404: "🔍  Not Found – URL missing",
    500: "💥  Server Error – Something broke",
}

class UserFlowTestCase(TestCase):
    def test_register_login_logout_flow(self):
        # ======== 🧪 REGISTRATION ========
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123",
            "confirm_password": "securepass123",
        }

        print("🔹 Sending registration data:")
        for key, value in register_data.items():
            print(f"{key}: {value}")

        response = self.client.post(reverse("register"), register_data)

        status = response.status_code
        print(f"🔹 Registration status code: {status} → {STATUS_EXPLANATIONS.get(status, 'Unknown')}")
        print("🔹 Registration form errors:")
        pprint.pprint(response.context.get("form").errors if response.context else "No context")

        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())
        user = CustomUser.objects.get(username="testuser")
        print(" User created:", user.username, user.email)

        # ======== 🧪 LOGIN ========
        login_data = {
            "username": "testuser",
            "password": "securepass123",
        }

        print("\n🔹 Sending login data:")
        for key, value in login_data.items():
            print(f"{key}: {value}")

        response = self.client.post(reverse("login"), login_data)

        status = response.status_code
        print(f"🔹 Login status code: {status} →  {STATUS_EXPLANATIONS.get(status, 'Unknown')}")
        print("🔹 Login redirect to home? ", response.url if status == 302 else "Not redirected")

        session_user_id = self.client.session.get("user_id")
        print(" Session user_id:", session_user_id)
        self.assertEqual(session_user_id, user.id)

        # ======== 🧪 LOGOUT ========
        print("\n🔹 Sending logout request")
        response = self.client.post(reverse("logout"))

        status = response.status_code
        print(f"🔹 Logout status code: {status} → {STATUS_EXPLANATIONS.get(status, 'Unknown')}")
        print("🔹 Session after logout:", dict(self.client.session))

        self.assertIsNone(self.client.session.get("user_id"))
        print(" User is logged out properly ✅")
