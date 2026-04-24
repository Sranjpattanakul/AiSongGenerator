from django.urls import path
from app.controllers import browse_controller

urlpatterns = [
    path('<int:user_id>/library/', browse_controller.list_library, name='list_library'),
    path('<int:user_id>/favorites/', browse_controller.list_favorites, name='list_favorites'),
    path('<int:user_id>/songs/<int:song_id>/share/', browse_controller.create_share_link, name='create_share_link'),
    path('shared/<str:token>/', browse_controller.get_shared_song, name='get_shared_song'),
]
