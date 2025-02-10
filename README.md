# RESTFUL-Professor-Rating-Service 🎓⭐
## **Description**
A web service allowing students to rate professors based on their teaching performance. The service is built using Django and exposes a RESTful API for interaction with the system. It includes features for user authentication, professor and module management, rating submission, and a client application for communication with the service.

## **Features**  
- ✅ **User Authentication** – Register, login, and logout.  
- ✅ **Professor & Module Management** – Admin adds professors and modules.  
- ✅ **Rate Professors** – Students can rate professors for specific modules.  
- ✅ **View Ratings** – Get overall and module-specific professor ratings.  
- ✅ **REST API** – Fully functional API with endpoints for interaction.  
- ✅ **Client Application** – CLI tool to interact with the service.

## **Tech Stack**  
- **Backend**: Django, Django REST Framework  
- **Database**: PostgreSQL / SQLite  
- **Authentication**: Token-based authentication  
- **Deployment**: Hosted on PythonAnywhere

## **API Endpoints**  

| Method | Endpoint | Description |  
|--------|----------|-------------|  
| **POST** | `/register/` | User registration |  
| **POST** | `/login/` | User login |  
| **POST** | `/logout/` | User logout |  
| **GET** | `/modules/` | List all modules and professors |  
| **GET** | `/ratings/professors/` | View professor ratings |  
| **GET** | `/ratings/professor/{professor_id}/module/{module_code}/` | View professor rating in a module |  
| **POST** | `/rate/` | Submit a rating |

## **Workflow:**

1. **Start**  
   The process begins.

2. **User Register/Login**  
   The user either registers a new account or logs into an existing one.  
   Authentication happens at this stage.

3. **View Modules**  
   Once logged in, the user can view a list of all available module instances and the professors teaching them.

4. **View Professor Ratings**  
   Alternatively, the user can choose to view the ratings of professors across all modules.

5. **Select Module Instance**  
   If the user chose to view modules, they select a specific module instance (year and semester).

6. **View Professor Rating for Module**  
   If the user selected the view ratings option, they can check the rating for a specific professor in a specific module.

7. **Submit Rating**  
   If the user has selected a module instance, they can submit a rating (from 1-5) for a professor.

8. **Update Professor Average Rating**  
   Once a rating is submitted, the system updates the professor's average rating based on all ratings for that professor.

9. **Store Rating in Database**  
   The rating is stored in the database for future reference.

10. **End**  
    The process ends.

## **Client Application Commands:**

- `register`: Allows the user to register by entering their username, email, and password.
- `login <url>`: Logs the user into the service using their username and password.
- `logout`: Logs the user out of the service.
- `list`: Views a list of all modules and professors.
- `view`: Views the ratings of all professors.
- `average <professor_id> <module_code>`: Views the average rating of a professor in a specific module.
- `rate <professor_id> <module_code> <year> <semester> <rating>`: Submits a rating for a professor in a specific module instance.

## **Setup & Installation**

### Requirements
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL or SQLite

### Steps to run the project locally:
1. Clone the repository:  
   `git clone`

2. Install dependencies:  
   `pip install -r requirements.txt`

3. Apply migrations:  
   `python manage.py migrate`

4. Run the server:  
   `python manage.py runserver`

5. Access the application at:  
   `http://127.0.0.1:8000/`

## **License**  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


