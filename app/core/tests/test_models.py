from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_tgid_successful(self):
        """Test creating a new user with an Telegram ID is successful"""
        tg_id = '112233'
        user = get_user_model().objects.create_user(
            tg_id=tg_id
        )

        self.assertEqual(user.tg_id, tg_id)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            '123123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
