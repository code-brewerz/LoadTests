import pytest
import subprocess
from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task
    def load_chefsbestpastry(self):
        self.client.get("/chefsbestpastry/?hl=en")

    @task
    def load_cooking_shooking(self):
        self.client.get("/cooking.shooking/?hl=en")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)


@pytest.mark.parametrize("num_users, spawn_rate, run_time", [
    (10, 1, "10s"),
    (20, 2, "20s"),
])
def test_onLocust(num_users, spawn_rate, run_time):
    cmd = [
        "locust",
        "-f", "test_insta.py",
        "--host", "https://www.instagram.com",
        "-u", str(num_users),
        "-r", str(spawn_rate),
        "--run-time", run_time,
        "--stop-timeout", "60",
        "--headless",
        "--html", "report.html"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Locust test failed with error:\n{result.stderr}"
    assert "Traceback" not in result.stderr, f"Locust test encountered an error:\n{result.stderr}"
    assert "FAILED" not in result.stderr, f"Locust test encountered a failure:\n{result.stderr}"

    print(result.stdout)

