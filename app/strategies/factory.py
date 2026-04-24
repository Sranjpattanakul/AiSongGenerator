from django.conf import settings
from .base import SongGeneratorStrategy


def get_generator(strategy: str = None) -> SongGeneratorStrategy:
    """Centralized strategy selection.
    Uses the provided strategy string, or falls back to GENERATOR_STRATEGY setting.
    Returns MockSongGeneratorStrategy for 'mock', SunoSongGeneratorStrategy for 'suno'.
    """
    if not strategy:
        strategy = getattr(settings, 'GENERATOR_STRATEGY', 'mock')
    strategy = strategy.lower()

    if strategy == 'suno':
        from .suno_strategy import SunoSongGeneratorStrategy
        return SunoSongGeneratorStrategy()

    from .mock_strategy import MockSongGeneratorStrategy
    return MockSongGeneratorStrategy()
