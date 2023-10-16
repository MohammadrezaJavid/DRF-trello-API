from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', viewset=views.BoardView, basename='board')
# router.register(r'tag', views.TagCardView, basename='tag')
list_list = views.ListView.as_view({
    # 'get': 'list',
    'post': 'create'
})
list_detail = views.ListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

card_list = views.CardView.as_view({
    # 'get': 'list',
    'post': 'create'
})
card_detail = views.CardView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),

    path('lists/', list_list, name='list-list'),
    path('lists/<int:id>/', list_detail, name='list-detail'),

    path('cards/', card_list, name='card-list'),
    path('cards/<int:id>/', card_detail, name='card-detail'),
    path('cards/tag/<str:tag>/', views.TagCardView.as_view({'get': 'list'}), name='card-list-by-tag'),
]
