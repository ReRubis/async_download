import asyncio
from pathlib import Path

import aiofiles
import aiohttp

# from asydown.bar import print_progress_bar

BUFFER_SIZE = 2**10  # 1 KB

TEST_FILE = 'https://w.wallhaven.cc/full/l8/wallhaven-l83o92.jpg'
TEST_FILE2 = 'https://linuxhint.com/wp-content/uploads/2022/08/Python-Asyncio-Gather-2.jpg'
TEST_DIST_DIR = './downloads'

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'


async def download_file(session: aiohttp.ClientSession, file_url: str, dist_dir: str | Path):
    """Download a file."""
    if isinstance(dist_dir, str):
        dist_dir = Path(dist_dir)

    async with session.get(file_url) as responce:
        file_name = file_url.rsplit('/', 1)[-1]
        dist_file_path = dist_dir / file_name
        current_file_size = 0

        async with aiofiles.open(dist_file_path, 'wb') as file:
            async for file_data in responce.content.iter_chunked(BUFFER_SIZE):
                await file.write(file_data)

                current_file_size = current_file_size + len(file_data)
                total = responce.content_length or 0
                # print_progress_bar(total, current_file_size, prefix=file_name)
                import time
                time.sleep(0.05)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        tasks.append(download_file(session, TEST_FILE, TEST_DIST_DIR))
        tasks.append(download_file(session, TEST_FILE2, TEST_DIST_DIR))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
