import requests
import re

DEFAULT_BASE_URL = 'http://sc22sro.pythonanywhere.com/'
BASE_URL = DEFAULT_BASE_URL
session = requests.Session()

logged_in = False

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

def register():
    global logged_in
    if logged_in:
        print("You are already logged in. Logout first to register a new account.")
        return

    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    confirm_password = input("Confirm password: ").strip()

    if password != confirm_password:
        print("Passwords do not match! Registration aborted.")
        return

    if not EMAIL_REGEX.match(email):
        print("Invalid email format. Please provide a valid email address.")
        return

    data = {
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': confirm_password
    }

    try:
        response = session.post(BASE_URL + 'accounts/register/', data=data)
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return

    try:
        resp = response.json()
    except Exception as e:
        print("Error parsing response:", e)
        return

    if 'error' in resp:
        print("Registration error:", resp['error'])
    elif isinstance(resp, dict) and any(k in resp for k in ('username', 'email', 'password')):
        if 'email' in resp:
            print("Email error:", resp['email'])
        elif 'username' in resp:
            print("Username error:", resp['username'])
        elif 'password' in resp:
            print("Password error:", resp['password'])
        else:
            print("Registration error:", resp)
    else:
        print(resp.get('message', 'Registration successful'))
        logged_in = True

def login(url_arg):
    global logged_in, BASE_URL
    if logged_in:
        print("You are already logged in. Please logout first before logging in with another account.")
        return
    url = DEFAULT_BASE_URL if url_arg.lower() == "sc22" else url_arg
    BASE_URL = url if url.endswith('/') else url + '/'
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if not username or not password:
        print("Error: Both username and password are required.")
        return
    data = {'username': username, 'password': password}
    try:
        response = session.post(BASE_URL + 'accounts/login/', data=data)
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return
    try:
        resp = response.json()
    except Exception as e:
        print("Error parsing response:", e)
        return
    if 'error' in resp:
        print("Login error:", resp['error'])
        print("Have you registered? If not, please register first.")
    else:
        print(resp.get('message', 'Login successful'))
        logged_in = True

def logout():
    global logged_in
    if not logged_in:
        print("You are not logged in.")
        return

    session.get(BASE_URL + 'accounts/logout/')
    print("Logged out successfully.")
    logged_in = False

def list_modules():
    if not logged_in:
        print("Please log in first.")
        return

    response = session.get(BASE_URL + 'professor_rating/')
    try:
        data = response.json()
    except Exception as e:
        print("Error parsing response:", e)
        return

    modules = data.get('modules', [])

    if not modules:
        print("No modules found.")
        return

    header = "{:<12} {:<25} {:<20} {:<6} {:<10} {:<40}".format(
        "Module Code", "Module Name", "Department", "Year", "Semester", "Professors"
    )
    print("\n-- List of Modules & Professors --")
    print(header)
    print("-" * len(header))
    for module in modules:
        professors = module.get('professors', [])
        prof_list = ", ".join([f"{p['id']} ({p['name']})" for p in professors])
        print("{:<12} {:<25} {:<20} {:<6} {:<10} {:<40}".format(
            module.get('module_code', 'N/A'),
            module.get('name', 'N/A'),
            module.get('department', 'N/A'),
            str(module.get('year', 'N/A')),
            str(module.get('semester', 'N/A')),
            prof_list
        ))
    print("\n")

def view_ratings():
    if not logged_in:
        print("Please log in first.")
        return

    response = session.get(BASE_URL + 'professor_rating/view/')
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Received unexpected response from the server.")
        return

    ratings_list = data.get('ratings', [])
    if not ratings_list:
        print("\nNo ratings available.")
        return

    header = "{:<15} {:<25} {:<20} {:<6}".format(
        "Professor ID", "Professor Name", "Department", "Avg Rating"
    )
    print("\n-- All Ratings --")
    print(header)
    print("-" * len(header))
    for rating in ratings_list:
        print("{:<15} {:<25} {:<20} {:<6}".format(
            rating.get('professor_id', 'N/A'),
            rating.get('professor_name', 'N/A'),
            rating.get('department', 'N/A'),
            rating.get('average_rating', 'N/A')
        ))
    print("\n")

def average_rating(args):
    if not logged_in:
        print("Please log in first.")
        return

    if len(args) != 2:
        print("Usage: average <professor_id> <module_code>")
        return

    professor_id, module_code = args[0], args[1]
    url = f"{BASE_URL}professor_rating/average/{professor_id}/{module_code}/"
    response = session.get(url)

    if response.status_code != 200:
        print("Not existent")
        return

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Received unexpected response from the server.")
        return

    avg_rating = result.get('average_rating', None)
    if avg_rating is not None:
        try:
            avg_rating = round(float(avg_rating))
        except (ValueError, TypeError):
            avg_rating = "N/A"
    else:
        avg_rating = "N/A"

    print("\n-- Average Rating --")
    print(f"Professor ID  : {result.get('professor_id', 'N/A')}")
    print(f"Module Code   : {result.get('module_code', 'N/A')}")
    print(f"Average Rating: {avg_rating}\n")

def rate_professor(args):
    if not logged_in:
        print("Please log in first.")
        return

    if len(args) != 5:
        print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
        return

    professor_id, module_code, year, semester, rating = args

    data = {
        'professor_id': professor_id,
        'module_code': module_code,
        'year': year,
        'semester': semester,
        'rating': rating
    }

    response = session.post(BASE_URL + 'professor_rating/api_rate_professor/', json=data)

    try:
        resp_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Server returned invalid response.")
        return

    print("\n-- Rating Response --")
    if 'error' in resp_json:
        print("Error:", resp_json['error'])
    else:
        print(f"Rating submitted successfully for professor {resp_json.get('professor_id', 'N/A')} in module {resp_json.get('module_code', 'N/A')} with a score of {resp_json.get('score', 'N/A')}.")

def main():
    global logged_in
    print("Welcome to the Professor Rating System")
    while True:
        command_line = input("\nEnter command: ").strip()
        if not command_line:
            continue
        parts = command_line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == "register":
            register()
        elif cmd == "login":
            if args:
                login(args[0])
            else:
                print("Usage: login <url>")
        elif cmd == "logout":
            logout()
        elif cmd == "list":
            if args:
                print("Usage: list")
            else:
                list_modules()
        elif cmd == "view":
            if args:
                print("Usage: view")
            else:
                view_ratings()
        elif cmd == "average":
            average_rating(args)
        elif cmd == "rate":
            rate_professor(args)
        elif cmd == "exit":
            print("Exiting program.")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == '__main__':
    main()
