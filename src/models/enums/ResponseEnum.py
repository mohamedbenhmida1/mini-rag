from enum import Enum


class ResponseEnum(Enum):
    FILE_TYPE_NOTE_SUPPORTED = "file type not supported_abc"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_VALID = "file is valid"
    UPLOAD_SUCCESS = "file uploaded successfully"
    UPLOAD_FAILED = "file upload failed"
    PROCESSING_FAILED = "file processing failed"
    PROCESSING_SUCCESS = "file processed successfully"
    NO_FILES_ERROR = "no files found in the project"
    FILE_ID_ERROR = "no file found with this id"
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_DB_ERROR = "error while inserting into db"
    INSERT_INTO_DB_SUCCESS = "successfully inserted into db"
    INSERT_INTO_VECTORDB_ERROR = "error while inserting into vector db"
    INSERT_INTO_VECTORDB_SUCCESS = "successfully inserted into vector db"
    VECTORDB_COLLECTION_RETRIEVED = "vector db collection info retrieved"
    VECTORDB_SEARCH_ERROR = "error while searching vector db"
    VECTORDB_SEARCH_SUCCESS = "vector db search success"
    RAG_ANSWER_ERROR = "error while generating rag answer"
    RAG_ANSWER_SUCCESS = "rag answer generated successfully"
