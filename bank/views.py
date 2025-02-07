from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import Client
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class RegisterUserView(CreateAPIView):
    queryset = Client.objects.all
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['data'] = serializer.data
            user = serializer.user
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)

class LoginUserView(APIView):
    queryset = Client.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)

        if not serializer_class.is_valid():
            return Response({
                "error": {
                    "code": 401,
                    "message": 'Ошибка авторизации'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        client = serializer_class.validated_data
        if client:
            token_object, token_created = Token.objects.get_or_create(user=client)
            token = token_object if token_object else token_created
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Не правильный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)
