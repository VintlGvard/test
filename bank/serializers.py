from django.contrib.auth import authenticate
from .models import Client
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = Client
        fields = ('id', 'username', 'password', 'password2')

    def save(self, *args, **kwargs):
        user = Client(
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'detail': "Пароли не совпадают"})
        user.set_password(password)
        user.save()

        self.user = user

        return self.user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    client: Client = None

    def validate(self, data):
        client = authenticate(**data)
        if client:
            return client
        return False