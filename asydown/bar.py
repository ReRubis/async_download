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

    def create_bar(self, prefix: str, total: int) -> ProgressBar:
        bar = ProgressBar(self, total, prefix)
        self.total_bar.total += total
        self._bars.append(bar)
        return bar

    def update_total_completed(self, completed: int, adjust: bool = True) -> None:
        self.total_bar.update_without_redraw(completed, adjust)

    def redraw(self) -> None:
        print(CLEAR_SCREEN_SEQUENCE)
        for bar in self.bars:
            bar.print()

    def remove_bar(self, bar_to_remove: ProgressBar) -> ProgressBar | None:
        try:
            self._bars.remove(bar_to_remove)
        except ValueError:
            return None

        return bar_to_remove

    @property
    def bars(self) -> list[ProgressBar]:
        return list(sorted(self._bars, key=lambda x: x.is_done, reverse=True)) + [self.total_bar]


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
        self.update_without_redraw(completed, adjust)
        self.progress_manager.update_total_completed(completed, adjust)

        update_time = datetime.now()

        if self.last_redraw_time:
            self.last_redraw_time_delta = update_time - self.last_redraw_time
            if self.last_redraw_time_delta.total_seconds() >= 0.5:
                self.progress_manager.redraw()
                self.last_redraw_time = datetime.now()

            if self.completed >= self.total:
                self.progress_manager.redraw()

            return None

        self.progress_manager.redraw()
        self.last_redraw_time = datetime.now()

    def update_without_redraw(self, completed: int, adjust: bool = True) -> None:
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

    def print(self) -> None:
        progress = int(self.completed / self.total * PBAR_WIDTH)
        if progress > PBAR_WIDTH:
            progress = PBAR_WIDTH

        bar = PBAR_CHAR * progress + ' ' * (PBAR_WIDTH - progress)

        percent = int(self.completed / self.total * 100)

        if self.last_completed_diff and self.last_update_time_delta:
            speed = round(
                self.last_completed_diff / self.last_update_time_delta.total_seconds()/MEGABYTE,
                2,
            )
        else:
            speed = ''

        if percent >= 100:
            percent = 100
            speed = 0.00

        if self.is_done:
            progress_str = f'{self.prefix:<30}: [{bar:>15}] {GREEN}{"Done":>20}{NO_COLOR}'
        else:
            progress_str = f'{self.prefix:<30}: [{bar:>15}] {speed:>8} mb/s {GREEN}{percent:>5}%{NO_COLOR}'

        print(progress_str, flush=True)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args) -> None:
        self.is_done = True
        self.progress_manager.redraw()
        await asyncio.sleep(2)
        self.progress_manager.remove_bar(self)
        self.progress_manager.redraw()


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
