from django.urls import path
from .views import RegistrationView, CustomLoginView, UserProfileView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-detail')
]