from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@ya.ru', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_username_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'bot1@yaya.ru'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test creating with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            '123123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_student_str(self):
        """Test the student representation"""
        student = models.Student.objects.create(
            user=sample_user(),
            tg_id='123123123'
        )

        self.assertEqual(str(student), student.tg_id)

    def test_word_str(self):
        """Test the word representation"""
        student = models.Student.objects.create(
            user=sample_user(),
            tg_id='123123123'
        )
        word = models.Word.objects.create(
            word='test',
            student=student
        )

        self.assertEqual(str(word), word.word)

    def test_word_set_str(self):
        """Test the set string representation"""
        student = models.Student.objects.create(
            user=sample_user(),
            tg_id='123123123'
        )
        word_set = models.WordSet.objects.create(
            name='First set',
            student=student
        )

        self.assertEqual(str(word_set), word_set.name)
