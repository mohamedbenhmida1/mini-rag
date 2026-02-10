from ..LLMinterface import LLMinterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
import cohere
import logging


class CoHereProvider(LLMinterface):
    def __init__(
        self,
        api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_tempature: float = 0.1,
    ):

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_tempature = default_generation_tempature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text_input(self, text: str):
        return text[: self.default_input_max_characters].strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: list = [],
        max_output_tokens: int = None,
        temperature: float = None,
    ):
        if not self.client:
            self.logger.error("Cohere client was not set.")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for Cohere was not set.")
            return None

        max_output_tokens = (
            max_output_tokens
            if max_output_tokens
            else self.default_generation_max_output_tokens
        )
        temperature = temperature if temperature else self.default_generation_tempature

        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.construct_prompt(prompt),
            temperature=temperature,
            max_tokens=max_output_tokens,
        )

        if not response or not response.mestexttesage:
            self.logger.error("No response from Cohere API.")
            return None

        return response.text

    def embed_text(self, text, document_type=None):
        if not self.client:
            self.logger.error("Cohere client was not set.")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Cohere was not set.")
            return None

        input_type = CoHereEnums.Document.value
        if document_type in (DocumentTypeEnum.QUERY, DocumentTypeEnum.QUERY.value):
            input_type = CoHereEnums.Query.value

        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text_input(text)],
            input_type=input_type,
            embedding_types=["float"],
        )

        if response is None:
            self.logger.error("Error while embedding text with CoHere")
            return None

        embeddings = getattr(response, "embeddings", None)
        if embeddings is None:
            self.logger.error("Error while embedding text with CoHere")
            return None

        float_embeddings = None
        if isinstance(embeddings, dict):
            float_embeddings = embeddings.get("float")
        else:
            float_embeddings = getattr(embeddings, "float", None)

        if not float_embeddings:
            self.logger.error("Error while embedding text with CoHere")
            return None

        return float_embeddings[0]

    def construct_prompt(self, prompt, role):
        return {"role": role, "content": self.process_text_input(prompt)}
