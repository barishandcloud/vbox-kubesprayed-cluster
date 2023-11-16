from locust import HttpUser, task, between
import random

class MyUser(HttpUser):
    host = "http://192.168.56.109:30003"

    urls_to_test = [f"/get_employee/i1_{empid}" for empid in range(1, 100001)]
    random.shuffle(urls_to_test)

    @task
    def update_employee(self):
        if not self.urls_to_test:
            self.environment.runner.quit()
            return

        url = self.urls_to_test.pop()
        response = self.client.get(url)

        if response.status_code == 200:
            pass
        elif 400 <= response.status_code < 500:
            pass
