'''
    Module for testing the webserver.
'''
import unittest
import json
import time
import requests

class TestWebserver(unittest.TestCase):
    '''
        Class for testing the web server.
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Function that sets up the test case.
        '''
        cls.base_url = 'http://127.0.0.1:5000/api/'

    def test_1_states_mean(self):
        '''
            Test the states_mean endpoint.
        '''
        self.run_test_case(1)

    def test_2_state_mean(self):
        '''
            Test the state_mean endpoint.
        '''
        self.run_test_case(2)
    
    def test_3_best5(self):
        '''
            Test the best5 endpoint.
        '''
        self.run_test_case(3)
    
    def test_4_worst5(self):
        '''
            Test the worst5 endpoint.
        '''
        self.run_test_case(4)
    
    def test_5_global_mean(self):
        '''
            Test the global_mean endpoint.
        '''
        self.run_test_case(5)

    def test_6_diff_from_mean(self):
        '''
            Test the diff_from_mean endpoint.
        '''
        self.run_test_case(6)
    
    def test_7_state_diff_from_mean(self):
        '''
            Test the state_diff_from_mean endpoint.
        '''
        self.run_test_case(7)

    def test_8_mean_by_category(self):
        '''
            Test the mean_by_category endpoint.
        '''
        self.run_test_case(8)

    def test_9_state_mean_by_category(self):
        '''
            Test the state_mean_by_category endpoint.
        '''
        self.run_test_case(9)

    def test_z_graceful_shutdown(self):
        '''
            Test the graceful_shutdown endpoint.
        '''
        res = requests.get(self.base_url + 'graceful_shutdown', timeout=50)

        # Wait for the server to shut down
        time.sleep(5)

        # Check if the server is down
        res = requests.post(
            self.base_url + 'states_mean', 
            json={"question": "What is the mean of the states?"},
            timeout=50
        )
        res_data = res.json()
        self.assertEqual(res_data["status"], "error")

    def test_z_get_jobs(self):
        '''
            Test the get_jobs endpoint.
        '''
        expected_res = []
        for i in range(1, 10):
            expected_res.append({str(i): "done"})
        
        res = requests.get(self.base_url + 'jobs', timeout=5)
        res_data = res.json()["data"]
        self.assertEqual(res_data, expected_res)

    def run_test_case(self, test_number):
        '''
            Function that runs the test case for the given test number.
        '''
        with open(f'unittests/in/in-{test_number}.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)

        endpoint = f"{self.base_url}{test_data['route']}"
        payload = {"question": test_data["question"]}

        if "state" in test_data:
            payload["state"] = test_data["state"]

        res = requests.post(endpoint, json=payload, timeout=5)
        job_id = res.json().get("job_id", None)

        current = 0

        while True:
            res = requests.get(
                self.base_url + "get_results/" + str(job_id), timeout=5)
            res_data = res.json()

            if res_data["status"] == "done":
                break

            if res_data["status"] == "running":
                time.sleep(0.2)
                current += 0.2

            elif current > 1.5:
                self.fail("Timeout")

            else:
                self.fail("Error")

        res_data = res_data["data"]

        with open(f'unittests/out/out-{test_number}.json', 'r', encoding='utf-8') as f:
            expected_data = json.load(f)
            self.assertEqual(res_data, expected_data)

if __name__ == '__main__':
    unittest.main()
