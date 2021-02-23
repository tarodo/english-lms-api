from rest_framework import serializers

from core.models import Student, Word


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for student objects"""

    class Meta:
        model = Student
        fields = ('id', 'tg_id', 'first_name', 'last_name',
                  'username', 'is_student', 'is_teacher')
        read_only_fields = ('id', )


class WordSerializer(serializers.ModelSerializer):
    """Serializer for word objects"""

    class Meta:
        model = Word
        fields = ('id', 'word', 'student')
        read_only = ('id',)
