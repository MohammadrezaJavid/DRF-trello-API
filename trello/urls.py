from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', viewset=views.BoardView, basename='board')

list_list = views.ListView.as_view({
    'post': 'create'
})
list_detail = views.ListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path('lists/', list_list, name='list-list'),
    path('lists/<int:id>/', list_detail, name='list-detail'),
]
