from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash

from accounts.models import UserAccount

class AccountSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = UserAccount
		# The fields in this serializer class are the same as in UserAccount model in accounts.models

		fields = ('username', 'created_at', 'first_name', 'last_name', 'email', 'profile_image', 'birthdate', 'password')
		# List of the fields serialized		
		read_only_fields = ('created_at',)

		def create(self, validated_data):
			return UserAccount(**validated_data)

		"""
		 Turning a JSON into a Python object is called deserialization and it is handled by the .create() and .update() methods.
		 When creating a new object, such as an Account, .create() is used. When we later update that Account, .update() is used.
		"""