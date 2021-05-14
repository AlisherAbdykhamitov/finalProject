from django.urls import path
from main import views

urlpatterns = [
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>', views.CategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy',
                                                               'put': 'update'})),
    path('categories/<int:pk>/book', views.BookViewSet.as_view({'get': 'retrieve'})),
    path('books/', views.BookViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('books/<int:pk>', views.BookViewSet.as_view({'delete': 'destroy', 'get': 'select', 'put': 'update'})),
    path('cards', views.credit_card),
    path('cards/<int:pk>', views.CardAPIView.as_view()),
    path('liked/<int:pk>', views.LikedAPIView.as_view()),
    path('liked', views.liked),
    path('orders', views.orders),
    path('orders/<int:pk>', views.OrderAPIView.as_view()),

]