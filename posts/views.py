import json
import rest_framework
from rest_framework.response import Response
from rest_framework import views
from django.core.files.storage import FileSystemStorage

from posts.models import PostModel
from accounts.models import UserAccount
from posts.serializers import PostSerializer

class PostView(views.APIView):
	def post(self, request):
		image = request.FILES['productImage']

		success = ''

		data = dict(request.POST)

		username = request.user
		data['productName'] = data.get('productName', '')
		
		data['productName'] = data['productName'][0]
		data['price'] = int(data['price'][0])
		data['location'] = data['location'][0]

		image.name = username + '_' + data['productName']

		serialized = PostSerializer(data=data)
		user = UserAccount.objects.get(username=username)

		if serialized.is_valid() and user_info is not None:
			post = PostModel(username=user, **serialized.data)
			#username is a foreignkey field. so instance is sent
			post.save()
			success = 'yes'
		else:
			success = 'no'

		return Response({
			'success': success
		})