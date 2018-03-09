from os import remove, path
import posixpath, ntpath

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

def delete_profile_image(account):
	imagePath = str(account.profile_image)
	print(account.profile_image)
	imagePath = BASE_DIR + '\\' + imagePath
	account.profile_image = None
	account.save()
	print(imagePath)
	remove(imagePath)
	return

def save_profile_image(account, image):
	account.profile_image = image
	account.save()
	return