from django.db import models


class Library(models.Model):
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='library',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'library'

    def __str__(self):
        return f"Library({self.user.display_name})"
