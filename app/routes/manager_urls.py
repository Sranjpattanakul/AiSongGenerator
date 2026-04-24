from django.urls import path
from app.controllers import song_manager_controller

urlpatterns = [
    path('<int:user_id>/songs/', song_manager_controller.list_songs, name='list_songs'),
    path('<int:user_id>/songs/<int:song_id>/favorite/', song_manager_controller.toggle_favorite, name='toggle_favorite'),
    path('<int:user_id>/songs/<int:song_id>/delete/', song_manager_controller.delete_song, name='delete_song'),
    path('<int:user_id>/drafts/', song_manager_controller.list_drafts, name='list_drafts'),
    path('<int:user_id>/drafts/save/', song_manager_controller.save_draft, name='save_draft'),
    path('<int:user_id>/drafts/<int:draft_id>/delete/', song_manager_controller.delete_draft, name='delete_draft'),
]
