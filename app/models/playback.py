from django.db import models


class PlaybackSession(models.Model):
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='playback_session',
    )
    current_song = models.ForeignKey(
        'app.Song',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='playback_sessions',
    )
    current_position = models.CharField(max_length=10, default='0:00')
    is_playing = models.BooleanField(default=False)
    volume = models.FloatField(default=1.0)
    loop_start_time = models.CharField(max_length=10, blank=True)
    loop_end_time = models.CharField(max_length=10, blank=True)
    is_looping = models.BooleanField(default=False)

    class Meta:
        db_table = 'playback_session'

    def __str__(self):
        return f"PlaybackSession({self.user.display_name})"
