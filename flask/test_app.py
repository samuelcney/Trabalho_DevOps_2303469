import unittest
import requests

class TestApp(unittest.TestCase):
    base_url = "http://localhost:5000"

    def test_register_student(self):
        payload = {"ra": "12345", "name": "Student Test"}
        response = requests.post(f"{self.base_url}/students", json=payload)

	print(response.json())

        self.assertEqual(response.status_code, 201)

        students = requests.get(f"{self.base_url}/students").json()
        self.assertTrue(any(student["ra"] == "12345" for student in students))

if __name__ == "__main__":
    unittest.main()

