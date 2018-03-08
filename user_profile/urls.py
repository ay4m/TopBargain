from django.urls import path

from .views import ProfileView

urlpatterns=[
	path('', ProfileView.as_view()),
	path('<slug:user>/', ProfileView.as_view()),
]