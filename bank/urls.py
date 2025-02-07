from django.urls import path, include
from .views import RegisterUserView, LoginUserView, LogoutUserView, TransactionBetrieveUpdateDestroyAPIView, TransactionListCreateView

auth = [
    path('register/', RegisterUserView.as_view(), name='RegisterClient'),
    path('login/', LoginUserView.as_view(), name='LoginClient'),
    path('logout/', LogoutUserView.as_view(), name='LogoutClient'),
]

transactions = [
    path('', TransactionListCreateView.as_view(), name='transactions'),
    path('<int:pk>', TransactionBetrieveUpdateDestroyAPIView.as_view(), name='transactions'),
]

urlpatterns = [
    path('auth/', include(auth)),
    path('transactions/', include(transactions)),
]
