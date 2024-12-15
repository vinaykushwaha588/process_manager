# Process Monitoring API

A Django-based application for monitoring and managing system process data. The application provides RESTful APIs to receive, store, and filter process information from multiple systems.

---

## Features

- Submit process data.
- Filter data by start and end time.
- Calculate the duration of a specific process.
- Robust error handling.

---

## Installation
### Step 1: Setting up a Virtual Environment

1. **Create a virtual environment** in the project directory:

    For Windows & Linux
    ```bash
    python3 -m venv venv
    ```
    
2. **Activate the virtual environment**:

    For Windows:
    ```bash
    .\venv\Scripts\activate
    ```

    For Linux:
    ```bash
    source venv/bin/activate
    ```


3. Clone the repository:

    ```bash
    git https://github.com/vinaykushwaha588/process_manager.git
    cd process_manager
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations & migrate: if required.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Run the Django server:

    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

---

## Running the Process Monitor

After starting the Django server, you need to monitor the system processes in real-time. To do this, follow these steps:

1. Open a new terminal window. in the same directory.
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
            {"pid": 1234, "name": "python", "cpu_percent": 5.2, "memory_percent": 1.5},
            {"pid": 5678, "name": "chrome", "cpu_percent": 15.7, "memory_percent": 8.3}
        ]
    }
    ```

### Process Filtering

- **Endpoint**: `/api/process-filter/`
- **Method**: `GET`
- **Query Parameters**:
    - `start_time` (format: `HH:MM:SS`)
    - `end_time` (format: `HH:MM:SS`)

Example:

```bash
GET {{url}}/api/filter-processes/?start_time=00:30:00&end_time=01:05:00


### Process Durations Specific process

- **Endpoint**: `/api/process-duration/`
- **Method**: `GET`
- **Query Parameters**:
    - `system_name` (required: ``)
    - `process_name` (required: ``)

Example:

```bash
GET {{url}}/api/process-duration/?system_name=Vinay&process_name=Code.exe

