import asyncio
from pathlib import Path

import aiofiles
import aiohttp

from asydown.downmanager import DownloadManager

url_list = [
    'https://w.wallhaven.cc/full/l8/wallhaven-l83o92.jpg',
    'https://linuxhint.com/wp-content/uploads/2022/08/Python-Asyncio-Gather-2.jpg',
    'https://w.wallhaven.cc/full/1p/wallhaven-1p398w.jpg',
    'https://w.wallhaven.cc/full/57/wallhaven-57o9j5.png',
    'https://w.wallhaven.cc/full/y8/wallhaven-y8lqo7.jpg',
    'https://miro.medium.com/max/1400/1*eMUTAcY2t1FRG8TgFa0h4A.png',
    'https://miro.medium.com/max/1400/1*lic9mXPkq0CNNm4g6StxXQ.png',
    'https://www.programmingfunda.com/wp-content/uploads/2022/01/Context-Manager-in-Python.png',
    'https://m.media-amazon.com/images/I/51tUd26IhsL.jpg',
]

TEST_DIST_DIR = './downloads'


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
        async with DownloadManager(session) as down_manager:
            for url in url_list:
                await down_manager.add_file_to_download(url, TEST_DIST_DIR)

        await down_manager.run_downloading()


if __name__ == '__main__':
    asyncio.run(main())
    import time
    time.sleep(1)
