import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from app.services.user_service import UserService


@csrf_exempt
@require_http_methods(['POST'])
def create_user(request):
    try:
        data = json.loads(request.body)
        service = UserService()
        user, created = service.get_or_create_user(
            email=data['email'],
            display_name=data.get('display_name', ''),
            google_id=data.get('google_id', ''),
        )
        return JsonResponse({
            'id': user.id,
            'email': user.email,
            'display_name': user.display_name,
            'created': created,
        }, status=201 if created else 200)
    except KeyError as exc:
        return JsonResponse({'error': f'Missing field: {exc}'}, status=400)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)


@require_http_methods(['GET'])
def get_user(request, user_id):
    try:
        service = UserService()
        user = service.get_user(user_id)
        return JsonResponse({
            'id': user.id,
            'email': user.email,
            'display_name': user.display_name,
            'created_at': user.created_at.isoformat(),
        })
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=404)


@require_http_methods(['GET'])
def list_equalizer_presets(request, user_id):
    service = UserService()
    presets = service.list_equalizer_presets(user_id)
    return JsonResponse({'presets': [
        {'id': p.id, 'name': p.name, 'bass_level': p.bass_level,
         'mid_level': p.mid_level, 'treble_level': p.treble_level}
        for p in presets
    ]})


@csrf_exempt
@require_http_methods(['POST'])
def create_equalizer_preset(request, user_id):
    try:
        data = json.loads(request.body)
        service = UserService()
        preset = service.create_equalizer_preset(
            user_id=user_id,
            name=data.get('name', 'My Preset'),
            bass=data.get('bass_level', 0.0),
            mid=data.get('mid_level', 0.0),
            treble=data.get('treble_level', 0.0),
        )
        return JsonResponse({
            'id': preset.id,
            'name': preset.name,
            'bass_level': preset.bass_level,
            'mid_level': preset.mid_level,
            'treble_level': preset.treble_level,
        }, status=201)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_equalizer_preset(request, user_id, preset_id):
    service = UserService()
    service.delete_equalizer_preset(preset_id, user_id)
    return JsonResponse({'success': True})
