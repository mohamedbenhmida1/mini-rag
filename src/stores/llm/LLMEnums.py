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


class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    Document = "search_document"
    Query = "search_query"


class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"
