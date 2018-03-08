from django.urls import path

from .views import ProfileView

urlpatterns=[
	path('<slug:user>/', ProfileView.as_view()),
]