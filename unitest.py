import unittest
import requests
import json

class TestCalendarApi(unittest.TestCase):
    token = None
    def setUp(self) -> None:
        self.url = 'http://localhost:5000'
        self.headers = {"Content-Type": "application/json"}
        self.login_data = {
            "nickname": 'test_user',
            "email": "test@test.com",
            "password": "test_pwd"
        }
        self.event_data = {
            "header": "test_event",
            "description": "test description",
            "date": "2023-03-18",
            "time": "15:00"
        }
    def test1_signup_user(self):

        response = requests.post(url=f"{self.url}/signup", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["isReg"],True)
        response = requests.post(url=f"{self.url}/signup", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["isReg"],False)

    def test2_login_user_with_correct_data(self):
        global token
        response = requests.post(url=f'{self.url}/login', json=self.login_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isLogged"])
        self.assertTrue('token' in response.json())
        token = response.json()['token']

    def test3_create_new_event_with_correct_data(self):
        global token

        self.headers['Authorization'] = f'Bearer {token}'
        response = requests.post(url=f'{self.url}/create_event', json=self.event_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isAdded"])

    def test4_get_events_by_date_added_in_previous_test(self):
        global token
        self.headers['Authorization'] = f'Bearer {token}'

        response = requests.get(url=f'{self.url}/get_events_by/{self.event_data["date"]}', headers=self.headers)
        print(response.json())
        response_data = json.loads(response.json()[0])
        self.assertEqual(response_data["header"], self.event_data["header"])
        self.assertEqual(response_data["time"], self.event_data["time"])

    def test5_delete_event_added_in_prev_test(self):
        global token
        self.headers['Authorization'] = f'Bearer {token}'
        response = requests.get(url=f'{self.url}/delete_event_by/{self.event_data["header"]}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["IsDeleted"])



    def test9_delete_user_by_email(self):
        response = requests.post(url=f"{self.url}/delete_user_by/{self.login_data['email']}", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["IsDeleted"])

if __name__ == "__main__":
    unittest.main()
