from django.db import models
from .song import GenerationStatus


class GenerationJob(models.Model):
    song = models.OneToOneField(
        'app.Song',
        on_delete=models.CASCADE,
        related_name='generation_job',
    )
    prompt = models.ForeignKey(
        'app.Prompt',
        on_delete=models.SET_NULL,
        null=True,
        related_name='generation_jobs',
    )
    task_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20,
        choices=GenerationStatus.choices,
        default=GenerationStatus.QUEUED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'generation_job'

    def __str__(self):
        return f"GenerationJob({self.task_id}, {self.status})"
