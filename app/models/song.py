from django.db import models


class GenerationStatus(models.TextChoices):
    QUEUED = 'QUEUED', 'Queued'
    GENERATING = 'GENERATING', 'Generating'
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'


class Song(models.Model):
    library = models.ForeignKey(
        'app.Library',
        on_delete=models.CASCADE,
        related_name='songs',
    )
    title = models.CharField(max_length=200)
    audio_file_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True)
    status = models.CharField(
        max_length=20,
        choices=GenerationStatus.choices,
        default=GenerationStatus.QUEUED,
    )
    is_favorite = models.BooleanField(default=False)
    play_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'song'

    def __str__(self):
        return self.title
