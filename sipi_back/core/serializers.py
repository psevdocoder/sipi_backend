import random
import string

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from core.models import Subject, Queue, Poll, Choice, Attendance
from users.models import User

PASSWORD_LENGTH = 12

QUEUE_ERROR_MESSAGE = "You are already in queue on this subject"


class SubjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор предметов
    """
    queue_is_open = serializers.BooleanField(source='is_open', read_only=True)

    class Meta:
        fields = ('id', 'title', 'slug', 'queue_is_open')
        model = Subject
        read_only_fields = ('slug', 'queue_is_open')


class UsersCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания пользователя
    """
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
        """
        Создать пользователя
        :param validated_data: данные опроса для создания объекта в базе данных
        :return: объект пользователя
        """
        password = ''.join(
            random.choices(string.ascii_letters + string.digits,
                           k=PASSWORD_LENGTH))
        validated_data['password'] = make_password(password)
        user = super().create(validated_data)
        user.password = password
        return user


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей
    """
    user_fullname = serializers.SerializerMethodField()

    @staticmethod
    def get_user_fullname(obj):
        """
        Получить полное имя пользователя
        :param obj: объект пользователя
        :return: полное имя пользователя
        """
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = ('username', 'personal_cipher', 'role', 'user_fullname')


class QueueSerializer(serializers.ModelSerializer):
    """
    Сериализатор очередей
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.CharField(source='user.username', read_only=True)
    user_fullname = serializers.SerializerMethodField()
    subject = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field='slug',
        queryset=Subject.objects.all())
    subject_name = serializers.CharField(
        source='subject.title', read_only=True)

    @staticmethod
    def get_user_fullname(obj):
        """
        Получить полное имя пользователя
        :param obj: объект пользователя
        :return: полное имя пользователя
        """
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    class Meta:
        model = Queue
        lookup_field = 'slug'
        fields = ('user', 'subject', 'timestamp', 'subject_name',
                  'user_fullname', 'username')
        read_only_fields = (
            'user', 'timestamp', 'subject', 'subject_name', 'user_fullname')
        validators = [
            UniqueTogetherValidator(
                queryset=Queue.objects.all(),
                fields=['user', 'subject'],
                message=QUEUE_ERROR_MESSAGE
            )
        ]


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор выбора в опросе
    """
    class Meta:
        model = Choice
        fields = ('id', 'text', 'votes')


class PollSerializer(serializers.ModelSerializer):
    """
    Сериализатор опросов
    """
    choices = ChoiceSerializer(many=True, read_only=False)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'choices')

    def create(self, validated_data):
        """
        Создать опрос
        :param validated_data: данные опроса для создания объекта в базе данных
        :return: объект опроса
        """
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    """
    Сериализатор голосования
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Choice.objects.all()
    )

    class Meta:
        model = Choice
        fields = ('id',)

    def create(self, validated_data):
        """
        Добавить объект выбора пользователя
        :param validated_data:
        :return: объект выбора
        """
        choice = validated_data.get("id")
        user = self.context.get('request').user
        if choice.voters.filter(id=user.id).exists():
            raise ValidationError("You have already voted for this choice.")
        choice.voters.add(user)
        choice.votes += 1
        choice.save()
        return choice


class AttendanceSerializer(serializers.ModelSerializer):
    """
    Сериализатор посещаемости
    """
    is_present = serializers.BooleanField(read_only=False)
    user_fullname = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SlugRelatedField(many=False,
                                           slug_field='slug',
                                           read_only=False,
                                           queryset=Subject.objects.all())

    @staticmethod
    def get_user_fullname(obj):
        """
        Получить полное имя пользователя
        :param obj: объект пользователя
        :return: полное имя пользователя
        """
        return '{} {}'.format(obj.student.first_name, obj.student.last_name)

    class Meta:
        model = Attendance
        fields = ['subject', 'student', 'lesson_serial_number', 'is_present',
                  'user_fullname']
