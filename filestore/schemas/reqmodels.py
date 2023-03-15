from pydantic import BaseModel


class FileToUpload(BaseModel):
    id: int
    user_id: int
    file_location: str
    privacy_level: str
    created_at: str
    removed_at: str
