from locust import HttpUser, task, between
import random

class MyUser(HttpUser):
    #host = "http://192.168.56.109:30003"
    #host = "http://192.168.56.241:90"
    #host = "http://192.168.56.201"
    host = "http://20.235.161.48"

    urls_to_test = [f"/update_employee/test_{empid}" for empid in range(1, 50000)]
    random.shuffle(urls_to_test)

    @task
    def update_employee(self):
        if not self.urls_to_test:
            self.environment.runner.quit() 
            return

        url = self.urls_to_test.pop()
        response = self.client.put(url)

        if response.status_code == 200:
            pass
        elif 400 <= response.status_code < 500:
            pass

#i1_ --> usage of nodeport with 7 replicas
#i2_ --> introduce metallb