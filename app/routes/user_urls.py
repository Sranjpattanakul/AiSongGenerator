from django.urls import path
from app.controllers import user_controller

urlpatterns = [
    path('', user_controller.create_user, name='create_user'),
    path('<int:user_id>/', user_controller.get_user, name='get_user'),
    path('<int:user_id>/equalizer/', user_controller.list_equalizer_presets, name='list_equalizer_presets'),
    path('<int:user_id>/equalizer/create/', user_controller.create_equalizer_preset, name='create_equalizer_preset'),
    path('<int:user_id>/equalizer/<int:preset_id>/delete/', user_controller.delete_equalizer_preset, name='delete_equalizer_preset'),
]
