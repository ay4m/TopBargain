import json
from rest_framework.response import Response
from rest_framework import views

from posts.models import PostModel
from accounts.models import UserAccount
from posts.serializers import PostSerializer

class PostView(views.APIView):

	def post(self, request):
		data = json.loads(request.body)
        #loads json data from the request and converts to python dictionary
		username = data.get('personname', '')

		###############################################
		data['productName'] = data.get('product', '')
		data.pop('product', None)
		#################################### change 'product' to 'productName' in front-end and delete these lines

		serialized = PostSerializer(data=data)
		user_info = UserAccount.objects.get(username=username)

		if serialized.is_valid() and user_info is not None:
			post = PostModel(username=user_info, **serialized.data)
			post.save()
			return Response({
					'success': 'yes',
				})

		return Response({
				'success': 'no',
			})
