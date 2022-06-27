from django.contrib import admin
from .models import Post, PostImage, Category, Group, Comment
# Register your models here.

class PostImageAdmin(admin.StackedInline):
	model = PostImage
	extra = 0

class PostGroupAdmin(admin.StackedInline):
	model = Group
	extra = 0

class PostCommentAdmin(admin.StackedInline):
	model = Comment
	extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	inlines = [PostImageAdmin, PostGroupAdmin, PostCommentAdmin]

	class Meta:
		model = Post

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
	pass

admin.site.register(Category)
admin.site.register(Comment)

	