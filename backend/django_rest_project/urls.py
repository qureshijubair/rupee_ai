"""
URL configuration for django_rest_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from . import settings
from django.conf.urls.static import static
from chatbot.views import login, refresh_token, query_api, home_page, favicon_requests

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('favicon.ico', favicon_requests), # To handle favicon.ico request
    path('auth/login/', login, name='login'),  # Your custom login endpoint
    path('auth/refresh/', refresh_token, name='refresh_token'),
    path('api/query/', query_api, name='query_api'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
