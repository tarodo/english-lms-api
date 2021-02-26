from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Student

from trainer.serializers import StudentSerializer


STUDENTS_URL = reverse('trainer:student-list')


def detail_url(student_id):
    """Retunr word set detail URL"""
    return reverse('trainer:student-detail', args=[student_id])


class PublicStudentsApiTests(TestCase):
    """Test publicly available students API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving students"""
        res = self.client.get(STUDENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentsApiTests(TestCase):
    """Test the authorized user students API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'bottest@ya.ru',
            'test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_students(self):
        """Test retrieving students"""
        Student.objects.create(user=self.user, tg_id='111111')
        Student.objects.create(user=self.user, tg_id='222222')

        res = self.client.get(STUDENTS_URL)

        students = Student.objects.all().order_by('tg_id')
        serializer = StudentSerializer(students, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_students_no_limited_to_user(self):
        """Test that students are returned not for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'bot@ya.ru',
            'test22222'
        )
        Student.objects.create(user=user2, tg_id='33333333')
        Student.objects.create(user=self.user, tg_id='111111')

        res = self.client.get(STUDENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_student_successful(self):
        """Tset creating a new student"""
        payload = {'tg_id': '11111', 'username': 'roman'}
        self.client.post(STUDENTS_URL, payload)

        exists = Student.objects.filter(
            user=self.user,
            tg_id=payload['tg_id']
        ).exists()
        self.assertTrue(exists)

    def test_create_student_invalid(self):
        """Test creating a new student with invalid payload"""
        payload = {'tg_id': ''}
        res = self.client.post(STUDENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_student(self):
        """Test updating student with patch"""
        student = Student.objects.create(user=self.user, tg_id='111111')

        payload = {'is_teacher': True}
        url = detail_url(student.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        student.refresh_from_db()
        self.assertEqual(student.is_teacher, payload['is_teacher'])

    def test_full_update_student(self):
        """Test updating a student with put"""
        student = Student.objects.create(user=self.user, tg_id='111111')
        payload = {
            'tg_id': '111111',
            'first_name': 'ttt',
            'last_name': 'bbb',
            'is_teacher': True
        }
        url = detail_url(student.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        student.refresh_from_db()
        self.assertEqual(student.tg_id, payload['tg_id'])
        self.assertEqual(student.first_name, 'ttt')
        self.assertEqual(student.last_name, payload['last_name'])
        self.assertEqual(student.is_teacher, payload['is_teacher'])
