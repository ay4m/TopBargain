from rest_framework import serializers

from posts.models import PostModel

class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = PostModel
		fields = (username, product_name, price, post_date, location, product_image,)

	def create(self, validated_data):
		return PostModel(**validated_data)