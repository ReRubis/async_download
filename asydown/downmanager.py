import asyncio
from pathlib import Path

import aiofiles

from asydown.bar import ProgressBarManager

BUFFER_SIZE = 2**10  # 1 KB


class DownloadManager:

    def __init__(self, session, streams):
        self.session = session
        self.tasks = []
        self.barmanager = ProgressBarManager()
        self.sem = asyncio.Semaphore(streams)

    async def add_file_to_download(self, file_url: str, dist_dir: str | Path):
        self.tasks.append(self.download_file(file_url, dist_dir))

    async def download_file(self, file_url: str, dist_dir: str | Path):
        """Download a file."""

        if isinstance(dist_dir, str):
            dist_dir = Path(dist_dir)

        async with self.session.get(file_url) as responce:
            file_name = file_url.rsplit('/', 1)[-1]
            dist_file_path = dist_dir / file_name
            current_file_size = 0
            file_size = int(responce.content_length)

            self.barmanager.adjust_total(file_size)

            async with (
                self.sem,
                self.barmanager.create_bar(file_name, file_size, add_total=False) as bar,
                aiofiles.open(dist_file_path, 'wb') as file,
            ):

                async for file_data in responce.content.iter_chunked(BUFFER_SIZE):
                    await file.write(file_data)
                    current_file_size += len(file_data)
                    bar.update_with_total(len(file_data))

    async def run_downloading(self):
        async with self.barmanager:
            async with self.barmanager.total_bar:
                await asyncio.gather(*self.tasks)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None
