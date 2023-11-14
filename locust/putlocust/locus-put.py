from locust import HttpUser, task, between
import random

class MyUser(HttpUser):
    #host = "http://192.168.56.109:30003"
    #host = "http://192.168.56.241:90"
    host = "http://192.168.56.240"

    # Define a list of URLs to be tested
    urls_to_test = [f"/update_employee/i5_pyopt_{empid}" for empid in range(1, 20000)]
    random.shuffle(urls_to_test)  # Shuffle the list to randomize the order

    @task
    def update_employee(self):
        if not self.urls_to_test:
            self.environment.runner.quit()  # Quit the test when all URLs are tested
            return

        url = self.urls_to_test.pop()
        response = self.client.put(url)

        if response.status_code == 200:
            # If the response is successful, continue
            pass
        elif 400 <= response.status_code < 500:
            # If the response is a 4xx error, log the failure and move to the next URL
            pass

#i1_ --> usage of nodeport with 7 replicas
#i2_ --> introduce metallb