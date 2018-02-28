from django.urls import path

from .views import search_view

urlpatterns = [
	path('<slug:query>/', search_view),
]