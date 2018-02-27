from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, account):
		"""
		Returns permission of the user (if logged in).
		If not logged in (anonymous user) returns False.
		Only returns True when the user making the request is same as the account passed to this function.
		"""
		if request.user:
			return account == request.user

		return False

