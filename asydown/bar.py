import time

CLEAR_LINE_SEQUENCE = '\033[2K'
GO_TO_BEGINNING_OF_LINE_SEQUENCE = '\033[1G'

PBAR_CHAR = '█'
PBAR_WIDTH = 20
GREEN = '\033[0;32m'
NO_COLOR = '\033[0m'

CLEAR_SCREEN_SEQUENCE = '\033[2J\033[1;1H'


class ProgressBarManager:
    list_of_bars = []

    def get(self, prefix: str, total: int) -> 'ProgressBar':
        bar = ProgressBar(self, total, prefix)
        self.list_of_bars.append(bar)
        return bar

    def update_total_bar(self, total: int) -> None:
        for bar in self.list_of_bars:
            if bar.prefix == 'TOTAL:':
                bar.update_total_bar(total)

    def print_bars(self) -> None:
        print(CLEAR_SCREEN_SEQUENCE)
        for bar in self.list_of_bars:
            bar.print()


class ProgressBar:
    def __init__(self, manager: ProgressBarManager, total: int, prefix: str = ''):
        self.progress_manager = manager
        self.total = 0
        self.completed = 0
        self.progress = 0
        self.total = total
        self.prefix = prefix

    def update(self, completed: int, adjust: bool = None) -> None:
        if adjust:
            self.completed = self.completed + completed

        else:
            self.completed = completed

        if self.completed >= self.total:
            self.completed = self.total

        self.progress = int(self.completed / self.total * PBAR_WIDTH)

        if self.prefix != 'TOTAL:':
            self.progress_manager.print_bars()

    def update_total_bar(self, total: int) -> None:
        self.total = self.total + total

    def print(self) -> None:

        progress_str = '{clear_screen}{prefix:<30}: [{progress_bar:>15}] {green}{percent:>5}% {no_color}\n'.format(
            clear_screen=CLEAR_LINE_SEQUENCE + GO_TO_BEGINNING_OF_LINE_SEQUENCE,
            prefix=self.prefix,
            progress_bar=PBAR_CHAR * self.progress +
            ' ' * (PBAR_WIDTH - self.progress),
            green=GREEN,
            percent=int(self.completed / self.total * 100),
            no_color=NO_COLOR
        )

        print(progress_str, end='', flush=True)


def main(end, start=0):
    manager = ProgressBarManager()
    bar1 = manager.get('bar1', 100)
    bar2 = manager.get('bar2', 3000)
    bar3 = manager.get('bar3', 3000)
    for i in range(start, end+1):
        time.sleep(0.1)

        bar1.update(5, True)
        bar2.update(500, True)
        bar3.update(123, True)


if __name__ == '__main__':
    main(100, 0)
