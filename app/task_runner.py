from queue import Queue
from threading import Thread, Event
import time
import os
from app.data_ingestor import DataIngestor

class ThreadPool:
    def __init__(self, logger=None):
        '''
            Function to initialize the Thread Pool with the number of threads
            specified in the environmental variable TP_NUM_OF_THREADS.
        '''
        self.num_threads = int(os.getenv("TP_NUM_OF_THREADS", os.cpu_count()))

        # Event to signal the Thread Pool to shutdown.
        self.graceful_shutdown = Event()

        # Queue of tasks that wait to be executed
        self.tasks = Queue()

        # List of thread workers
        self.workers = []

        # Dictionary to map the job_id to the task status
        self.job_id_to_task = {}

        self.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
        self.logger = logger

        # Logging the thread pool's initialisation
        self.logger.info(f"Thread pool has been initialised with {self.num_threads} threads.")
        for i in range(self.num_threads):
            self.workers.append(TaskRunner(self))
            self.workers[i].start()
            self.logger.info(f"Thread {i} started its job.")

    def shutdown(self):
        '''
            Function to trigger the graceful_shutdown even and stop the Thread Pool
        '''
        if not self.graceful_shutdown.is_set():
            # Sets the graceful_shutdown event and logs the thread pool's shutdown
            self.graceful_shutdown.set()
            self.logger.info("Thread Pool has been shut down.")

            for thread in self.workers:
                thread.join(timeout=10)
                self.logger.info(f"Thread {thread.ident} joined.")
    
    def add_task(self, task):
        '''
            Function to add a task to the queue.
        '''
        # First check if the thread pool hasn't already been shut down
        if not self.graceful_shutdown.is_set():
            self.tasks.put(task)
            self.logger.info(f"Task {task['job_id']} added to the queue.")
        else:
            self.logger.info("Thread Pool has been shut down, tasks can no longer be added.")
        
        return -1


class TaskRunner(Thread):
    def __init__(self, thread_pool):
        '''
            Function to initialize the TaskRunner thread.
        '''
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self.current_task = None

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass
