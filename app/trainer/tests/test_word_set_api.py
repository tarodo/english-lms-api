from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import WordSet, Student, Word

from trainer.serializers import WordSetSerializer, WordSetDetailSerializer


WORD_SET_URL = reverse('trainer:wordset-list')


def detail_url(word_set_id):
    """Retunr word set detail URL"""
    return reverse('trainer:wordset-detail', args=[word_set_id])


def sample_word(student, word='voyage'):
    """Create and return a sample word"""
    return Word.objects.create(student=student, word=word)


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

    def test_view_word_set_detail(self):
        """Test viewing a word set detail"""
        word_set = sample_word_set(student=self.student)
        word_set.words.add(sample_word(student=self.student))

        url = detail_url(word_set.id)
        res = self.client.get(url)

        serializer = WordSetDetailSerializer(word_set)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_word_set(self):
        """Test creating word set"""
        payload = {
            'name': 'My journey',
            'student': self.student.id
        }
        res = self.client.post(WORD_SET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # word_set = WordSet.objects.get(id=res.data['id'])
        # for key in payload.keys():
        #     self.assertEqual(payload[key], getattr(word_set, key))

    def test_create_word_set_with_words(self):
        """Test creating a word set with words"""
        word1 = sample_word(student=self.student, word='voyage')
        word2 = sample_word(student=self.student, word='trip')
        payload = {
            'name': 'voyage',
            'student': self.student.id,
            'words': [word1.id, word2.id]
        }
        res = self.client.post(WORD_SET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        word_set = WordSet.objects.get(id=res.data['id'])
        words = word_set.words.all()
        self.assertEqual(words.count(), 2)
        self.assertIn(word1, words)
        self.assertIn(word2, words)
