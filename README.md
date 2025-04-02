
# Fitness Data API

This project implements a Python web server that analyzes U.S. nutrition, physical activity, and obesity data (2011-2022) from a CSV dataset. It provides state-level statistics via API endpoints, computing averages, rankings, and deviations from the mean to highlight public health trends.

## Getting Started

Before running the project, it's important to ensure that your development environment is properly set up. This includes installing the necessary dependencies and configuring a virtual environment for isolated package management. The following sections will guide you through the setup process, ensuring that you can run the server and execute tests seamlessly.

### Prerequisites
This project requires the following dependencies:
- **Programming Language**: Python
- **Package Manager**: Pip

### Instalation
In order to install the required dependencies, use:
```
> pip install -r requirements.txt
```

The project has been tested using a virtual environment. 

Use one shell to activate the virtual environment and start the server:
```
> source venv/bin/activate
> make run_server
```

In a different shell, activate the virtual environment and run the automated tests:
```
> source venv/bin/activate
> make run_tests
```

## Features
- Endpoints to validate multiple functionalities
- Automated testing of the API endpoints
- Validation of expected outputs
- Job status verification

## Implementation
The server uses multithreading and a thread pool to efficiently handle incoming requests. Tasks are placed in a queue and executed by worker threads, ensuring concurrent processing and improved performance.

### Thread Pool Architecture
- The ThreadPool class initializes a fixed number of worker threads (defaulting to the number of CPU cores or a specified environment variable `TP_NUM_OF_THREADS`).
- Incoming tasks are added to a queue and processed asynchronously by worker threads.
- Each worker thread, implemented via the TaskRunner class, continuously retrieves tasks from the queue and executes them.
- A graceful shutdown mechanism is implemented using an event flag, ensuring that threads complete their tasks before terminating.

### Task Execution Flow
1. Adding a Task
- When a new request is received, it is assigned a **job ID** and pushed into the task queue.
- The job ID is tracked in a dictionary to monitor progress.

2. Processing a Task
- Worker threads retrieve tasks from the queue and process them using the **TaskProcessor** class.
- Task execution involves filtering and computing statistics based on predefined operations.
- Results are stored in JSON files inside the `./results` directory.

3. Supported Job Types
- The server can compute various statistics, including:
    - Mean values per state (`states_mean`)
    - Best and worst 5 states (`best5`, `worst5`)
    - Global mean and deviations (`global_mean`, `diff_from_mean`)
    - State-specific statistics (`state_mean`, `state_diff_from_mean`)
    - Mean values by category (`mean_by_category`, `state_mean_by_category`)

This implementation ensures scalability and optimized performance for handling multiple requests simultaneously.
