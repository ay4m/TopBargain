from django.db import models

from accounts.models import UserAccount

class PostModel(models.Model):
	username = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
	product_name = models.TextField(max_length=80)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	post_date = models.DateTimeField(auto_now_add=True)
	location = models.CharField(max_length=100)
	product_image = models.ImageField(upload_to='products/images/',max_length=200, blank=True)

	def __str__(self):
		return self.product_name
