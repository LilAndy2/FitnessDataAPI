from queue import Queue
from threading import Thread, Event
import os
from app.data_ingestor import DataIngestor
import json

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
        self.job_status = {}

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
            return task['job_id']
        # If the thread pool has been shut down, log a warning
        else:
            self.logger.warning("Thread Pool has been shut down, tasks can no longer be added.")
            return -1


class TaskRunner(Thread):
    def __init__(self, thread_pool):
        '''
            Function to initialize the TaskRunner thread.
        '''
        Thread.__init__(self)
        self.thread_pool = thread_pool

    def run(self):
        '''
            Function to run a loop for the task runner, until the
            graceful_shutdown event is triggered.
        '''
        while not self.thread_pool.graceful_shutdown.is_set():
            try:
                task = self.thread_pool.tasks.get(timeout=1)
                self.process_task(task)
            except:
                continue

    def process_task(self, task):
        '''
            Function that simulates the work of a thread.
        '''
        self.thread_pool.logger.info(f"Processing task {task['job_id']}.")
        processor = TaskProcessor(self.thread_pool.data_ingestor)
        result = processor.compute_result(task)
        self.write_result(task['job_id'], result)
        self.thread_pool.logger.info(f"Task {task['job_id']} has been processed.")
        self.thread_pool.job_status[task['job_id']] = 'completed'

    def write_result(self, job_id, result):
        os.makedirs('./results', exist_ok=True)
        with open(f"./results/result-{job_id}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

class TaskProcessor:
    def __init__(self, data_ingestor):
        '''
            Function to initialize the TaskProcessor with the data ingestor
        '''
        self.data = data_ingestor.get_data()
        self.questions_best_is_min = data_ingestor.questions_best_is_min

    def compute_result(self, task):
        '''
            Function that calculates the result of the job based on the job type
        '''
        job_type = task['job_type']
        if job_type == 1:
            return self.states_mean(task)
        elif job_type == 2:
            return self.state_mean(task)
        elif job_type == 3:
            return self.best5_or_worst5(task, top=True)
        elif job_type == 4:
            return self.best5_or_worst5(task, top=False)
        elif job_type == 5:
            return self.global_mean(task)
        elif job_type == 6:
            return self.diff_from_mean(task)
        elif job_type == 7:
            return self.state_diff_from_mean(task)
        elif job_type == 8:
            return self.mean_by_category(task)
        elif job_type == 9:
            return self.state_mean_by_category(task)
        return {"error": "Invalid job type"}

    def states_mean(self, task):
        '''
            Groups the data by 'LocationDesc' and calculates the mean of 'Data_Value' for each group
            'LocationDesc' is the state name, therefore the result is the mean value for each state
        '''
        result = self.data[self.data['Question'] == task['question']].groupby('LocationsDesc')['Data_Value'].mean().to_dict()
        return dict(sorted(result.items(), key=lambda item: item[1]))
        
    def state_mean(self, task):
        '''
            Filters the data for the specified state & question and calculates the mean of 'Data_Value'
        '''
        result = self.data[(self.data['LocationDesc'] == task['state']) & (self.data['Question'] == task['question'])]['Data_Value'].mean()
        return {task['state']: result}
        
    def best5_or_worst5(self, task, top=True):
        '''
            best5:
            Calculates the mean of 'Data_Value' for each state for the specified question
            Sorts the results based on whether a lower value is better or not
            Returns the top 5 states

            worst5:
            Calculates the mean of 'Data_Value' for each state for the specified question
            Sorts the results based on whether a lower value is better or not
            Returns the last 5 states 
        '''
        best_is_min = task['question'] in self.questions_best_is_min
        result = self.data[self.data['Question'] == task['question']].groupby('LocationDesc')['Data_Value'].mean().to_dict()
        sorted_result = result.sort_values(ascending=best_is_min)
        return sorted_result.head(5).to_dict() if top else sorted_result.tail(5).to_dict()
        
    def global_mean(self, task):
        '''
            Calculates the mean of 'Data_Value' for the specified question
        '''
        return {'global_mean': self.data[self.data['Question'] == task['question']]['Data_Value'].mean()}
        
    def diff_from_mean(self, task):
        '''
            Calculates the difference between the global mean and the mean of 'Data_Value' 
            for each state for the specified question
        '''
        global_mean = self.global_mean(task)['global_mean']
        state_means = self.states_mean(task)
        return {state: global_mean - value for state, value in state_means.items()}

    def state_diff_from_mean(self, task):
        '''
            Calculates the difference between the global mean and the mean of 'Data_Value'
            for the specified state and question
        '''
        global_mean = self.global_mean(task)['global_mean']
        state_mean = self.state_mean(task)[task['state']]
        return {task['state']: global_mean - state_mean}

    def mean_by_category(self, task):            
        '''
            Groups the data by 'LocationDesc', 'StratificationCategory1' and 'Stratification1'
            (group by state, and by the stratification categories, stratifications within that state)
            Calculates the mean of 'Data_Value' for each group
        '''
        filtered_data = self.data[self.data['Question'] == task['question']]
        mean_values = filtered_data.groupby(('Category')['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean()
        return {str(state): value for state, value in mean_values.to_dict().items()}
        
    def state_mean_by_category(self, task):
        '''
            Groups the data by 'StratificationCategory1' and 'Stratification1' and
            calculates the mean of 'Data_Value' for the specified state and question
        '''
        filtered_data = self.data[(self.data['LocationDesc'] == task['state']) & (self.data['Question'] == task['question'])]
        mean_values = filtered_data.groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean()
        return {task['state']: {str(state): value for state, value in mean_values.to_dict().items()}}