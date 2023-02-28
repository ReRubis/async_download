import asyncio

import argparse

import aiohttp
from yarl import URL

from asydown.downmanager import DownloadManager

URL_LIST = [
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

STREAMS = 5
TEST_DIST_DIR = './downloads'

# download_manager --streams=5 --dest-dir=~/Downloads http://url.one http://url.two http://url.three http://url...


def parser_init():
    parser = argparse.ArgumentParser(
        prog='download_manager',
        description='Downloads Specified files',
    )

    parser.add_argument(
        '-S',
        '--streams',
        type=int,
        help='to set how many files you download at a time',
        default=STREAMS,
    )

    parser.add_argument(
        '-D',
        '--destdir',
        type=str,
        help='pass in the directery where the files will be sent',
        default=TEST_DIST_DIR,
    )

    parser.add_argument(
        'url_list',
        help='Activates storing in DB',
        type=str,
        default=URL_LIST,
        nargs='*',

    )

    return parser


def parse_args():
    parser = parser_init()
    return parser.parse_args()


async def main():
    args = parse_args()

    async with aiohttp.ClientSession() as session:
        async with DownloadManager(session) as down_manager:
            for url in args.url_list:
                await down_manager.add_file_to_download(url, args.destdir)

        await down_manager.run_downloading()


if __name__ == '__main__':
    asyncio.run(main())
    import time
    time.sleep(1)


# python ./asydown/main.py -S 1 -D './downloads2' 'https://m.media-amazon.com/images/I/51tUd26IhsL.jpg'
