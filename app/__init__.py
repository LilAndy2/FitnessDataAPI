import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging
import logging.handlers

# Create 'results' directory if it doesn't exist
if not os.path.exists('results'):
    os.mkdir('results')

# Initialize Flask app
webserver = Flask(__name__)

# webserver.task_runner.start()

# Initialize DataIngestor with dataset file
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

# Initialize job counter for tracking submitted jobs
webserver.job_counter = 1

# Set up logging with RotatingFileHandler
webserver.log = logging.getLogger(__name__)
webserver.log.setLevel(logging.INFO)

# Rotating log file: max size 300KB, keeps 5 backup files
rotating_file_handler = logging.handlers.RotatingFileHandler(
    'webserver.log', maxBytes=300000, backupCount=5
)

# Log format includes timestamp, module name, log level, and message
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)
rotating_file_handler.setFormatter(formatter)

# Add handler to logger
webserver.log.addHandler(rotating_file_handler)


# Initialize thread pool for task execution
webserver.tasks_runner = ThreadPool()