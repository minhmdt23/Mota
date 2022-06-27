from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
	return '{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
	user   = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	avatar = models.ImageField(default='default_user_avatar/default_user.png', upload_to=user_directory_path, null=True, blank=True )

	def __str__(self):
		return self.user.username