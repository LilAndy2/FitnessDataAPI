"""
    This file contains the DataIngestor class, which is responsible for 
    loading and processing the dataset used in the application.
"""
from threading import Lock
import pandas as pd

class MetaSingleton(type):
    """
    A metaclass that implements the Singleton pattern.
    """
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        '''
            This method is called when the class is called
        '''
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(
                    MetaSingleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]

class DataIngestor(metaclass=MetaSingleton): # pylint: disable=too-few-public-methods
    """
        This class handles the ingestion and processing of the dataset.
        It loads data from a CSV file and provides methods for filtering
        and aggregating the information.
    """
    def __init__(self, csv_path: str):
        self.data = pd.read_csv(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity' +
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic ' +
            'activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity ' +
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic ' +
            'physical activity and engage in muscle-strengthening activities on 2 or more days ' +
            'a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity ' +
            'aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic' +
            ' activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more ' +
            'days a week',
        ]
