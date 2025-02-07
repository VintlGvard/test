from django.urls import path, include
from .views import RegisterUserView, LoginUserView

auth = [
    path('register/', RegisterUserView.as_view(), name='RegisterClient'),
    path('login/', LoginUserView.as_view(), name='LoginClient'),
]

urlpatterns = [
    path('auth/', include(auth)),
]
