from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from posts.models import PostModel

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def instant_search(request, query):
	query = query.replace('-', ' ')

	instant_search_list = {'instantSearchList':[]}
	#dictionary containing list of query hits to be sent as response

	objects = PostModel.objects.filter(productName__icontains=query)
	#query the database for product names which contain the string in query

	[instant_search_list['instantSearchList'].append(str(object)) for object in objects]
	#append the matched product names to the array in the dictionary 

	return Response(instant_search_list)
	#convert the dictionary to JSON and return
