import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app.services.browse_service import BrowseService


@require_http_methods(['GET'])
def list_library(request, user_id):
    service = BrowseService()
    songs = service.list_library(user_id)
    return JsonResponse({'songs': [
        {'id': s.id, 'title': s.title, 'audio_file_url': s.audio_file_url,
         'duration': s.duration, 'is_favorite': s.is_favorite}
        for s in songs
    ]})


@require_http_methods(['GET'])
def list_favorites(request, user_id):
    service = BrowseService()
    songs = service.list_favorites(user_id)
    return JsonResponse({'songs': [
        {'id': s.id, 'title': s.title, 'audio_file_url': s.audio_file_url,
         'duration': s.duration}
        for s in songs
    ]})


@require_http_methods(['GET'])
def get_shared_song(request, token):
    try:
        service = BrowseService()
        song = service.get_shared_song(token)
        return JsonResponse({
            'id': song.id,
            'title': song.title,
            'audio_file_url': song.audio_file_url,
            'duration': song.duration,
        })
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=404)


@csrf_exempt
@require_http_methods(['POST'])
def create_share_link(request, user_id, song_id):
    try:
        data = json.loads(request.body) if request.body else {}
        service = BrowseService()
        link = service.create_share_link(song_id, user_id, expires_at=data.get('expires_at'))
        return JsonResponse({'token': link.unique_token}, status=201)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=400)
