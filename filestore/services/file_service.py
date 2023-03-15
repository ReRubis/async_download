import subprocess
import asyncio
from fastapi import UploadFile, File
from filestore.utils.repository import FileRepository
from filestore.utils.db_session import session_init
from fastapi import Depends


class FileDownloadService():
    def __init__(self, passed_repository: FileRepository, directory: str = 'downloads'):
        self.directory = directory
        self.repository = passed_repository

    def download_by_url(self, url: str) -> str:
        """Download a file from a link, returns location on disk"""
        self.directory = 'downloads'
        process = subprocess.Popen(
            ['python',
                './filestore/asydown/asydown.py',
                '--streams=1',
                f'--destdir={self.directory}',
                url],
            stdout=subprocess.PIPE
        )

        for line in process.stdout:
            print(line.decode().strip())
        return self.directory

    async def upload(self, stream: File) -> str:
        """Upload a file, returns location on disk"""
        with open(stream.filename, "wb") as buffer:
            buffer.write(await stream.read())

        self.repository.save_file()

        return f'{self.directory}/{stream.filename}'


class FileStorageService():
    def __init__(self, passed_repository: FileRepository, directory: str = 'downloads'):
        self.directory = directory
        self.repository = passed_repository

    def get(self, id: int):
        """Return file's with certain id location on disk"""
        ...

    def get_file_list(self, user_id: int):
        """Returns a list of file locations on disk corresponding to user"""
        ...

    def add_file(self, file_path: str):
        ...


class FileAppService():
    def __init__(self):
        self.down_service = FileDownloadService(self.build_file_repository)
        self.store_service = FileStorageService(self.build_file_repository)

    @property
    def build_file_repository(self, session=Depends(session_init)):
        return FileRepository(session)
