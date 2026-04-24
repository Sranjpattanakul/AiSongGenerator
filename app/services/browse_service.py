from app.models import Song, ShareLink
from app.models.song import GenerationStatus


class BrowseService:
    def list_library(self, user_id):
        return Song.objects.filter(
            library__user_id=user_id,
            status=GenerationStatus.SUCCESS,
        ).order_by('-created_at')

    def list_favorites(self, user_id):
        return Song.objects.filter(
            library__user_id=user_id,
            status=GenerationStatus.SUCCESS,
            is_favorite=True,
        ).order_by('-created_at')

    def get_shared_song(self, token):
        link = ShareLink.objects.select_related('song').get(unique_token=token)
        link.access_count += 1
        link.save()
        return link.song

    def create_share_link(self, song_id, user_id, expires_at=None):
        import secrets
        song = Song.objects.get(id=song_id, library__user_id=user_id)
        token = secrets.token_urlsafe(32)
        return ShareLink.objects.create(song=song, unique_token=token, expires_at=expires_at)
