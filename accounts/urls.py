from django.urls import path
from accounts.views import LoginView, RegisterView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('isCredentialComing/', LoginView.as_view()),
    #path('obtain-auth-token/', obtain_auth_token),
]