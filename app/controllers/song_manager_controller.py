import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app.services.song_manager_service import SongManagerService


@require_http_methods(['GET'])
def list_songs(request, user_id):
    service = SongManagerService()
    songs = service.list_songs(user_id)
    return JsonResponse({'songs': [
        {'id': s.id, 'title': s.title, 'audio_file_url': s.audio_file_url,
         'duration': s.duration, 'is_favorite': s.is_favorite,
         'play_count': s.play_count, 'created_at': s.created_at.isoformat()}
        for s in songs
    ]})


@csrf_exempt
@require_http_methods(['PATCH'])
def toggle_favorite(request, user_id, song_id):
    try:
        service = SongManagerService()
        song = service.toggle_favorite(song_id, user_id)
        return JsonResponse({'id': song.id, 'is_favorite': song.is_favorite})
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=404)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_song(request, user_id, song_id):
    service = SongManagerService()
    service.delete_song(song_id, user_id)
    return JsonResponse({'success': True})


@require_http_methods(['GET'])
def list_drafts(request, user_id):
    service = SongManagerService()
    drafts = service.list_drafts(user_id)
    return JsonResponse({'drafts': [
        {'id': d.id, 'title': d.prompt.title, 'mood': d.prompt.mood,
         'occasion': d.prompt.occasion, 'last_modified_at': d.last_modified_at.isoformat()}
        for d in drafts
    ]})


@csrf_exempt
@require_http_methods(['POST'])
def save_draft(request, user_id):
    try:
        data = json.loads(request.body)
        service = SongManagerService()
        draft = service.save_draft(
            user_id=user_id,
            title=data.get('title', 'Untitled'),
            description=data.get('description', ''),
            occasion=data.get('occasion', 'CUSTOM'),
            mood=data.get('mood', 'HAPPY'),
            singer_tone=data.get('singer_tone', 'NEUTRAL'),
            requested_duration=data.get('requested_duration', '3:00'),
        )
        return JsonResponse({'id': draft.id, 'title': draft.prompt.title}, status=201)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_draft(request, user_id, draft_id):
    service = SongManagerService()
    service.delete_draft(draft_id, user_id)
    return JsonResponse({'success': True})
