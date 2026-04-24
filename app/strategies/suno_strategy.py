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

    def generate(self, request: GenerationRequest) -> GenerationResult:
        prompt = (
            f"{request.mood.lower()} {request.occasion.lower()} song. "
            f"{request.description}"
        )
        payload = {
            'prompt': prompt,
            'title': request.title,
            'style': f"{request.mood.lower()} {request.singer_tone.lower()}",
            'make_instrumental': False,
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
        task_id = data.get('taskId') or data.get('task_id', '')

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
        suno_status = data.get('status', 'PENDING')
        our_status = self.STATUS_MAP.get(suno_status, 'QUEUED')

        audio_url = None
        image_url = None
        title = None
        duration = None

        clips = data.get('clips') or data.get('data', [])
        if clips and isinstance(clips, list) and len(clips) > 0:
            clip = clips[0]
            audio_url = clip.get('audio_url')
            image_url = clip.get('image_url')
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
