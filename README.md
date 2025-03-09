# RESTFUL-Professor-Rating-Service 🎓⭐

## **Description**
A web service that allows students to rate professors based on their teaching performance. The service is built using Django and exposes a RESTful API for system interaction. Features include user authentication, professor/module management, rating submission, and a command-line client to interact with the service.

## **Features**
- ✅ **User Authentication** – Register, login, and logout.
- ✅ **Professor & Module Management** – Admin adds professors and modules.
- ✅ **Rate Professors** – Students can rate professors for specific modules.
- ✅ **View Ratings** – View overall and module-specific professor ratings.
- ✅ **REST API** – Fully functional API for interaction.
- ✅ **Client Application** – CLI tool to interact with the service.

## **Tech Stack**
- **Backend:** Django, Django REST Framework  
- **Database:** SQLite  
- **Deployment:** Hosted on PythonAnywhere  

## **API Endpoints**

### **Accounts API**

**Login** | `/accounts/login/` | POST  
* **Purpose:** Authenticate a user and start a session.  
* **Req:** `username`, `password` (strings)  
* **Res:** 200 (success), 400 (missing required fields), 401 (invalid credentials), 403 (admin login not allowed), 405 (wrong method)

**Logout** | `/accounts/logout/` | POST  
* **Purpose:** End the current session.  
* **Req:** None  
* **Res:** 200 (success), 405 (wrong method)

**Register** | `/accounts/register/` | POST  
* **Purpose:** Create a new user account.  
* **Req:** `username`, `email`, `password`, `confirm_password` (strings)  
* **Res:** 200 (registration successful), 400 (missing required fields, passwords do not match, or duplicate username/email), 405 (wrong method), 500 (server error during registration)

---

### **Professor Rating API**

**List** | `/professor_rating/` | GET  
* **Purpose:** Retrieve a list of professors and modules with details.  
* **Req:** None  
* **Res:** 200 (JSON: professors & modules arrays), 401 (unauthorized), 500 (error)  
* **Response Details:**  
  * `professors`: Array of objects with `id`, `name`, `department`, `average_rating`  
  * `modules`: Array of objects with `module_code`, `name`, `department`, `year`, `semester`, `average_rating`, and associated professors

**Average** | `/professor_rating/average/<professor_id>/<module_code>/` | GET  
* **Purpose:** Return the average rating for a professor in a module.  
* **Req:** URL parameters `professor_id` and `module_code`  
* **Res:** 200 (JSON with average), 400 (invalid relation), 404 (not found), 500 (error)  
* **Response Example:** `{ "professor_id": "...", "module_code": "...", "average_rating": ... }`

**View** | `/professor_rating/view/` | GET  
* **Purpose:** Retrieve overall average ratings for all professors.  
* **Req:** None  
* **Res:** 200 (JSON ratings array), 401 (unauthorized), 500 (error)  
* **Response Details:** Array of objects with `professor_id`, `professor_name`, `department`, `average_rating`

**Rate** | `/professor_rating/api_rate_professor/` | POST  
* **Purpose:** Submit a rating using a complete JSON payload.  
* **Req:** JSON `professor_id` (string), `module_code` (string), `rating` (integer 1–5)  
* **Res:** 200 (success with details), 400 (invalid data), 404 (not found), 500 (error)  
* **Error Handling:** Missing fields, invalid rating values, or non-existent resources return appropriate error messages.

---

## **Client Application Commands**

The client application adheres to the provided specifications. The available commands are:

- `register` – Prompts for username, email, and password to register a new account.
- `login <url>` – Logs in to the service. The `<url>` parameter sets the service URL (e.g., `sc22sro.pythonanywhere.com`). If no URL is provided, the client uses the default.
- `logout` – Logs out the current user.
- `list` – Displays all modules and associated professors.
- `view` – Views overall average ratings for all professors.
- `average <professor_id> <module_code>` – Retrieves the average rating for a specific professor in a specific module (e.g., `average NG1 CS101`).
- `rate <professor_id> <module_code> <year> <semester> <rating>` – Submits a rating for a professor in a specific module instance (e.g., `rate NG1 CS101 2023 1 4`).
- `exit` – Exits the client.

## **Setup & Installation**

### Requirements
- Python 3.x  
- Django  
- Django REST Framework  
- PostgreSQL or SQLite  
- **Client Library:** `requests` (install via `pip install requests`)

### Local Setup
1. Clone the repository:  
   `git clone <repository-url>`
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Apply migrations:  
   `python manage.py migrate`
4. Run the server:  
   `python manage.py runserver`
5. Access the application at:  
   `http://127.0.0.1:8000/`

For deployment, the application is hosted on PythonAnywhere (e.g., `sc22sro.pythonanywhere.com`).
