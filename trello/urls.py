from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', viewset=views.BoardView, basename='board')

urlpatterns = [
    # path('board/', views.BoardView.as_view({'get': 'list'}), name='board-list'),
    # path('board/<int:id>/', views.BoardView.as_view({'get': 'detail'}), name='board-detail'),
    path('', include(router.urls))
]
