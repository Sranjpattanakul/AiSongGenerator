from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import MinValueValidator, MaxValueValidator
import re
from django.core.exceptions import ValidationError


# Enumerations
class GenerationStatus(models.TextChoices):
    QUEUED = 'QUEUED', 'Queued'
    GENERATING = 'GENERATING', 'Generating'
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'


class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    WEDDING = 'WEDDING', 'Wedding'
    ANNIVERSARY = 'ANNIVERSARY', 'Anniversary'
    GRADUATION = 'GRADUATION', 'Graduation'
    CELEBRATION = 'CELEBRATION', 'Celebration'
    CUSTOM = 'CUSTOM', 'Custom'


class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    ENERGETIC = 'ENERGETIC', 'Energetic'
    CALM = 'CALM', 'Calm'
    ROMANTIC = 'ROMANTIC', 'Romantic'
    INSPIRATIONAL = 'INSPIRATIONAL', 'Inspirational'


class SingerTone(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    NEUTRAL = 'NEUTRAL', 'Neutral'
    CHILD = 'CHILD', 'Child'


# Validators
def validate_duration(value):
    """Validate duration format mm:ss and range 2:00 - 6:00"""
    pattern = r'^([0-5]?\d):([0-5]\d)$'
    if not re.match(pattern, value):
        raise ValidationError('Duration must be in mm:ss format')
    
    minutes, seconds = map(int, value.split(':'))
    total_seconds = minutes * 60 + seconds
    
    if total_seconds < 120:  # 2:00
        raise ValidationError('Duration must be at least 2:00 minutes')
    if total_seconds > 360:  # 6:00
        raise ValidationError('Duration must not exceed 6:00 minutes')


# Domain Entities
class UserProfile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='profile')
    google_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    class Meta:
        db_table = 'user_profiles'


class Library(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='library')

    def __str__(self):
        return f"Library of {self.user.username}"

    class Meta:
        db_table = 'libraries'
        verbose_name_plural = 'Libraries'


class Prompt(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requested_duration = models.CharField(max_length=5, validators=[validate_duration])
    occasion = models.CharField(max_length=20, choices=Occasion.choices)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    singer_tone = models.CharField(max_length=20, choices=SingerTone.choices)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'prompts'


class Song(models.Model):
    title = models.CharField(max_length=200)
    audio_file_url = models.URLField()
    duration = models.CharField(max_length=5, validators=[validate_duration])
    is_favorite = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=GenerationStatus.choices, default=GenerationStatus.QUEUED)
    
    # Relationships
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='songs')
    prompt = models.ForeignKey(Prompt, on_delete=models.PROTECT, related_name='songs')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'songs'


class Draft(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='drafts')
    prompt = models.OneToOneField(Prompt, on_delete=models.CASCADE, related_name='draft')

    def __str__(self):
        return f"Draft: {self.prompt.title}"

    class Meta:
        db_table = 'drafts'


class ShareLink(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='share_links')
    unique_token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Share link for {self.song.title}"

    class Meta:
        db_table = 'share_links'


class PlaybackSession(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='playback_session')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='playback_sessions')
    current_position = models.CharField(max_length=5)
    is_playing = models.BooleanField(default=False)
    volume = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0.5)
    loop_start_time = models.CharField(max_length=5, blank=True, null=True)
    loop_end_time = models.CharField(max_length=5, blank=True, null=True)
    is_looping = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s playback"

    class Meta:
        db_table = 'playback_sessions'


class EqualizerPreset(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='equalizer_presets')
    name = models.CharField(max_length=100)
    bass_level = models.FloatField(validators=[MinValueValidator(-12.0), MaxValueValidator(12.0)])
    mid_level = models.FloatField(validators=[MinValueValidator(-12.0), MaxValueValidator(12.0)])
    treble_level = models.FloatField(validators=[MinValueValidator(-12.0), MaxValueValidator(12.0)])

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        db_table = 'equalizer_presets'