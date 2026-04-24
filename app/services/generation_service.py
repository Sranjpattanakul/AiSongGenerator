from app.strategies.factory import get_generator
from app.strategies.base import GenerationRequest
from app.models import GenerationJob, Song, Prompt


class GenerationService:
    def __init__(self):
        self.generator = get_generator()

    def start_generation(self, prompt: Prompt, song: Song) -> GenerationJob:
        request = GenerationRequest(
            title=prompt.title,
            description=prompt.description,
            mood=prompt.mood,
            occasion=prompt.occasion,
            singer_tone=prompt.singer_tone,
            requested_duration=prompt.requested_duration,
        )

        result = self.generator.generate(request)

        job, _ = GenerationJob.objects.update_or_create(
            song=song,
            defaults={
                'prompt': prompt,
                'task_id': result.task_id,
                'status': result.status,
            },
        )

        song.status = result.status
        if result.audio_url:
            song.audio_file_url = result.audio_url
        if result.image_url:
            song.image_url = result.image_url
        if result.title:
            song.title = result.title
        if result.duration:
            song.duration = result.duration
        song.save()

        return job

    def check_status(self, task_id: str) -> dict:
        result = self.generator.get_status(task_id)

        try:
            job = GenerationJob.objects.get(task_id=task_id)
            job.status = result.status
            job.save()

            song = job.song
            song.status = result.status
            if result.audio_url:
                song.audio_file_url = result.audio_url
            if result.image_url:
                song.image_url = result.image_url
            if result.duration:
                song.duration = result.duration
            song.save()
        except GenerationJob.DoesNotExist:
            pass

        return {
            'task_id': result.task_id,
            'status': result.status,
            'audio_url': result.audio_url,
            'image_url': result.image_url,
            'title': result.title,
            'duration': result.duration,
        }
