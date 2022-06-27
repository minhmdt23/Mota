from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import login_user, logout_user, register_user, upload_user_avatar

urlpatterns = [
    path('login_user', login_user, name = 'login'),
    path('logout_user', logout_user, name = 'logout'),
    path('register_user', register_user, name = 'register'),
    path('upload_user_avatar', upload_user_avatar, name = 'upload_user_avatar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
