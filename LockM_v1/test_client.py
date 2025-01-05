from client.client import HDFSClient

# Create client instance
client = HDFSClient()

# Test health check
print("Health check:", client.health_check())

# Test write operation
print("Writing data:", client.write_data("test_key", "test_value"))

# Test read operation
print("Reading data:", client.read_data("test_key"))