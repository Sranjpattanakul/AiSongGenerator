from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GenerationRequest:
    title: str
    description: str
    mood: str
    occasion: str
    singer_tone: str
    requested_duration: str = '3:00'


@dataclass
class GenerationResult:
    task_id: str
    status: str
    audio_url: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[str] = None
    raw_data: Optional[dict] = field(default_factory=dict)


class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Submit a song generation request and return a result with a task_id."""

    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult:
        """Poll the status of a previously submitted generation task."""
