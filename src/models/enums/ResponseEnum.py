from enum import Enum
class ResponseEnum(Enum):
    FILE_TYPE_NOTE_SUPPORTED="file type not supported_abc"
    FILE_SIZE_EXCEEDED="file size exceeded"
    FILE_VALID="file is valid"
    UPLOAD_SUCCESS="file uploaded successfully"
    UPLOAD_FAILED="file upload failed"
    PROCESSING_FAILED="file processing failed"
    PROCESSING_SUCCESS="file processed successfully"
