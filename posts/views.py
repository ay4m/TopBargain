import json, rest_framework
from rest_framework.response import Response
from rest_framework import views, permissions, status
from django.core.files.storage import FileSystemStorage

from posts.models import PostModel
from accounts.models import UserAccount
from posts.serializers import PostSerializer

WHITELIST = ['jpg', 'bmp', 'png', 'gif', 'tiff']

class PostView(views.APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request):
		image = request.FILES['productImage']

		err_msg = ''

		data = dict(request.POST)

		username = request.user
		data['productName'] = data.get('productName', '')
		
		data['productName'] = data['productName'][0]
		data['price'] = int(data['price'][0])
		data['location'] = data['location'][0]

		serialized = PostSerializer(data=data)

		user_instance = UserAccount.objects.get(username=username)

		if image is not None:
			ext = image.name.split('.')[1]
			ext = ext.lower()
			if ext not in WHITELIST:
				err_msg += 'invalid image format; '

			image.name = str(username) + '_' + data['productName'] + '.' + ext   # username_productname.jpg

		if not serialized.is_valid():
			err_msg += 'invalid input.'

		if len(err_msg) > 0:
			return Response({
				'success': 'no',
				'message': 'Post not successful; ' + err_msg
			}, status = status.HTTP_406_NOT_ACCEPTABLE)

		post = PostModel(username=user_instance, **serialized.data)
		#username is a foreignkey field. so instance is sent
		post.image = image			
		post.save()
		return Response({
			'success': 'yes',
			'message': 'Post successful'
		})