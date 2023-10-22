from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', viewset=views.BoardView, basename='board')

listList = views.ListView.as_view({
    'post': 'create'
})
listDetail = views.ListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

cardList = views.CardView.as_view({
    'get': 'list',
    'post': 'create'
})
cardDetail = views.CardView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tagCardList = views.TagCardView.as_view({
    'get': 'list'
})

cardCommentList = views.CommentView.as_view({
    'get': 'list',
    'post': 'create'
})
cardCommentDetail = views.CommentView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

notificationUserList = views.NotificationView.as_view({
    'get': 'list'
})

urlpatterns = [
    path('', include(router.urls)),

    path('lists/', listList, name='list-list'),
    path('lists/<int:id>/', listDetail, name='list-detail'),

    path('cards/', cardList, name='card-list'),
    path('cards/<int:id>/', cardDetail, name='card-detail'),

    path('cards/tag/<str:tag>/', tagCardList, name='card-list-by-tag'),

    path('cards/comment/', cardCommentList, name='comment-list'),
    path('cards/comment/<int:id>/', cardCommentDetail, name='comment-detail'),

    path('user/notifications/', notificationUserList, name='notification-list')
]
