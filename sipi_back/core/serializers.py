import random
import string

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Subject, Queue
from users.models import User


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title',)
        model = Subject


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
            random.choices(string.ascii_letters + string.digits, k=12))
        validated_data['password'] = make_password(password)
        user = super().create(validated_data)
        user.password = password
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'personal_cipher',
                  'role', 'first_name', 'last_name')


class JoinLeftQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('user_id', 'subject_id', 'timestamp')
        read_only_fields = ('user_id', 'timestamp')
