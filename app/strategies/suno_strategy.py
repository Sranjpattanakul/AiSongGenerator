import requests
from django.conf import settings
from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult
from .exceptions import GenerationAPIError


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """Calls the SunoApi.org external service to generate songs.
    Requires SUNO_API_KEY to be set in the environment."""

    BASE_URL = 'https://api.sunoapi.org/api/v1'

    # Maps Suno API status values to our internal GenerationStatus values
    STATUS_MAP = {
        'PENDING': 'QUEUED',
        'TEXT_SUCCESS': 'GENERATING',
        'FIRST_SUCCESS': 'GENERATING',
        'SUCCESS': 'SUCCESS',
        'FAILED': 'FAILED',
    }

    def __init__(self):
        self.api_key = settings.SUNO_API_KEY
        if not self.api_key:
            raise GenerationAPIError(
                'SUNO_API_KEY is not set. Add it to your .env file.'
            )
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    @staticmethod
    def _duration_to_seconds(duration_str: str) -> int:
        parts = duration_str.split(':')
        return int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 180

    TONE_LABELS = {
        'MALE': 'male vocalist',
        'FEMALE': 'female vocalist',
        'CHILD': 'child singer',
        'NEUTRAL': 'versatile vocalist',
    }

    def generate(self, request: GenerationRequest) -> GenerationResult:
        tone = self.TONE_LABELS.get(request.singer_tone.upper(), 'vocalist')
        prompt = (
            f"A {request.mood.lower()} song for a {request.occasion.lower()} "
            f"performed by a {tone}. "
            f"The song is entirely about: {request.description}. "
            f"Every verse, chorus, and bridge must stay on this theme."
        )
        style_tags = f"{request.mood.lower()}, {request.occasion.lower()}, {request.singer_tone.lower()} voice"

        callback_url = getattr(settings, 'SUNO_CALLBACK_URL', 'https://httpbin.org/post')
        payload = {
            'prompt': prompt,
            'title': request.title,
            'style': style_tags,
            'instrumental': False,
            'model': 'V4',
            'customMode': False,
            'callBackUrl': callback_url,
            'duration': self._duration_to_seconds(request.requested_duration),
        }

        try:
            response = requests.post(
                f'{self.BASE_URL}/generate',
                json=payload,
                headers=self.headers,
                timeout=30,
            )
        except requests.RequestException as exc:
            raise GenerationAPIError(f'Network error contacting Suno API: {exc}') from exc

        if not response.ok:
            raise GenerationAPIError(
                f'Suno API returned {response.status_code}: {response.text}'
            )

        data = response.json()
        print(f"[Suno] generate → code={data.get('code')} msg={data.get('msg')} taskId={data.get('data', {}).get('taskId') if isinstance(data.get('data'), dict) else None}")

        nested = data.get('data') or {}
        task_id = (
            data.get('taskId') or data.get('task_id') or
            (nested.get('taskId') if isinstance(nested, dict) else None) or
            (nested.get('task_id') if isinstance(nested, dict) else None) or
            ''
        )

        if not task_id:
            raise GenerationAPIError(f'Suno API returned no task ID. Full response: {data}')

        return GenerationResult(
            task_id=task_id,
            status='QUEUED',
            raw_data=data,
        )

    def get_status(self, task_id: str) -> GenerationResult:
        try:
            response = requests.get(
                f'{self.BASE_URL}/generate/record-info',
                params={'taskId': task_id},
                headers=self.headers,
                timeout=30,
            )
        except requests.RequestException as exc:
            raise GenerationAPIError(f'Network error contacting Suno API: {exc}') from exc

        if not response.ok:
            raise GenerationAPIError(
                f'Suno API returned {response.status_code}: {response.text}'
            )

        data = response.json()
        inner = data.get('data') or {}
        if isinstance(inner, dict):
            suno_status = inner.get('status') or data.get('status', 'PENDING')
            print(f"[Suno] status → taskId={task_id[:12]}... status={suno_status}")
            response_data = inner.get('response') or {}
            if isinstance(response_data, dict):
                clips = response_data.get('sunoData') or response_data.get('clips') or []
            else:
                clips = inner.get('clips') or inner.get('sunoData') or data.get('clips') or []
        else:
            suno_status = data.get('status', 'PENDING')
            clips = data.get('clips') or []

        our_status = self.STATUS_MAP.get(suno_status, 'QUEUED')

        audio_url = None
        image_url = None
        title = None
        duration = None

        if isinstance(clips, list) and len(clips) > 0:
            clip = clips[0]
            audio_url = clip.get('sourceAudioUrl') or clip.get('audioUrl') or clip.get('audio_url')
            image_url = clip.get('sourceImageUrl') or clip.get('imageUrl') or clip.get('image_url')
            title = clip.get('title')
            raw_duration = clip.get('duration')
            if raw_duration is not None:
                total_seconds = int(float(raw_duration))
                duration = f"{total_seconds // 60}:{total_seconds % 60:02d}"

        return GenerationResult(
            task_id=task_id,
            status=our_status,
            audio_url=audio_url,
            image_url=image_url,
            title=title,
            duration=duration,
            raw_data=data,
        )
