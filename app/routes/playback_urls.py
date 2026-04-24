from django.urls import path
from app.controllers import playback_controller

urlpatterns = [
    path('<int:user_id>/', playback_controller.get_session, name='get_session'),
    path('<int:user_id>/play/', playback_controller.play_song, name='play_song'),
    path('<int:user_id>/pause/', playback_controller.pause_song, name='pause_song'),
    path('<int:user_id>/update/', playback_controller.update_session, name='update_session'),
]
