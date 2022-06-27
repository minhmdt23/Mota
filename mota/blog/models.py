from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime
from django.utils import timezone
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=255)
	decription = models.CharField(max_length=512)
	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=255)
	image = models.ImageField(blank=True)
	pubdate = models.DateField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	decription = models.CharField(max_length=512)
	content = RichTextField()
	class Meta:
		ordering = ['-id']

	def date_fomat_d_m_y(self):
		return self.pubdate.strftime("%d/%m/%Y")
		
	def __str__(self):
		return self.title

class Group(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.post.title + " " + self.category.name

def post_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
	 return 'post_{0}/{1}'.format(instance.post.id, filename)

class PostImage(models.Model):
	post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=post_directory_path)
	def __str__(self):
		return self.post.title + " " + str(self.id)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	# manually deactivate inappropriate comments from admin site
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

	def was_published(self):
		was_created = timezone.now() - self.created
		if was_created.total_seconds() > 60:
			minutes = int(was_created.total_seconds()/60)
			if minutes > 60:
				hours = int(minutes/60)
				if hours > 24:
					days = int(hours/24)
					if days > 7:
						weeks = int(days/7)
						if weeks > 4:
							months = int(weeks/4)
							if months > 12:
								years = int(months/12)
								return str(years)+" "+"năm trước"

							return str(month)+" "+"tháng trước"

						return str(weeks)+" "+"tuần trước"

					return str(days)+" "+"ngày trước"

				return str(hours)+" "+"giờ trước"

			return str(minutes)+" "+"phút trước"

		else:
			return str(int(was_created.total_seconds()))+" "+"giây trước"





	class Meta:
		# sort comments in chronological order by default
		ordering = ('-created',)

	def __str__(self):
		return self.body