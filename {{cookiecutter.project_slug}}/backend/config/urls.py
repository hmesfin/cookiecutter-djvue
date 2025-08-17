"""
URL configuration for {{ cookiecutter.project_name }} project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
{% if cookiecutter.use_drf_spectacular == 'y' -%}
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
{%- endif %}

from apps.core.views import home_view

# Customize admin
admin.site.site_header = "{{ cookiecutter.project_name }} Admin"
admin.site.site_title = "{{ cookiecutter.project_name }} Admin Portal"
admin.site.index_title = "Welcome to {{ cookiecutter.project_name }} Administration"

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('api/', include('apps.core.urls')),
    
    {% if cookiecutter.use_drf_spectacular == 'y' -%}
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    {%- endif %}
    
    {% if cookiecutter.use_graphql == 'y' -%}
    # GraphQL
    path('graphql/', include('apps.graphql.urls')),
    {%- endif %}
]

if settings.DEBUG:
    # Static and media files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    {% if cookiecutter.use_debug_toolbar == 'y' -%}
    # Django Debug Toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    {%- endif %}