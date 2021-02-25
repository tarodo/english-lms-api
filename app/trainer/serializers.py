from rest_framework import serializers

from core.models import Student, Word, WordSet


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
        fields = ('id', 'word', 'translate', 'definition',
                  'example', 'student')
        read_only = ('id',)


class WordSetSerializer(serializers.ModelSerializer):
    """Serializer a word set"""
    words = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Word.objects.all()
    )

    class Meta:
        model = WordSet
        fields = ('id', 'name', 'student', 'words')
        read_only = ('id', )
