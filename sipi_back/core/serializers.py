import random
import string

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Subject, Queue
from users.models import User

PASSWORD_LENGTH = 12

QUEUE_ERROR_MESSAGE = "You are already in queue on this subject"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug')
        model = Subject
        read_only_fields = ('slug',)


class UsersCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'personal_cipher', 'role', 'password'
        ]
        read_only_fields = ('password',)

    def create(self, validated_data):
        password = ''.join(
            random.choices(string.ascii_letters + string.digits,
                           k=PASSWORD_LENGTH))
        validated_data['password'] = make_password(password)
        user = super().create(validated_data)
        user.password = password
        return user


class UsersSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()

    @staticmethod
    def get_user_fullname(obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = ('username', 'personal_cipher', 'role', 'user_fullname')


class QueueSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_fullname = serializers.SerializerMethodField()
    subject = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field='slug',
        queryset=Subject.objects.all())
    subject_name = serializers.CharField(
        source='subject.title', read_only=True)

    @staticmethod
    def get_user_fullname(obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    class Meta:
        model = Queue
        fields = ('user', 'subject', 'timestamp', 'subject_name', 'user_fullname')
        read_only_fields = ('user', 'timestamp', 'subject', 'subject_name', 'user_fullname')
        validators = [
            UniqueTogetherValidator(
                queryset=Queue.objects.all(),
                fields=['user', 'subject'],
                message=QUEUE_ERROR_MESSAGE
            )
        ]
