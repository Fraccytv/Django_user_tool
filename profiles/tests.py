from django.test import TestCase
from accounts.models import CustomUser
from profiles.models import Profile

class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        # Opret bruger
        user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            encrypted_password="fake"
        )
        print("Created test user:", user)

        # Opret profil
        profile = Profile.objects.create(
            user=user,
            bio="Just a test bio",
            location="Testland"
        )
        print("Created profile:", profile)

        # Tjek at profilen er tilknyttet brugeren
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.bio, "Just a test bio")
        self.assertEqual(profile.location, "Testland")

        print("All assertions passed! ✅")
