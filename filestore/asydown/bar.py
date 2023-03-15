from __future__ import annotations
import asyncio
import time
from datetime import datetime, timedelta


CLEAR_LINE_SEQUENCE = '\033[2K'
GO_TO_BEGINNING_OF_LINE_SEQUENCE = '\033[1G'

PBAR_CHAR = '█'
PBAR_WIDTH = 20
GREEN = '\033[0;32m'
NO_COLOR = '\033[0m'

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'

MEGABYTE = 2**20


class ProgressBarManager:
    def __init__(self) -> None:
        self.total_bar = ProgressBar(self, total=0, prefix='Total')
        self._bars = []

    def adjust_total(self, add_total: int) -> int:
        self.total_bar.total += add_total
        return self.total_bar.total

    def create_bar(self, prefix: str, total: int, add_total: bool = True) -> ProgressBar:
        bar = ProgressBar(self, total, prefix)

        if add_total:
            self.total_bar.total += total

        self._bars.append(bar)
        return bar

    def update_total_completed(self, completed: int, adjust: bool = True) -> None:
        self.total_bar.update(completed, adjust)

    def remove_bar(self, bar_to_remove: ProgressBar) -> ProgressBar | None:
        try:
            self._bars.remove(bar_to_remove)
        except ValueError:
            return None

        return bar_to_remove

    # async def __aenter__(self):
    #     self._rendering_task = asyncio.create_task(self.renderer.run_loop())
    #     return self

    # async def __aexit__(self, *args) -> None:
    #     self.renderer.stop_loop()
    #     await self._rendering_task

    # @property
    # def bars(self) -> list[ProgressBar]:
    #     return list(sorted(self._bars, key=lambda x: x.is_done, reverse=True)) + [self.total_bar]


class ProgressBar:
    def __init__(self, manager: ProgressBarManager, total: int, prefix: str = ''):
        self.progress_manager = manager
        self.completed = 0
        self.total = total
        self.prefix = prefix

        self.is_done: bool = False

        self.last_update_time: datetime | None = None
        self.last_update_time_delta: timedelta | None = None
        self.last_completed_diff: int | None = None

        self.last_redraw_time: datetime | None = None
        self.last_redraw_time_delta: timedelta | None = None

    def update(self, completed: int, adjust: bool = True) -> None:
        old_completed_value = self.completed

        if adjust:
            self.completed += completed
        else:
            self.completed = completed

        new_update_time = datetime.now()
        if self.last_update_time:
            self.last_update_time_delta = new_update_time - self.last_update_time
            self.last_completed_diff = self.completed - old_completed_value

        self.last_update_time = new_update_time

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args) -> None:
        self.is_done = True
        # await asyncio.sleep(2)
        self.progress_manager.remove_bar(self)
        self.progress_manager.update_total_completed(1)


def main(end, start=0):
    manager = ProgressBarManager()
    bar1 = manager.create_bar('bar1', 100)
    bar2 = manager.create_bar('bar2', 3000)
    bar3 = manager.create_bar('bar3', 3000)
    for i in range(start, end+1):
        time.sleep(0.1)
        bar1.update(5, True)
        bar2.update(500, True)
        bar3.update(123, True)


if __name__ == '__main__':
    main(100, 0)
