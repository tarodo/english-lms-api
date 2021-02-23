from rest_framework import serializers

from core.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for student objects"""

    class Meta:
        model = Student
        fields = ('id', 'tg_id', 'first_name', 'last_name',
                  'username', 'is_student', 'is_teacher')
        read_only_fields = ('id', )
