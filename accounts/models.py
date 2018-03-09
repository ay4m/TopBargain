from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
	def create_user(self, email, password, **kwargs):
		if not email:
			raise ValueError('Users must have a valid email address.')

		if not kwargs.get('username'):
			raise ValueError('Users must have a valid username.')

		account = self.model(
			email = self.normalize_email(email), username = kwargs.get('username'), first_name = kwargs.get('first_name', ''),
			last_name = kwargs.get('last_name', '')
		)

		account.set_password(password)
		account.save()
		
		return account

	def create_superuser(self, email, password, **kwargs):
		account = self.create_user(email, password, **kwargs)
		account.is_admin = True
		account.is_staff = True
		account.save()

		

class UserAccount(AbstractBaseUser):
	email = models.EmailField(max_length=80, unique=True)
	username = models.CharField(max_length=40, unique=True, primary_key=True)
	first_name = models.CharField(max_length=40, blank=True)
	last_name = models.CharField(max_length=40, blank=True)
	birthdate = models.DateField(blank=True, null=True)
	profile_image = models.ImageField(upload_to='TopBargain/static/profiles/images/',max_length=140, 
									default='TopBargain/static/default/no_profile_image.png')

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	#dateTime added at time of creation
	updated_at = models.DateTimeField(auto_now=True)
	#dateTime updated each time the data of the user is updated

	objects = AccountManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'password']
	
	def __unicode__(self):
		return self.username

	def get_full_name(self):
		return ' '.join([self.first_name, self.last_name])

	def get_short_name(self):
		return self.first_name
	
	@property
	def is_superuser(self):
		return self.is_admin

	@property
	def is_staff(self):
		return self.is_admin

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin

	@is_staff.setter
	def is_staff(self, value):
		self._is_staff = value
