# logs/tests.py
from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser
from .models import Log

class LogModelTestCase(TestCase):
    def test_log_creation(self):
        user = CustomUser.objects.create(
            username="tester",
            email="tester@example.com",
            encrypted_password="dummy",
            salt="salt123",
        )
        log = Log.objects.create(
            user=user,
            ip_address="127.0.0.1",
            status=Log.STATUS_SUCCESS,
            event_type=Log.EVENT_LOGIN,
        )
        self.assertEqual(log.user, user)
        self.assertEqual(log.ip_address, "127.0.0.1")
        self.assertEqual(log.status, Log.STATUS_SUCCESS)
        self.assertEqual(log.event_type, Log.EVENT_LOGIN)
        self.assertTrue((timezone.now() - log.timestamp).total_seconds() < 5)