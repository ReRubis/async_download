import asyncio
from pathlib import Path
import time
import aiofiles
import aiohttp

from asydown.bar import ProgressBarManager

CLEAR_LINE_SEQUENCE = '\033[2K'
GO_TO_BEGINNING_OF_LINE_SEQUENCE = '\033[1G'

PBAR_CHAR = '█'
PBAR_WIDTH = 20

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'

BUFFER_SIZE = 2**10  # 1 KB


TEST_DIST_DIR = './downloads'

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'


class DownManager:
    tasks = []

    def __init__(self, session):
        self.session = session

        self.barmanager = ProgressBarManager()
        self.total_bar = self.barmanager.get('TOTAL:', 0)

    async def add_download_task(self, file_url: str, dist_dir: str | Path):
        self.tasks.append(self.download_file(file_url, dist_dir))

    async def download_file(self, file_url: str, dist_dir: str | Path):
        """Download a file."""

        if isinstance(dist_dir, str):
            dist_dir = Path(dist_dir)

        async with self.session.get(file_url) as responce:
            file_name = file_url.rsplit('/', 1)[-1]
            dist_file_path = dist_dir / file_name
            current_file_size = 0

            self.total_bar.update_total_bar(int(responce.content_length))

            bar = self.barmanager.get(file_name, int(responce.content_length))

            async with aiofiles.open(dist_file_path, 'wb') as file:
                async for file_data in responce.content.iter_chunked(BUFFER_SIZE):
                    await file.write(file_data)

                    current_file_size = current_file_size + len(file_data)
                    bar.update(len(file_data), True)
                    self.total_bar.update(len(file_data), True)
                    # print_progress_bar(total, current_file_size, prefix=file_name)

    async def do_tasks(self):
        await asyncio.gather(*self.tasks)
