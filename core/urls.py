from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import register,custom_login,profile
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('profile/', profile, name='profile'),
]

urlpatterns += [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)