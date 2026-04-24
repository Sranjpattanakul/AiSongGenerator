from django.db import models


class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    ENERGETIC = 'ENERGETIC', 'Energetic'
    CALM = 'CALM', 'Calm'
    ROMANTIC = 'ROMANTIC', 'Romantic'
    INSPIRATIONAL = 'INSPIRATIONAL', 'Inspirational'


class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    WEDDING = 'WEDDING', 'Wedding'
    ANNIVERSARY = 'ANNIVERSARY', 'Anniversary'
    GRADUATION = 'GRADUATION', 'Graduation'
    CELEBRATION = 'CELEBRATION', 'Celebration'
    CUSTOM = 'CUSTOM', 'Custom'


class SingerTone(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    NEUTRAL = 'NEUTRAL', 'Neutral'
    CHILD = 'CHILD', 'Child'


class Prompt(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    occasion = models.CharField(max_length=20, choices=Occasion.choices)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    singer_tone = models.CharField(max_length=20, choices=SingerTone.choices)
    requested_duration = models.CharField(max_length=10, blank=True, default='3:00')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prompt'

    def __str__(self):
        return self.title
