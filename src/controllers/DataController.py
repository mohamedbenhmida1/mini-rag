from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseEnum

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # Convert MB to Bytes

    def validate_uploaded_file(self, file:UploadFile):
           if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
                return False,   ResponseEnum.FILE_TYPE_NOTE_SUPPORTED.value
           if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
                return False, ResponseEnum.FILE_SIZE_EXCEEDED
           return True, ResponseEnum.FILE_VALID.value
            