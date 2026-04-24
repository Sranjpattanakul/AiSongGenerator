from django.conf import settings
from .base import SongGeneratorStrategy


def get_generator() -> SongGeneratorStrategy:
    """Centralized strategy selection.
    Reads GENERATOR_STRATEGY from Django settings (set via environment variable).
    Returns MockSongGeneratorStrategy for 'mock', SunoSongGeneratorStrategy for 'suno'.
    """
    strategy = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()

    if strategy == 'suno':
        from .suno_strategy import SunoSongGeneratorStrategy
        return SunoSongGeneratorStrategy()

    from .mock_strategy import MockSongGeneratorStrategy
    return MockSongGeneratorStrategy()
