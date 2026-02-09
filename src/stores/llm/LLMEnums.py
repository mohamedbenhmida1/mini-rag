from enum import Enum


class LLMEnum(Enum):
    """
    Enum for LLM types.
    """

    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSistANT = "assistant"
