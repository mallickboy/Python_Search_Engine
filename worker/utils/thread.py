import threading
from queue import Queue
from datetime import datetime
import os
from typing import Iterable, Any, List

from utils.log import log, Color

LOG_EXCEPTION = True

class ThreadPool:
    def __init__(self, task_function, num_workers: int = None, verbose: bool = False) -> None:
        self.task_queue = Queue()
        self.num_workers = num_workers or os.cpu_count() or 4
        self.task_function = task_function
        self.verbose = verbose
        self.threads: List[threading.Thread] = []
        self._stop_signal = object()
        self.results: List[Any] = []  # store results of tasks
        self._lock = threading.Lock()  # to make results thread-safe

    def worker(self, thread_id: int) -> None: # each threads runs this function
        while True:
            task = self.task_queue.get()
            if task is self._stop_signal:
                log(f" CPU <-- Thread {thread_id} exiting.", verbose=self.verbose)
                self.task_queue.task_done()
                break

            start_time = datetime.now()
            log(f" CPU --> Thread {thread_id} | Start | Task: {task}", verbose=self.verbose)

            try:
                result = self.task_function(task)
                
                with self._lock:    # Safely store result
                    self.results.append(result)
            except Exception as e:
                log(f" Thread {thread_id} | Error on task {task} -> {e}",
                         verbose=LOG_EXCEPTION, color=Color.RED)

            duration = (datetime.now() - start_time).total_seconds()
            log(f" --| Thread {thread_id} | Done in {duration:.2f}s | Task: {task}",
                     verbose=self.verbose)
            self.task_queue.task_done()

    def add_tasks(self, tasks: Iterable[Any]) -> None:
        for task in tasks:
            self.task_queue.put(task)

    def start(self) -> None:
        for i in range(self.num_workers):
            t = threading.Thread(
                target=self.worker, args=(i + 1,),
                daemon=True, name=f"Worker-{i+1}"
            )
            t.start()
            self.threads.append(t)

    def wait_completion(self) -> List[Any]:
        self.task_queue.join() # waits untill all tasks are marked with self.task_queue.task_done()
        for _ in self.threads:
            self.task_queue.put(self._stop_signal)
        for th in self.threads:
            th.join()
        log("<<All threads completed. All tasks done.>>\n",
                 verbose=self.verbose, color=Color.GREEN)
        return self.results
