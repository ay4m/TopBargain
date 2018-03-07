from django.urls import path

from .views import PostView

urlpatterns = [
	path('image/', PostView.as_view()),
]