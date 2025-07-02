from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from logs.models import Log

class LogModelTestCase(TestCase):
    def test_log_creation(self):
        # Opret en testbruger
        user = User.objects.create(
            username="tester",
            email="tester@example.com",
            encrypted_password="dummy",
            salt="salt123"
        )
        print("✅ Created test user:", user.username)

        # Opret en log for login-hændelse
        log = Log.objects.create(
            user=user,
            ip_address="127.0.0.1",
            status="success",
            event_type="login"
        )
        print("📝 Created log entry:")
        print(f"  - User: {log.user}")
        print(f"  - IP Address: {log.ip_address}")
        print(f"  - Status: {log.status}")
        print(f"  - Event Type: {log.event_type}")
        print(f"  - Timestamp: {log.timestamp}")

        # Assertion tests (vil fejle hvis noget er forkert)
        self.assertEqual(log.user, user)
        self.assertEqual(log.ip_address,"")
        self.assertEqual(log.status, "success")
        self.assertEqual(log.event_type, "login")
        self.assertTrue((timezone.now() - log.timestamp).total_seconds() < 5)

        print("✅ Log creation test passed.")
