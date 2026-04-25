from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser
from .models import (
    UserProfile, Library, Prompt, Song, Draft, 
    ShareLink, PlaybackSession, EqualizerPreset
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_id')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'occasion', 'mood', 'singer_tone', 'requested_duration')
    list_filter = ('occasion', 'mood', 'singer_tone')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'is_favorite', 'duration', 'library')
    list_filter = ('status', 'is_favorite')
    search_fields = ('title',)


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'user')


@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ('song', 'unique_token', 'expires_at')


@admin.register(PlaybackSession)
class PlaybackSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'is_playing', 'current_position')


@admin.register(EqualizerPreset)
class EqualizerPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'bass_level', 'mid_level', 'treble_level')