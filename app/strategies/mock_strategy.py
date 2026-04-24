import uuid
from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """Offline, deterministic strategy for development and testing.
    Never calls any external API."""

    PLACEHOLDER_AUDIO_URL = (
        'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        task_id = f"mock-{uuid.uuid4().hex[:8]}"
        return GenerationResult(
            task_id=task_id,
            status='SUCCESS',
            audio_url=self.PLACEHOLDER_AUDIO_URL,
            title=request.title,
            duration='3:30',
            raw_data={
                'mock': True,
                'prompt': request.description,
                'mood': request.mood,
                'occasion': request.occasion,
                'singer_tone': request.singer_tone,
            },
        )

    def get_status(self, task_id: str) -> GenerationResult:
        return GenerationResult(
            task_id=task_id,
            status='SUCCESS',
            audio_url=self.PLACEHOLDER_AUDIO_URL,
            title='Mock Generated Song',
            duration='3:30',
            raw_data={'mock': True},
        )
