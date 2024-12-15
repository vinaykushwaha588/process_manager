# Process Monitoring API

A Django-based application for monitoring and managing system process data. The application provides RESTful APIs to receive, store, and filter process information from multiple systems.

---

## Features

- Submit process data.
- Filter data by system name and time.
- Robust error handling.

---

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```

4. Run the Django server:

    ```bash
    python manage.py runserver
    ```

---

## Running the Process Monitor

After starting the Django server, you need to monitor the system processes in real-time. To do this, follow these steps:

1. Open a new terminal window.
2. Run the process monitor script:

    ```bash
    python process_monitor.py
    ```

This script collects and submits process data from your system to the API.

---

## API Endpoints

### Process Submission

- **Endpoint**: `/api/process-data/`
- **Method**: `POST`
- **Payload Example**:

    ```json
    {
        "system_name": "System_A",
        "processes": [
            {"pid": 1234, "name": "python", "cpu_percent": 5.2, "memory": 1.5},
            {"pid": 5678, "name": "chrome", "cpu_percent": 15.7, "memory": 8.3}
        ]
    }
    ```

### Process Filtering

- **Endpoint**: `/api/process-filter/`
- **Method**: `GET`
- **Query Parameters**:
    - `system_name` (required)
    - `start_time` (optional, format: `HH:MM:SS`)
    - `end_time` (optional, format: `HH:MM:SS`)

Example:

```bash
GET /api/process-filter/?system_name=System_A&start_time=09:00:00&end_time=17:00:00
