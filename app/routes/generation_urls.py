from django.urls import path
from app.controllers import generation_controller

urlpatterns = [
    path('generate/', generation_controller.generate_song, name='generate_song'),
    path('status/<str:task_id>/', generation_controller.generation_status, name='generation_status'),
]
