class GenerationError(Exception):
    pass


class GenerationAPIError(GenerationError):
    pass


class GenerationTimeoutError(GenerationError):
    pass
