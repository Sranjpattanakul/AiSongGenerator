import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app.services.playback_service import PlaybackService


@require_http_methods(['GET'])
def get_session(request, user_id):
    service = PlaybackService()
    session = service.get_or_create_session(user_id)
    return JsonResponse({
        'user_id': user_id,
        'current_song_id': session.current_song_id,
        'current_position': session.current_position,
        'is_playing': session.is_playing,
        'volume': session.volume,
        'is_looping': session.is_looping,
        'loop_start_time': session.loop_start_time,
        'loop_end_time': session.loop_end_time,
    })


@csrf_exempt
@require_http_methods(['POST'])
def play_song(request, user_id):
    try:
        data = json.loads(request.body)
        service = PlaybackService()
        session = service.play(user_id, data['song_id'])
        return JsonResponse({'is_playing': session.is_playing, 'song_id': session.current_song_id})
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def pause_song(request, user_id):
    service = PlaybackService()
    session = service.pause(user_id)
    return JsonResponse({'is_playing': session.is_playing})


@csrf_exempt
@require_http_methods(['PATCH'])
def update_session(request, user_id):
    try:
        data = json.loads(request.body)
        service = PlaybackService()
        session = service.update_session(user_id, **data)
        return JsonResponse({
            'volume': session.volume,
            'is_looping': session.is_looping,
            'current_position': session.current_position,
        })
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=400)
