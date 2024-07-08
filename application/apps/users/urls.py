from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .views import LoginView, UserProfileView, RegistrationView, activate_user

urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', login_required(LogoutView.as_view(next_page='main_page')), name='logout'),
    path('activate-user/<uidb64>/<token>', activate_user, name='activate')
]