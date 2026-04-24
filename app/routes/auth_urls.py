from django.urls import path
from app.controllers import auth_controller

urlpatterns = [
    path('google/', auth_controller.google_auth, name='google_auth'),
    path('callback/', auth_controller.google_callback, name='google_callback'),
    path('demo/', auth_controller.demo_login, name='demo_login'),
    path('logout/', auth_controller.logout, name='logout'),
]
