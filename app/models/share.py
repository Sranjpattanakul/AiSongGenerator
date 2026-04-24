from django.db import models


class ShareLink(models.Model):
    song = models.ForeignKey(
        'app.Song',
        on_delete=models.CASCADE,
        related_name='share_links',
    )
    unique_token = models.CharField(max_length=200, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'share_link'

    def __str__(self):
        return f"ShareLink({self.unique_token})"
