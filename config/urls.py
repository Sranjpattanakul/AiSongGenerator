from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/generation/', include('app.routes.generation_urls')),
    path('api/users/', include('app.routes.user_urls')),
    path('api/library/', include('app.routes.manager_urls')),
    path('api/playback/', include('app.routes.playback_urls')),
    path('api/browse/', include('app.routes.browse_urls')),
]
