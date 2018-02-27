from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash

from accounts.models import UserAccount

class AccountSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	confirm_password = serializers.CharField(write_only=True, required=False)
	"""
	Both these fields are only required when the user is attempting to change their password.
	Although passwords are in hashed and salted form, they shoould not visible to user. So, write_only is True.
	"""

	class Meta:
		model = UserAccount
		# The fields in this serializer class are the same as in UserAccount model in accounts.models

		fields = ('username', 'created_at', 'updated_at', 'first_name',
					'last_name', 'tagline', 'password', 'confirm_password')
		# List of the fields serialized
		
		read_only_fields = ('created_at', 'updated_at')
		#declared as read only as they should not be altered by users

		def create(self, validated_data):
			return UserAccount(**validated_data)

		"""
		 Turning a JSON into a Python object is called deserialization and it is handled by the .create() and .update() methods.
		 When creating a new object, such as an Account, .create() is used. When we later update that Account, .update() is used.
		"""

		def update(self, instance, validated_data):
			instance.username = validated_data.get('username', instance.username)
			instance.tagline = validated_data.get('tagline', instance.tagline)
			instance.save()

			password = validated_data.get('password', None)
			confirm_password = validated_data.get('confirm_password', None)

			if password and confirm_password and password==confirm_password:
				instance.set_password(password)
				instance.save()
			#passwords only updated if the both password and confirm password fields are present and are same.

			update_session_auth_hash(self.context.get('request'), instance)
			"""
			When a user's password is updated, their session authentication hash must be explicitly updated.
			If we don't do this here, the user will not be authenticated on their next request and will have to log in again.
			"""

			return instance