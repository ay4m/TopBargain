from django.urls import path

from instantSearch.views import instant_search

urlpatterns = [
	path('<slug:query>/', instant_search),
]