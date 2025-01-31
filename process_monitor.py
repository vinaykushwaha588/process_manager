import psutil
import time
import requests
import socket

# API endpoint of the Django backend
API_URL = "http://127.0.0.1:8000/api/process-data/"
SYSTEM_NAME = socket.gethostname()

def get_process_info():
    """Fetch information about currently running processes."""
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info = {
                'pid': process.info['pid'],
                'name': process.info['name'],
                'cpu_percent': process.info['cpu_percent'],
                'memory_percent': process.info['memory_percent']
            }
            # Check if any of the memory or CPU data is invalid
            if process_info['memory_percent'] is None or process_info['cpu_percent'] is None:
                raise ValueError(f"Invalid process data for PID {process_info['pid']}")

            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError) as e:
            continue
    return processes

def send_process_info():
    """Send process data to the centralized Django system."""
    while True:
        data = {
            "system_name": SYSTEM_NAME,
            "processes": get_process_info()
        }
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 201:
                print("Data sent successfully.")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Failed to send data: {e}")
        time.sleep(5)  # Wait for 5 seconds before sending data again
        
if __name__ == "__main__":
    send_process_info()
