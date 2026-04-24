from django.db import models


class Draft(models.Model):
    prompt = models.OneToOneField(
        'app.Prompt',
        on_delete=models.CASCADE,
        related_name='draft',
    )
    library = models.ForeignKey(
        'app.Library',
        on_delete=models.CASCADE,
        related_name='drafts',
    )
    saved_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'draft'

    def __str__(self):
        return f"Draft({self.prompt.title})"
