from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from app.controllers import home_controller, pages_controller


def login_page(request):
    if request.session.get('user_email'):
        return redirect('home')
    return render(request, 'login.html', {
        'google_client_id': settings.GOOGLE_CLIENT_ID,
    })


urlpatterns = [
    path('', home_controller.index, name='home'),
    path('library/', pages_controller.library_page, name='library'),
    path('browse/', pages_controller.browse_page, name='browse'),
    path('login/', login_page, name='login'),
    path('auth/', include('app.routes.auth_urls')),
    path('admin/', admin.site.urls),
    path('api/generation/', include('app.routes.generation_urls')),
    path('api/users/', include('app.routes.user_urls')),
    path('api/library/', include('app.routes.manager_urls')),
    path('api/playback/', include('app.routes.playback_urls')),
    path('api/browse/', include('app.routes.browse_urls')),
]
