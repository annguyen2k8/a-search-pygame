from typing import Callable, List

from pygame import Clock


class Task:
    # interval -> milliseconds
    __interval: int
    __callback: Callable

    __elapsed: int
    __enabled: bool

    __killed: bool

    def __init__(self, interval: int, callback: Callable):
        self.__interval = interval
        self.__callback = callback

        self.__elapsed = 0
        self.__enabled = True
        self.__killed = False

    @property
    def interval(self) -> int:
        return self.__interval

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @property
    def disabled(self) -> bool:
        return not self.__enabled

    def enable(self):
        self.__enabled = True

    def disable(self):
        self.__enabled = False

    @property
    def killed(self) -> bool:
        return self.__killed

    def update(self, dt: int):
        if not self.enabled:
            return

        self.__elapsed += dt
        if self.__elapsed >= self.interval:
            self.__elapsed -= self.interval

            self.__callback()

    def reset(self):
        self.__elapsed = 0

    def kill(self):
        self.__killed = True


class Scheduler:
    __tasks: List[Task]
    __clock: Clock

    def __init__(self, clock: Clock):
        self.__tasks = []
        self.__clock = clock

    @property
    def tasks(self) -> List[Task]:
        return self.__tasks

    @property
    def clock(self) -> Clock:
        return self.__clock

    def register(self, callback: Callable, interval: int = 1000) -> Task:
        task = Task(interval, callback)

        self.__tasks.append(task)
        return task

    def update(self):
        dt = self.clock.get_time()
        for task in self.tasks[:]:
            if task.killed:
                self.tasks.remove(task)
            else:
                task.update(dt)
