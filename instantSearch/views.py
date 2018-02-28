from rest_framework.response import Response
from rest_framework.decorators import api_view

from posts.models import PostModel

@api_view(['GET'])
def instant_search(request, query):
	instant_search_list = {'instantSearchList':[]}
	#dictionary containing list of query hits to be sent as response

	objects = PostModel.objects.filter(productName__icontains=query)
	#query the database for product names which contain the string in query

	[instant_search_list['instantSearchList'].append(str(object)) for object in objects]
	#append the matched product names to the array in the dictionary 

	return Response(instant_search_list)
	#convert the dictionary to JSON and return
