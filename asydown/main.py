import asyncio
from pathlib import Path

import aiofiles
import aiohttp

from asydown.downmanager import DownManager
# from asydown.bar import print_progress_bar

BUFFER_SIZE = 2**10  # 1 KB

TEST_FILE = 'https://w.wallhaven.cc/full/l8/wallhaven-l83o92.jpg'
TEST_FILE2 = 'https://linuxhint.com/wp-content/uploads/2022/08/Python-Asyncio-Gather-2.jpg'
TEST_FILE3 = 'https://w.wallhaven.cc/full/1p/wallhaven-1p398w.jpg'
TEST_FILE4 = 'https://w.wallhaven.cc/full/57/wallhaven-57o9j5.png'
TEST_DIST_DIR = './downloads'

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'


# async def download_file(session: aiohttp.ClientSession, file_url: str, dist_dir: str | Path):
#     """Download a file."""
#     if isinstance(dist_dir, str):
#         dist_dir = Path(dist_dir)

#     async with session.get(file_url) as responce:
#         file_name = file_url.rsplit('/', 1)[-1]
#         dist_file_path = dist_dir / file_name
#         current_file_size = 0

#         async with aiofiles.open(dist_file_path, 'wb') as file:
#             async for file_data in responce.content.iter_chunked(BUFFER_SIZE):
#                 await file.write(file_data)

#                 current_file_size = current_file_size + len(file_data)
#                 total = responce.content_length or 0
#                 # print_progress_bar(total, current_file_size, prefix=file_name)


async def main():
    async with aiohttp.ClientSession() as session:
        down_manager = DownManager(session)
        await down_manager.add_download_task(TEST_FILE, TEST_DIST_DIR)
        await down_manager.add_download_task(TEST_FILE2, TEST_DIST_DIR)
        await down_manager.add_download_task(TEST_FILE3, TEST_DIST_DIR)
        await down_manager.add_download_task(TEST_FILE4, TEST_DIST_DIR)
        await down_manager.do_tasks()


if __name__ == '__main__':
    asyncio.run(main())
