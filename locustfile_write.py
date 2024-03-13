from locust import HttpUser, task, between, TaskSet, constant
from locust import LoadTestShape

class UserTasks(TaskSet):
    @task
    def post_order(self):
        data = {
            "table_id": 7,
            "orders": "locust test seoul",
            "order_time": "2024-03-05 12:00:00",
            "order_status": 0
        }
        self.client.post("/postData", json=data)

class User(HttpUser):
    wait_time = between(0.5, 3.0)
    tasks = {UserTasks}

# 常態分佈
class CustomShape(LoadTestShape):
    stages = [
        {"duration": 15, "users": 100, "spawn_rate": 10},
        {"duration": 45, "users": 200, "spawn_rate": 10},
        {"duration": 75, "users": 300, "spawn_rate": 10},
        {"duration": 125, "users": 500, "spawn_rate": 10},
        {"duration": 150, "users": 600, "spawn_rate": 10},
        {"duration": 200, "users": 1000, "spawn_rate": 10},
        {"duration": 230, "users": 2000, "spawn_rate": 10},
        {"duration": 270, "users": 2000, "spawn_rate": 10},
        {"duration": 570, "users": 2000, "spawn_rate": 10},
        {"duration": 600, "users": 1000, "spawn_rate": 10},
        {"duration": 650, "users": 700, "spawn_rate": 10},
        {"duration": 700, "users": 500, "spawn_rate": 10},
        {"duration": 750, "users": 300, "spawn_rate": 10},
        {"duration": 800, "users": 200, "spawn_rate": 10},
        {"duration": 900, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
