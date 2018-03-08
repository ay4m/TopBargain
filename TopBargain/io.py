from os import remove, path
import posixpath, ntpath

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

def delete_profile_image(account):
	imagePath = str(account.profile_image)
	imagePath = BASE_DIR + '\\' + imagePath
	account.profile_image = None
	account.save()
	remove(imagePath)
	return

def save_profile_image(account, image):
	imagePath = str(account.profile_image)
	imagePath = BASE_DIR + '\\' + imagePath
	remove(imagePath)
	account.profile_image = image
	account.save()
	return