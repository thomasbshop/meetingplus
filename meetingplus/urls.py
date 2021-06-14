"""meetingplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
# from minutes.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("accounts/", include("authentication.urls")), # Auth routes - login / register
    path("", include('core.urls')),
    # path("meeting/", include('core.urls')),
    path("meeting/", include('meeting_room.urls', namespace='room')),
    path("meeting/", include('document.urls')),
]

#Add URL maps to redirect the base URL to our application
# from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='meeting/', permanent=True)),
# ]

# Use static() to add url mapping to serve static files during development (only)

from django.conf.urls.static import static
from core import views as core_views
# urlpatterns = i18n_patterns(
#     # other URL configuration rules...
#     path("js-settings/", core_views.js_settings,
#     name="js_settings"),
# )
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)