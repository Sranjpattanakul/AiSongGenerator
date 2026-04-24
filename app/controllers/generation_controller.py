import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app.models import User, Library, Song, Prompt
from app.services.generation_service import GenerationService
from app.strategies.exceptions import GenerationError


@csrf_exempt
@require_http_methods(['POST'])
def generate_song(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, Exception):
        return JsonResponse({'success': False, 'error': 'Invalid JSON body'}, status=400)

    try:
        user, _ = User.objects.get_or_create(
            email=data.get('user_email', 'demo@example.com'),
            defaults={
                'display_name': data.get('user_name', 'Demo User'),
                'google_id': data.get('google_id', 'demo-google-id'),
            },
        )
        library, _ = Library.objects.get_or_create(user=user)

        prompt = Prompt.objects.create(
            title=data.get('title', 'My Song'),
            description=data.get('description', ''),
            occasion=data.get('occasion', 'CELEBRATION'),
            mood=data.get('mood', 'HAPPY'),
            singer_tone=data.get('singer_tone', 'NEUTRAL'),
            requested_duration=data.get('requested_duration', '3:00'),
        )

        song = Song.objects.create(
            library=library,
            title=prompt.title,
        )

        service = GenerationService(strategy=data.get('strategy'))
        job = service.start_generation(prompt, song)

        song.refresh_from_db()
        return JsonResponse({
            'success': True,
            'task_id': job.task_id,
            'song_id': song.id,
            'status': job.status,
            'audio_url': song.audio_file_url,
            'image_url': song.image_url,
            'message': 'Song generation started',
        }, status=201)

    except GenerationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=502)
    except Exception as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=500)


@require_http_methods(['GET'])
def generation_status(request, task_id):
    try:
        strategy = 'mock' if task_id.startswith('mock-') else 'suno'
        service = GenerationService(strategy=strategy)
        result = service.check_status(task_id)
        return JsonResponse({'success': True, **result})
    except GenerationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=502)
    except Exception as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=500)
