from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Student, Word, WordSet

from trainer import serializers


class StudentViewSet(viewsets.ModelViewSet):
    """Manage students in the database"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def perform_create(self, serializer):
        """Create a new student"""
        serializer.save(user=self.request.user)


class WordViewSet(viewsets.ModelViewSet):
    """Manage words in the database"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Word.objects.all()
    serializer_class = serializers.WordSerializer

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return the words for the student"""
        student = self.request.query_params.get('student')
        queryset = self.queryset
        if student:
            student_id = int(student)
            queryset = queryset.filter(student__id=student_id)

        return queryset

    def perform_create(self, serializer):
        """Create a new word"""
        serializer.save()


class WordSetViewSet(viewsets.ModelViewSet):
    """Manage word sets in the database"""
    serializer_class = serializers.WordSetSerializer
    queryset = WordSet.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Retrieve the word sets for the student"""
        student = self.request.query_params.get('student')
        queryset = self.queryset.order_by('id')
        if student:
            student_id = int(student)
            queryset = queryset.filter(student__id=student_id)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.WordSetDetailSerializer

        return self.serializer_class
