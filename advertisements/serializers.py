from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        text = '''В настоящее время у Вас 10 объявлений в статусе открыто.
                  Для открытия нового объявления необходимо закрыть одно из объявлений.'''

        if self.context['request'].stream.method == 'PATCH' or self.context['request'].stream.method == 'PUT':
            if self.instance.status == 'CLOSED':
                raise ValidationError('Вы пытаетесь изменить объявление, которое уже закрыто.')
            return data
        quantity = Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count()
        if quantity >= 10:
            raise ValidationError(text.replace('\n', ''))

        return data
