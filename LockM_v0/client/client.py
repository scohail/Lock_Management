import requests

class HDFSClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def health_check(self):
        """Check if the server is healthy"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def write_data(self, key, value):
        """Write data to the server"""
        response = requests.post(
            f"{self.base_url}/write",
            json={"key": key, "value": value}
        )
        return response.json()

    def read_data(self, key):
        """Read data from the server"""
        response = requests.get(f"{self.base_url}/read/{key}")
        return response.json()