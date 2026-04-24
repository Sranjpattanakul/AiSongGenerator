from app.models import Song, Library, Prompt, Draft
from app.models.song import GenerationStatus


class SongManagerService:
    def list_songs(self, user_id):
        return Song.objects.filter(
            library__user_id=user_id,
            status=GenerationStatus.SUCCESS,
        ).order_by('-created_at')

    def get_song(self, song_id, user_id):
        return Song.objects.get(id=song_id, library__user_id=user_id)

    def toggle_favorite(self, song_id, user_id):
        song = self.get_song(song_id, user_id)
        song.is_favorite = not song.is_favorite
        song.save()
        return song

    def delete_song(self, song_id, user_id):
        Song.objects.filter(id=song_id, library__user_id=user_id).delete()

    def list_drafts(self, user_id):
        return Draft.objects.filter(library__user_id=user_id).order_by('-last_modified_at')

    def save_draft(self, user_id, title, description, occasion, mood, singer_tone, requested_duration):
        library = Library.objects.get(user_id=user_id)
        prompt = Prompt.objects.create(
            title=title,
            description=description,
            occasion=occasion,
            mood=mood,
            singer_tone=singer_tone,
            requested_duration=requested_duration,
        )
        return Draft.objects.create(library=library, prompt=prompt)

    def delete_draft(self, draft_id, user_id):
        Draft.objects.filter(id=draft_id, library__user_id=user_id).delete()
