# Attendance System

This is a Django-based attendance system where users can register, log in, and mark their attendance. It also includes a homepage displaying an attendance graph for users to track their attendance history.

## Features

- **User Registration & Login**: 
  - Users can register with their email and password.
  - After registration, users must be verified by a superuser to log in.
  
- **User Verification**:
  - Only verified users can log in.
  - Superusers have the ability to verify registered users.

- **Attendance**:
  - Users can mark themselves as present for the current day.
  - An attendance graph is displayed on the homepage, showing the user’s attendance over time.

- **API Access:** :
The system provides a RESTful API that can be accessed at `/api/v1/docs/`, which includes endpoints for user registration, login, and attendance marking. The API uses token authentication.


### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/attendance-system.git
    cd attendance-system
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```bash
    python manage.py migrate
    ```

4. Load fixtures for initial data:
    ```bash
    python manage.py loaddata user_fixtures.json
    python manage.py loaddata attendance_fixtures.json
    ```

5. Create a superuser to manage the system:
    ```bash
    python manage.py createsuperuser
    ```

5. Test user credentials:
    ```bash
    email: testuser@example.com
    pswd: nepal123
    ```
### API DOcumentation

To access the API documentation, navigate to http://127.0.0.1:8000/api/v1/docs/ after starting the server.