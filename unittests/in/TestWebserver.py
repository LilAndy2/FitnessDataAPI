'''
    Module for testing the webserver
'''
import unittest
import json
from time import sleep
import requests


class TestWebserver(unittest.TestCase):
    '''
        Class to test the webserver with different test cases
    '''

    def test_1_states_mean(self):
        '''
            Test case to check the mean of all states
        '''
        self.helper_for_tests(1)

    def test_2_state_mean(self):
        '''
            Test case to check the mean of a specific state
        '''
        self.helper_for_tests(2)

    def test_3_best5(self):
        '''
            Test case to check the best 5 states
        '''
        self.helper_for_tests(3)

    def test_4_worst5(self):
        '''
            Test case to check the worst 5 states
        '''
        self.helper_for_tests(4)

    def test_5_global_mean(self):
        '''
            Test case to check the global mean
        '''
        self.helper_for_tests(5)

    def test_6_diff_from_mean(self):
        '''
            Test case to check the difference of each state from the global mean
        '''
        self.helper_for_tests(6)

    def test_7_state_diff_from_mean(self):
        '''
            Test case to check the difference of a specific state from the global mean
        '''
        self.helper_for_tests(7)

    def test_8_mean_by_category(self):
        '''
            Test case to check the mean of all states by category and stratifications
        '''
        self.helper_for_tests(8)

    def test_9_state_mean_by_category(self):
        '''
            Test case to check the mean of a specific state by category and stratifications
        '''
        self.helper_for_tests(9)

    def test_z_ungraceful_shutdown(self):
        '''
            Test case to check the shutdown of the ThreadPool
        '''

        # setup for sending the request
        endpoint = "http://127.0.0.1:5000/api/graceful_shutdown"
        res = requests.get(endpoint, timeout=50)

        sleep(2.5)  # wait for the ThreadPool to shut down

        # send another request to check if the ThreadPool shut down
        endpoint = "http://127.0.0.1:5000/api/best5"
        res = requests.post(
            endpoint, json={"question": "What is the best state?"}, timeout=50)
        res_data = res.json()
        self.assertEqual(res_data["status"], "error")

    def test_z_get_jobs(self):
        '''
            Test case to check the status of all jobs
        '''
        endpoint = "http://127.0.0.1:5000/api/jobs"
        # this test runs after the other tests, so the expected result is that all jobs are done
        expected_result = []
        for job_id in range(1, 10):
            expected_result.append({str(job_id): "done"})

        res = requests.get(endpoint, timeout=5)
        res = res.json()["data"]

        self.assertEqual(res, expected_result)

    def helper_for_tests(self, test_number):
        '''
            Helper function to run the tests
        '''
        # Read input data from file
        with open(f'unittests/in-{test_number}.json', 'r', encoding='utf-8') as infile:
            test = json.load(infile)

        # setup for sending the request
        endpoint = "http://127.0.0.1:5000/api/" + test["route"]
        req_data = {"question": test["question"]}

        # if the test contains "state", add it to the request
        if "state" in test:
            req_data["state"] = test["state"]

        # get the job_id
        res = requests.post(endpoint, json=req_data, timeout=5)
        job_id = res.json()
        job_id = job_id.get("job_id", None)

        # the tests are not allowed to run multiple times
        # due to the nature of the shutdown test
        if job_id is None or res.status_code != 200:
            self.fail("Multiple calls of tests is not permitted")

        current = 0

        while True:
            res = requests.get(
                "http://127.0.0.1:5000/api/get_results/" + str(job_id), timeout=5)
            res_data = res.json()

            if res_data["status"] == "done":
                break

            if res_data["status"] == "running":
                sleep(0.2)
                current += 0.2

            elif current > 1.5:
                self.fail("Timeout")

            else:
                self.fail("Error")

        res_data = res_data["data"]

        # Write result to output file
        with open(f'unittests/out-{test_number}.json', 'r', encoding='utf-8') as outfile:
            # read the expected result
            expected = json.load(outfile)
            # compare it with the actual result
            self.assertEqual(res_data, expected)


if __name__ == '__main__':
    unittest.main()
