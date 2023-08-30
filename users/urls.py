from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', login_required(views.UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_account/', views.UserRegistrationView.as_view(), name='create_account'),
    path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),
]
