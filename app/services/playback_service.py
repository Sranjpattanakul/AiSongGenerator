from app.models import PlaybackSession, Song


class PlaybackService:
    def get_or_create_session(self, user_id):
        session, _ = PlaybackSession.objects.get_or_create(user_id=user_id)
        return session

    def play(self, user_id, song_id):
        song = Song.objects.get(id=song_id, library__user_id=user_id)
        session = self.get_or_create_session(user_id)
        session.current_song = song
        session.is_playing = True
        session.current_position = '0:00'
        session.save()
        return session

    def pause(self, user_id):
        session = self.get_or_create_session(user_id)
        session.is_playing = False
        session.save()
        return session

    def update_session(self, user_id, **kwargs):
        session = self.get_or_create_session(user_id)
        allowed = {'current_position', 'volume', 'is_looping', 'loop_start_time', 'loop_end_time'}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(session, key, value)
        session.save()
        return session
