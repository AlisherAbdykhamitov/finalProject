from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserSignup

urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', UserSignup.as_view({'post': 'signup'})),
    path('managers/signup', UserSignup.as_view({'post': 'create_manager'}))
]

