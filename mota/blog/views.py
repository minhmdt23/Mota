from django.shortcuts import render, get_object_or_404
from .models import Post, PostImage, Group, Category, Comment, PostImage
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
	posts = Post.objects.order_by('-id')[:3]
	context = {
		'posts': posts,
	}
	return render(request, 'blog/home.html', context)

def post(request):
	posts = Post.objects.all()
	search = ''
	# category = ''
	groups = {}
	current_category = ''
	page_obj_previous = 0
	page_obj_next = 0
	category_choose = ''

	if request.method == 'GET':

		if request.GET.get('search'):
			search = request.GET.get('search')
			posts = Post.objects.filter(Q(title__contains=search) | Q(decription__contains=search))

		if request.GET.get('category'):

			category_id = request.GET.get('category')
			current_category = category_id
			category_choose = Category.objects.filter(id__in=category_id)
			groups = Group.objects.filter(category__in=category_choose)

			post_id = set()
			for i in groups:
				post_id.add(i.post.id)

			posts = Post.objects.filter(id__in = post_id)


	paginator = Paginator(posts, 7)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	if page_obj.has_previous():
		page_obj_previous = paginator.get_page(page_obj.previous_page_number())
	if page_obj.has_next():
		page_obj_next = paginator.get_page(page_obj.next_page_number())
	

	context = {
		'posts': posts,
		'search': search,
		'groups': groups,
		'category_choose': category_choose,
		'page_obj': page_obj,
		'current_category': current_category,
		'page_obj_previous': page_obj_previous,
		'page_obj_next': page_obj_next,
	}
	return render(request, 'blog/post.html', context)


def get_comment(request, id):
	post = Post.objects.get(id=id)
	comments = Comment.objects.filter(Q(post=post) & Q(parent__isnull=True))

	context = {
		"comments": comments,
		"post": post,
	}

	return render(request, 'blog/post_comment.html', context)

def create_comment(request):
	if request.method == 'POST':
		comment = request.POST['comment']
		if comment != '':
			parent = None
			user_id = int(request.POST['user_id'])
			user = User.objects.get(id=user_id)
			post_id = int(request.POST['post_id'])
			post = Post.objects.get(id=post_id)
			
			if request.POST.get('parent_id'):
				parent_id = int(request.POST.get('parent_id'))
				parent = Comment.objects.get(id=parent_id)

		new_comment = Comment(post=post, author=user, body=comment, parent=parent)
		new_comment.save()

	return HttpResponse("New comment add successfully")


def get_reply_form(request):

	parent_comment = ''
	post = ''

	if request.method == 'POST':
		parent_id = int(request.POST['parent_id'])
		parent_comment = Comment.objects.get(id=parent_id)
		post = parent_comment.post

	context = {
		'parent_comment': parent_comment,
		'post': post,
	}

	return render(request, 'blog/reply_form.html', context)

def post_detail(request, id):
	comment = ''

	post = get_object_or_404(Post, id=id)
	comments = Comment.objects.filter(Q(post=post) & Q(parent__isnull=True))

	if request.method == 'POST':
		if request.POST.get('comment'):
			comment = request.POST.get('comment')

	context = {
		'post': post,
		'comments': comments,
		'comment': comment,

	}
	return render(request, 'blog/post_detail.html', context)

def image_gallery(request):
	post_images = PostImage.objects.all()

	post_id = set()
	for i in post_images:
		post_id.add(i.post.id)

	post = Post.objects.filter(id__in = post_id)
	context = {
		'post_images': post_images,
		'post': post,
	}
	return render(request, 'blog/image_gallery.html', context)