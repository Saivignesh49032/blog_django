# myblogproject/urls.py
from blog.views import SignUpView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Includes Django's built-in login/logout pages
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Admin interface
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    # Include blog app URLs
    path('', include('blog.urls')),
    
    # Include authentication app URLs
    path('auth/', include('authentication.urls')),
    path('polls/', include('polls.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)