from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Word, Student

from trainer.serializers import WordSerializer


WORD_URL = reverse('trainer:word-list')


class PublicWordsApiTests(TestCase):
    """Test the publicly available words API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(WORD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWordsApiTests(TestCase):
    """Test the private words API"""

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

    def test_retrieve_word_list(self):
        """Test retrieving a list of words"""
        Word.objects.create(student=self.student, word='test')
        Word.objects.create(student=self.student, word='equipment')

        res = self.client.get(WORD_URL)

        words = Word.objects.all().order_by('-word')
        serializer = WordSerializer(words, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_words_limited_to_student(self):
        """Test that only words for the student are returned"""
        student2 = Student.objects.create(
            user=self.user,
            tg_id='11111'
        )
        Word.objects.create(student=student2, word='out1')
        Word.objects.create(student=student2, word='out2')
        word = Word.objects.create(student=self.student, word='in2')

        res = self.client.get(WORD_URL,
                              {'student': self.student.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['word'], word.word)
