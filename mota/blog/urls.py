from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, post_detail, post, get_comment, create_comment, get_reply_form, image_gallery

urlpatterns = [
    path('', home, name='home'),
    path('post/', post, name='post'),
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('getCommentPost/<int:id>', get_comment, name='get_comment'),
    path('create_comment/', create_comment, name='create_comment'),
    path('getReplyForm/', get_reply_form, name='get_reply_form'),
    path('image_gallery', image_gallery, name = 'image_gallery'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
