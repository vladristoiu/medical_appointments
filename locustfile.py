from locust import HttpUser, task, between
from bs4 import BeautifulSoup


class BeHealthyUser(HttpUser):
    wait_time = between(1, 3)

    def login(self, username, password):

        response = self.client.get("authentication/")
        soup = BeautifulSoup(response.content, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        self.client.post("authentication/", {
            "csrfmiddlewaretoken": csrf_token,
            "username": username,
            "password": password
        })

    @task(1)
    def successful_login(self):
        self.login("ristoiu", "ristoiu123456789")

    @task(2)
    def failed_login(self):
        self.login("invalid_username", "invalid_password")
