from locust import HttpUser, task

SERVER_IP_ADDR = "80.78.251.43"

class LoadTestingDjangoHW(HttpUser):
    @task
    def test_some_pages_open(self):
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/courses")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/courses/1/")

        self.client.get(f"http://{SERVER_IP_ADDR}/authapp/register")
        self.client.get(f"http://{SERVER_IP_ADDR}/authapp/login")