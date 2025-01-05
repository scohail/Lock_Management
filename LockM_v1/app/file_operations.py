# file_operations.py
import requests
import os

BASE_URL = 'http://localhost:5000'  # Adjust if your port is different

def create_file(filename, content):
    """Create a new file in HDFS"""
    url = f'{BASE_URL}/create_file'
    data = {
        'filename': filename,
        'content': content
    }
    response = requests.post(url, data=data)
    return response.status_code, response.text

def update_file(filename, content):
    """Update an existing file in HDFS"""
    url = f'{BASE_URL}/update/{filename}'
    data = {
        'content': content
    }
    response = requests.post(url, data=data)
    return response.status_code, response.text

def read_file(filename):
    """Read a file from HDFS"""
    url = f'{BASE_URL}/read/{filename}'
    response = requests.get(url)
    return response.status_code, response.json()

# Example usage
if __name__ == "__main__":
    # Create a new file
    status, response = create_file("test.txt", "Hello, this is a test file!")
    print(f"Create file status: {status}")
    print(f"Response: {response}")

    # Read the file
    status, response = read_file("test.txt")
    print(f"\nRead file status: {status}")
    print(f"Content: {response}")

    # Update the file
    status, response = update_file("test.txt", "Updated content!")
    print(f"\nUpdate file status: {status}")
    print(f"Response: {response}")

    # Read the updated file
    status, response = read_file("test.txt")
    print(f"\nRead updated file status: {status}")
    print(f"Updated content: {response}")