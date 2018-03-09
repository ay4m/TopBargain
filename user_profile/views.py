import json
from rest_framework import status, views, permissions
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import AnonymousUser
#update_session_auth_hash(self.context.get('request'), instance)#account

from accounts.serializers import AccountSerializer
from accounts.models import UserAccount
from accounts.permissions import IsAccountOwner
from posts.models import PostModel
from search.serializers import PostSerializer
from TopBargain.io import delete_profile_image, save_profile_image

WHITELIST = ['jpeg', 'jpg', 'bmp', 'png', 'gif', 'tiff']

class ProfileView(views.APIView):

	def get_permissions(self):
		if self.request.method in permissions.SAFE_METHODS:
			return (permissions.AllowAny(),)

		return (permissions.IsAuthenticated(),)

	def get(self, request, user=None):
		if request.user.username == user:
			user = None
		
		self_profile = False

		if user is not None:
			user = user.replace('-', ' ')

			try:
				account = UserAccount.objects.get(username=user)
				self_profile = False
			except:
				return Response({
					'message': 'Username ' + user + ' does not exist.',
				}, status=status.HTTP_404_NOT_FOUND)
		else:
			account = request.user
			self_profile = True
			if isinstance(account, AnonymousUser):
				return Response({
					'success': 'no',
					'message': 'User unauthorized to make the request.'
				}, status=status.HTTP_403_FORBIDDEN)

		serialized = AccountSerializer(account)
		serialized = dict(serialized.data)  #no need to validate as it is surely a UserAccount instance
		
		try:
			path = serialized['profile_image'].split('TopBargain/')[1]
		except:
			path = ''

		serialized['profilePic'] = path			
		serialized.pop('profile_image')

		print(request.user.username)

		if self_profile:
			serialized['isSelfProfile'] = True
		else:
			serialized['isSelfProfile'] = False

		serialized['posts'] = []
		posts = PostModel.objects.filter(username=account).order_by('-postDate')

		for post in posts:
			serialized_post = PostSerializer(post)
			serialized_post = dict(serialized_post.data)
			
			try:
				serialized_post['image'] = serialized_post['image'].split('TopBargain/')[1] #to get the static URL
			except:
				serialized_post['image'] = None

			serialized['posts'].append(serialized_post)

		return Response(serialized)

	def post(self, request, username=None):
		account = request.user

		profileData = dict(request.POST)


		try:
			image = request.FILES['profilePic']
		except:
			image=None
		
		if image is not None:
			#image = image[0] ################## Also _^
			ext = image.name.split('.')[1]
			ext = ext.lower()
			
			if ext not in WHITELIST:
				return Response({
					'success': 'no',
					'message': 'Request not successful. Invalid image format.'
				}, status = status.HTTP_406_NOT_ACCEPTABLE)
			
			if str(account.profile_image) is not '':
				delete_profile_image(account)

			image.name = account.username + '.' + ext
			save_profile_image(account, image)

			return Response({
				'profilePic': str(account.profile_image).split('TopBargain/')[1],
			})
		
		changed_val = ''

		if 'fullName' in profileData and  profileData['fullName'][0] is not '':
			name = profileData['fullName'][0].split()
			account.first_name = name[0]
			
			try:
				account.last_name = name[1]
			except:
				pass

		if 'birthdate' in profileData and profileData['birthdate'][0] is not '':
			if profileData['birthdate'][0] != account.birthDate:
				account.birthDate = profileData['birthdate'][0]
				changed_val = 'Date of birth'

		if 'email' in profileData and profileData['email'][0] is not '':
			if profileData['email'][0] != account.email:
				account.email = profileData['email'][0]
				changed_val = 'Email'

		if 'password' in profileData and profileData['password'][0] is not '':
			account.set_password(password)
			changed_val = 'Password'

		account.save()
		print(account)

		return Response({
				'success': 'yes',
				'message': changed_val + ' successfully changed.'
		})





