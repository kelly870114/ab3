from locust import HttpUser, task, between, TaskSet, constant
from locust import LoadTestShape

class UserTasks(TaskSet):
    @task
    def get_order(self):
        self.client.get("/getData")

class User(HttpUser):
    wait_time = between(0.5, 3.0)
    tasks = {UserTasks}

class CustomShape(LoadTestShape):
    stages = [
        {"duration": 15, "users": 10, "spawn_rate": 10},
        {"duration": 45, "users": 20, "spawn_rate": 10},
        {"duration": 75, "users": 30, "spawn_rate": 10},
        {"duration": 125, "users": 50, "spawn_rate": 10},
        {"duration": 150, "users": 60, "spawn_rate": 10},
        {"duration": 200, "users": 80, "spawn_rate": 10},
        {"duration": 230, "users": 100, "spawn_rate": 10},
        {"duration": 270, "users": 100, "spawn_rate": 10},
        {"duration": 570, "users": 100, "spawn_rate": 10},
        {"duration": 600, "users": 90, "spawn_rate": 10},
        {"duration": 650, "users": 70, "spawn_rate": 10},
        {"duration": 700, "users": 50, "spawn_rate": 10},
        {"duration": 750, "users": 30, "spawn_rate": 10},
        {"duration": 800, "users": 20, "spawn_rate": 10},
        {"duration": 900, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
