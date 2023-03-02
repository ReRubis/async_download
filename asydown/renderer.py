from __future__ import annotations
import asyncio
from datetime import datetime, timedelta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from asydown.bar import ProgressBar


CLEAR_LINE_SEQUENCE = '\033[2K'
GO_TO_BEGINNING_OF_LINE_SEQUENCE = '\033[1G'

PBAR_CHAR = '█'
PBAR_WIDTH = 20
GREEN = '\033[0;32m'
NO_COLOR = '\033[0m'

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'

MEGABYTE = 2**20


class DefaultRenderer():
    def __init__(self, progress_bars: list[ProgressBar], total_bar: ProgressBar, fps: int = 60):
        self.bars = progress_bars
        self.active = False
        self.fps = fps
        self.total_bar = total_bar

    def redraw(self) -> None:
        print(CLEAR_SCREEN_SEQUENCE)

        for bar in self.bars:
            self.print(bar)
        self.print(self.total_bar)

    def print(self, bar: ProgressBar) -> None:
        progress = int(bar.completed / bar.total * PBAR_WIDTH)
        if progress > PBAR_WIDTH:
            progress = PBAR_WIDTH

        bar_string = PBAR_CHAR * progress + ' ' * (PBAR_WIDTH - progress)

        percent = int(bar.completed / bar.total * 100)

        if bar.last_completed_diff and bar.last_update_time_delta:
            speed = round(
                bar.last_completed_diff / bar.last_update_time_delta.total_seconds()/MEGABYTE,
                2,
            )
        else:
            speed = ''

        if percent >= 100:
            percent = 100
            speed = 0.00

        if bar.is_done:
            progress_str = f'{bar.prefix:<30}: [{bar_string:>15}] {GREEN}{"Done":>20}{NO_COLOR}'
        else:
            progress_str = f'{bar.prefix:<30}: [{bar_string:>15}] {speed:>8} mb/s {GREEN}{percent:>5}%{NO_COLOR}'

        print(progress_str, flush=True)

    async def run_loop(self):
        await asyncio.sleep(0.5)

        ts = None
        period = timedelta(milliseconds=1000/self.fps)
        self.active = True

        while self.active:
            if not ts or ((datetime.now() - ts) >= period):
                self.redraw()
                ts = datetime.now()
            await asyncio.sleep(period.total_seconds()/3)

    def stop_loop(self):
        self.active = False
