from django.db import models


class EqualizerPreset(models.Model):
    user = models.ForeignKey(
        'app.User',
        on_delete=models.CASCADE,
        related_name='equalizer_presets',
    )
    playback_session = models.ForeignKey(
        'app.PlaybackSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equalizer_presets',
    )
    name = models.CharField(max_length=100)
    bass_level = models.FloatField(default=0.0)
    mid_level = models.FloatField(default=0.0)
    treble_level = models.FloatField(default=0.0)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'equalizer_preset'

    def __str__(self):
        return f"EqualizerPreset({self.name})"
