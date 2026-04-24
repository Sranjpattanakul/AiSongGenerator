from app.models import User, Library, EqualizerPreset


class UserService:
    def get_or_create_user(self, email, display_name, google_id):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'display_name': display_name, 'google_id': google_id},
        )
        if created:
            Library.objects.create(user=user)
        return user, created

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def list_equalizer_presets(self, user_id):
        return EqualizerPreset.objects.filter(user_id=user_id)

    def create_equalizer_preset(self, user_id, name, bass, mid, treble):
        return EqualizerPreset.objects.create(
            user_id=user_id,
            name=name,
            bass_level=bass,
            mid_level=mid,
            treble_level=treble,
        )

    def delete_equalizer_preset(self, preset_id, user_id):
        EqualizerPreset.objects.filter(id=preset_id, user_id=user_id).delete()
