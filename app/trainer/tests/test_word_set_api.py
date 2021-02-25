from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import WordSet, Student

from trainer.serializers import WordSetSerializer


WORD_SET_URL = reverse('trainer:wordset-list')


def sample_word_set(student, **params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'test',
        'student': student
    }
    defaults.update(params)

    return WordSet.objects.create(**defaults)


class PublicWordSetApiTest(TestCase):
    """Test unauthenticated word set API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(WORD_SET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWordSetApiTest(TestCase):
    """Test authenticated word set API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'bottest@ya.ru',
            'test123'
        )
        self.client.force_authenticate(self.user)
        self.student = Student.objects.create(
            user=self.user,
            tg_id='123123123'
        )

    def test_retrieve_word_sets(self):
        """Test retrieving a list of word sets"""
        sample_word_set(student=self.student)
        sample_word_set(student=self.student)

        res = self.client.get(WORD_SET_URL)

        word_sets = WordSet.objects.all().order_by('id')
        serializer = WordSetSerializer(word_sets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_word_sets_limited_to_student(self):
        """Test retrieving word sets for student"""
        student2 = Student.objects.create(
            user=self.user,
            tg_id='11111'
        )
        sample_word_set(student=student2)
        sample_word_set(student=self.student)

        res = self.client.get(WORD_SET_URL, {'student': self.student.id})

        word_sets = WordSet.objects.filter(student=self.student)
        serializer = WordSetSerializer(word_sets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
