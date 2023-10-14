from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='access-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),

    path('user/', views.UserList.as_view(), name='user-list'),
    path('user/<int:id>/', views.UserDetail.as_view(), name='user-detail'),
    path('user/register/', views.Register.as_view(), name='user-register'),
]
