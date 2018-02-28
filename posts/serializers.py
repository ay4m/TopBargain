from rest_framework import serializers

from posts.models import PostModel

class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = PostModel
		fields = ('image', 'productName', 'location', 'price',)

	def create(self, validated_data):
		return PostModel(**validated_data)