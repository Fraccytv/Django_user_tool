from django.test import TestCase
from accounts.models import CustomUser
from profiles.models import Profile


class ProfileModelTest(TestCase):
    def test_profile_is_linked_to_user_and_can_be_updated(self):
        # Opret bruger
        user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            encrypted_password="fake"
        )
        print("✅ Created test user:", user)

        # Hent profilen oprettet af signal
        profile = Profile.objects.get(user=user)

        # Opdater profil
        profile.bio = "Just a test bio"
        profile.location = "Testland"
        profile.save()

        # Bekræft ændringerne
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.bio, "Just a test bio")
        self.assertEqual(profile.location, "Testland")
        print("✅ Profile updated and linked to user correctly.")


class ProfileSignalTestCase(TestCase):
    def test_profile_created_by_signal(self):
        # Create user - signal should auto-create profile
        user = CustomUser.objects.create(
            username="signaluser",
            email="sig@test.com",
            encrypted_password="abc1234"
        )
        print("✅ Created user for signal test:", user)

        # Get profile created by signal
        profile = Profile.objects.get(user=user)

        # Assertions
        self.assertEqual(profile.user.username, "signaluser")
        self.assertIsNone(profile.bio)
        self.assertIsNone(profile.location)
        print("✅ Signal-based profile creation test passed!")
