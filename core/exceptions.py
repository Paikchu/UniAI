"""Custom exception classes"""


class UniAIException(Exception):
    """Base exception class for UniAI project"""

    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ModelNotSupportedException(UniAIException):
    """Model not supported exception"""

    def __init__(self, model: str):
        super().__init__(f"Model '{model}' is not supported", 400)


class SceneNotFoundException(UniAIException):
    """Scene not found exception"""

    def __init__(self, scene_id: str):
        super().__init__(f"Scene '{scene_id}' not found", 400)


class ProviderException(UniAIException):
    """AI provider exception"""

    def __init__(self, provider: str, message: str):
        super().__init__(f"Provider '{provider}' error: {message}", 500)
