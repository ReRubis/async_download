from pydantic import BaseModel


class FileToDownload(BaseModel):
    something: str
    ...
