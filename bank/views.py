from django.contrib.auth import logout
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserLoginSerializer, TransactionsSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Transaction, Client

class RegisterUserView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": {"code": 401, "message": "Ошибка авторизации"}}, status=status.HTTP_401_UNAUTHORIZED)

        client = serializer.validated_data
        if client:
            token, _ = Token.objects.get_or_create(user=client)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except:
            return Response({"error": {"code": 401, "message": "Не получилось выйти"}}, status=status.HTTP_401_UNAUTHORIZED)

        logout(request)
        return Response({"data": {"message": "Успешно вышел"}}, status=status.HTTP_200_OK)

class TransactionListCreateView(GenericAPIView, CreateModelMixin, ListModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TransactionBetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)