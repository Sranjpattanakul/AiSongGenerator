from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=200)
    google_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.display_name
