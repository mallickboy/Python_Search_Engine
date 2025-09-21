import threading
from queue import Queue
from datetime import datetime
import time
import os
from enum import Enum
from colorama import Fore, Style, init
from typing import Iterable, Any

init(autoreset=True)  # Initializing colorama for cross-platform support

class Color(Enum):
    """
    Enum for terminal text colors.

    Uses colorama's Fore constants to enable type-safe usage
    of color values across the application.
    """

    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW

class ThreadPool:
    def __init__(self, task_function, num_workers: int=None, verbose: bool=False) -> None:
        self.task_queue = Queue()
        self.num_workers = num_workers or os.cpu_count() or 4
        self.task_function = task_function
        self.verbose = verbose
        self.threads = []
        self._stop_signal = object()

    def log(self, msg: str, verbose: bool = False, color: Color = Color.CYAN) -> None:
        """
        Print a timestamped log message if verbose is enabled.

        Args:
            msg (str): The message to log.
            verbose (bool): Whether to print the log.
            color (Color): Color for the timestamp and label (default: Color.CYAN).
        """
        if verbose:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"{color.value}[{timestamp}] [log]{Style.RESET_ALL} {msg}"
            )  # colorize timestamp and log label

    def worker(self, thread_id: int) -> None:
        while True:
            task = self.task_queue.get()
            if task is self._stop_signal:
                self.log(f" CPU <-- Thread {thread_id} exiting.", verbose=self.verbose)
                self.task_queue.task_done()
                break

            start_time = datetime.now()
            self.log(f" CPU --> Thread {thread_id} | Start | Task: {task}", verbose=self.verbose)
            
            try:
                self.task_function(task)
            except Exception as e:
                self.log(f" Thread {thread_id} | Error on task {task} -> {e}", verbose=True, color=Color.RED)

            duration = (datetime.now() - start_time).total_seconds()
            self.log(f" --| Thread {thread_id} | Done in {duration:.2f}s | Task: {task}", verbose=self.verbose)
            self.task_queue.task_done()

    def add_tasks(self, tasks: Iterable[Any]) -> None:
        for task in tasks:
            self.task_queue.put(task)

    def start(self) -> None:
        for i in range(self.num_workers):
            t = threading.Thread(
                target=self.worker, args=(i + 1,), daemon=True, name=f"Worker-{i+1}"
            )
            t.start()
            self.threads.append(t)

    def wait_completion(self) -> None:
        self.task_queue.join()
        for _ in self.threads:
            self.task_queue.put(self._stop_signal)
        for t in self.threads:
            t.join()
        self.log("<<All threads completed. All tasks done.>>\n", verbose= self.verbose, color=Color.GREEN
                 )