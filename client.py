# import requests

# BASE_URL = 'http://127.0.0.1:8000/'  # Django server URL on localhost
# session = requests.Session()  # Use a session to persist cookies

# # Global flag to track login state
# logged_in = False

# def register():
#     global logged_in
#     print("\n-- Registration --")
#     username = input("Enter username: ")
#     email = input("Enter email: ")
#     password = input("Enter password: ")
#     confirm_password = input("Confirm password: ")
#     if password != confirm_password:
#         print("Passwords do not match! Registration aborted.")
#         return
#     data = {
#         'username': username,
#         'email': email,
#         'password': password,
#         'confirm_password': confirm_password
#     }
#     response = session.post(BASE_URL + 'accounts/register/', data=data)
#     try:
#         resp = response.json()
#     except Exception as e:
#         print("Error parsing response:", e)
#         return
#     if 'error' in resp:
#         print("Registration error:", resp['error'])
#     else:
#         print(resp.get('message', 'Registration successful'))
#         logged_in = True

# def login():
#     global logged_in
#     print("\n-- Login --")
#     username = input("Enter username: ")
#     password = input("Enter password: ")
#     data = {'username': username, 'password': password}
#     response = session.post(BASE_URL + 'accounts/login/', data=data)
#     try:
#         resp = response.json()
#     except Exception as e:
#         print("Error parsing response:", e)
#         return
#     if 'error' in resp:
#         print("Login error:", resp['error'])
#         print("Have you registered? If not, please register first.")
#     else:
#         print(resp.get('message', 'Login successful'))
#         logged_in = True

# def logout():
#     global logged_in
#     session.get(BASE_URL + 'accounts/logout/')
#     print("Logged out successfully.")
#     logged_in = False

# def get_professors_and_modules():
#     """
#     Retrieve professors and modules from the server.
#     Assumes the response JSON contains:
#       - 'professors': list of professor dictionaries
#       - 'modules': list of module dictionaries, each including:
#             'module_code', 'name', 'year', 'semester', 'average_rating',
#             'professor_id', and 'professor_name'
#     """
#     response = session.get(BASE_URL + 'professor_rating/')
#     data = response.json()
#     professors = data.get('professors', [])
#     modules = data.get('modules', [])
#     return professors, modules

# def list_combined():
#     """Display a combined table of modules with their associated professor details,
#     showing professor details only once per professor group.
#     Uses the module's 'department' field in place of a module name.
#     """
#     if not logged_in:
#         print("Please log in first.")
#         return
#     professors, modules = get_professors_and_modules()
#     if not modules:
#         print("No modules found.")
#         return

#     # Build a mapping for professor information
#     prof_info = {}
#     for prof in professors:
#         prof_info[prof.get('id', '')] = {
#             'name': prof.get('name', '')
#         }

#     # Group modules by professor_id
#     grouped = {}
#     for mod in modules:
#         prof_id = mod.get('professor_id', '')
#         if prof_id not in grouped:
#             grouped[prof_id] = []
#         grouped[prof_id].append(mod)
    
#     # Print header (without ratings)
#     header = "{:<10} {:<25} {:<15} {:<25} {:<6}".format(
#         "Prof ID", "Prof Name", "Module Code", "Department", "Year"
#     )
#     print("\n-- Combined List of Modules & Professors --")
#     print(header)
#     print("-" * len(header))
    
#     # For each professor group, display each module;
#     # show professor details only once (in the first row for that professor).
#     for prof_id, mods in grouped.items():
#         first = True
#         for mod in mods:
#             if first:
#                 prof_id_disp = mod.get('professor_id', '')
#                 prof_name_disp = mod.get('professor_name', '')
#                 first = False
#             else:
#                 prof_id_disp = ""
#                 prof_name_disp = ""
#             module_code = mod.get('module_code', '')
#             dept = mod.get('department', '')
#             year = mod.get('year', '')
#             print("{:<10} {:<25} {:<15} {:<25} {:<6}".format(
#                 prof_id_disp,
#                 prof_name_disp,
#                 module_code,
#                 dept,
#                 year
#             ))


# def average_rating():
#     if not logged_in:
#         print("Please log in first.")
#         return

#     professors, modules = get_professors_and_modules()
#     if not professors:
#         print("No professors available.")
#         return

#     # Ask if the user wants overall professor rating or module-specific rating
#     print("\nDo you want the overall professor rating or a specific module rating?")
#     print("1. Overall Professor Rating")
#     print("2. Specific Module Rating")
#     choice = input("Enter option number (1 or 2): ").strip()

#     if choice == '1':  # Get overall professor rating
#         print("\nSelect a professor:")
#         for idx, prof in enumerate(professors, start=1):
#             print(f"{idx}. {prof['id']} - {prof['name']}")
#         try:
#             prof_choice = int(input("Enter professor option number: "))
#             selected_prof = professors[prof_choice - 1]
#         except (ValueError, IndexError):
#             print("Invalid professor selection.")
#             return

#         professor_id = selected_prof['id']
#         professor_name = selected_prof['name']
#         professor_avg = selected_prof.get('average_rating', 'N/A')

#         print("\n-- Overall Professor Rating --")
#         print(f"Professor ID   : {professor_id}")
#         print(f"Professor Name : {professor_name}")
#         print(f"Average Rating : {professor_avg}")

#     elif choice == '2':  # Get module-specific rating
#         print("\nSelect a professor:")
#         for idx, prof in enumerate(professors, start=1):
#             print(f"{idx}. {prof['id']} - {prof['name']}")
#         try:
#             prof_choice = int(input("Enter professor option number: "))
#             selected_prof = professors[prof_choice - 1]
#         except (ValueError, IndexError):
#             print("Invalid professor selection.")
#             return

#         professor_id = selected_prof['id']
#         professor_modules = [m for m in modules if m.get('professor_id') == professor_id]

#         if not professor_modules:
#             print("No modules found for this professor.")
#             return

#         # Let user select a module
#         print("\nSelect a module for the chosen professor:")
#         for idx, mod in enumerate(professor_modules, start=1):
#             print(f"{idx}. {mod['module_code']} - {mod['department']}")
#         try:
#             mod_choice = int(input("Enter module option number: "))
#             selected_mod = professor_modules[mod_choice - 1]
#         except (ValueError, IndexError):
#             print("Invalid module selection.")
#             return

#         module_code = selected_mod['module_code']
#         url = f"{BASE_URL}professor_rating/average/{professor_id}/{module_code}/"
#         response = session.get(url)
#         try:
#             result = response.json()
#         except requests.exceptions.JSONDecodeError:
#             print("Error: Received unexpected response from the server.")
#             return

#         # Display the module rating
#         print("\n-- Module-Specific Rating --")
#         print(f"Professor ID  : {result.get('professor_id', 'N/A')}")
#         print(f"Module Code   : {result.get('module_code', 'N/A')}")
#         print(f"Average Rating: {result.get('average_rating', 'N/A')}")

#     else:
#         print("Invalid option. Please enter 1 or 2.")



# def rate_professor():
#     if not logged_in:
#         print("Please log in first.")
#         return

#     professors, modules = get_professors_and_modules()
#     if not professors:
#         print("No professors available.")
#         return

#     # Let user select a professor
#     print("\nSelect a professor:")
#     for idx, prof in enumerate(professors, start=1):
#         print(f"{idx}. {prof['id']} - {prof['name']}")
#     try:
#         prof_choice = int(input("Enter professor option number: "))
#         selected_prof = professors[prof_choice - 1]
#     except (ValueError, IndexError):
#         print("Invalid professor selection.")
#         return

#     professor_id = selected_prof['id']
#     professor_modules = [m for m in modules if m.get('professor_id') == professor_id]
#     if not professor_modules:
#         print("No modules found for this professor.")
#         return

#     # Select a module
#     print("\nSelect a module for the chosen professor:")
#     for idx, mod in enumerate(professor_modules, start=1):
#         print(f"{idx}. {mod['module_code']} - {mod['department']}")
#     try:
#         mod_choice = int(input("Enter module option number: "))
#         selected_mod = professor_modules[mod_choice - 1]
#     except (ValueError, IndexError):
#         print("Invalid module selection.")
#         return

#     module_code = selected_mod['module_code']
#     rating_val = input("Enter rating (1-5): ")

#     data = {
#         'professor_id': professor_id,
#         'module_code': module_code,
#         'rating': rating_val
#     }

#     response = session.post(BASE_URL + 'professor_rating/api_rate_professor/', json=data)

#     # **Check if response is valid JSON**
#     try:
#         resp_json = response.json()
#     except requests.exceptions.JSONDecodeError:
#         print("Error: Server returned invalid response.")
#         return

#     print("\n-- Rating Response --")
#     print(resp_json)


# def view_ratings():
#     if not logged_in:
#         print("Please log in first.")
#         return
#     response = session.get(BASE_URL + 'professor_rating/view/')
#     print("\n-- All Ratings --")
#     print(response.json())

# def main():
#     global logged_in
#     while True:
#         if not logged_in:
#             print("\n==== Main Menu ====")
#             print("1. Register")
#             print("2. Login")
#             print("3. Exit")
#             choice = input("Enter option number: ").strip()
#             if choice == '1':
#                 register()
#             elif choice == '2':
#                 login()
#             elif choice == '3':
#                 break
#             else:
#                 print("Invalid option.")
#         else:
#             print("\n==== User Menu ====")
#             print("1. Logout")
#             print("2. List Combined Modules & Professors")
#             print("3. Average Rating")
#             print("4. Rate Professor")
#             # print("5. View All Ratings")
#             print("5. Exit")
#             choice = input("Enter option number: ").strip()
#             if choice == '1':
#                 logout()
#             elif choice == '2':
#                 list_combined()
#             elif choice == '3':
#                 average_rating()
#             elif choice == '4':
#                 rate_professor()
#             # elif choice == '5':
#             #     view_ratings()
#             elif choice == '5':
#                 break
#             else:
#                 print("Invalid option.")

# if __name__ == '__main__':
#     main()

import requests
from tabulate import tabulate

# Default Django server URL
DEFAULT_BASE_URL = 'http://127.0.0.1:8000/'
BASE_URL = DEFAULT_BASE_URL  # Allow changing the base URL if needed
session = requests.Session()  # Use a session to persist cookies

# Global flag to track login state
logged_in = False

def register():
    """Command: register"""
    global logged_in
    if logged_in:
        print("You are already logged in. Logout first to register a new account.")
        return

    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match! Registration aborted.")
        return

    data = {'username': username, 'email': email, 'password': password, 'confirm_password': confirm_password}
    response = session.post(BASE_URL + 'accounts/register/', data=data)
    
    try:
        resp = response.json()
    except Exception as e:
        print("Error parsing response:", e)
        return

    if 'error' in resp:
        print("Registration error:", resp['error'])
    else:
        print(resp.get('message', 'Registration successful'))
        logged_in = True

def login():
    """Command: login"""
    global logged_in, BASE_URL

    if logged_in:
        print("You are already logged in. Please logout first before logging in with another account.")
        return

    url = input(f"Enter service URL (Press Enter to use {DEFAULT_BASE_URL}): ").strip()
    if not url:
        url = DEFAULT_BASE_URL  # Use default if empty
    
    BASE_URL = url if url.endswith('/') else url + '/'  # Ensure trailing slash
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    data = {'username': username, 'password': password}
    response = session.post(BASE_URL + 'accounts/login/', data=data)
    
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
    """Command: logout"""
    global logged_in
    if not logged_in:
        print("You are not logged in.")
        return

    session.get(BASE_URL + 'accounts/logout/')
    print("Logged out successfully.")
    logged_in = False

def list_modules():
    """Command: list - Display modules and professors in a tabular format"""
    if not logged_in:
        print("Please log in first.")
        return

    response = session.get(BASE_URL + 'professor_rating/')
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Received unexpected response from the server.")
        return

    professors = data.get('professors', [])
    modules = data.get('modules', [])

    if not modules:
        print("No modules found.")
        return

    table_data = []
    for module in modules:
        professor_names = ", ".join([prof["name"] for prof in module.get("professors", [])])
        table_data.append([
            module["module_code"],
            module["name"],
            module["department"],
            module["year"],
            module["semester"],  # Added semester field
            professor_names
        ])

    headers = ["Module Code", "Module Name", "Department", "Year", "Semester", "Professors"]
    print("\n-- List of Modules & Professors --")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("\n")

def view_ratings():
    """Command: view"""
    if not logged_in:
        print("Please log in first.")
        return

    response = session.get(BASE_URL + 'professor_rating/view/')
    
    try:
        ratings = response.json().get("ratings", [])
    except requests.exceptions.JSONDecodeError:
        print("Error: Received unexpected response from the server.")
        return
    
    if not ratings:
        print("\nNo ratings available.")
        return

    print("\n-- All Ratings --")
    for rating in ratings:
        print(f"Professor: {rating['professor__name']} | Module: {rating['module__name']} | Year: {rating['module__year']} | Score: {rating['score']}")
    print("\n")

def average_rating():
    """Command: average <professor_id> <module_code>"""
    if not logged_in:
        print("Please log in first.")
        return
    
    print("\n1. Overall Professor Rating")
    print("2. Specific Module Rating")
    choice = input("Enter option number: ").strip()

    if choice == '1':  # Overall professor rating
        professor_id = input("Enter professor ID: ")
        url = f"{BASE_URL}professor_rating/average/{professor_id}/"
    
    elif choice == '2':  # Specific module rating
        professor_id = input("Enter professor ID: ")
        module_code = input("Enter module code: ")
        url = f"{BASE_URL}professor_rating/average/{professor_id}/{module_code}/"
    
    else:
        print("Invalid option.")
        return

    response = session.get(url)
    
    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Received unexpected response from the server.")
        return

    # Display the average rating
    print("\n-- Average Rating --")
    print(f"Professor ID  : {result.get('professor_id', 'N/A')}")
    print(f"Module Code   : {result.get('module_code', 'N/A')}")
    print(f"Average Rating: {result.get('average_rating', 'N/A')}\n")

def rate_professor():
    """Command: rate <professor_id> <module_code> <year> <semester> <rating>"""
    if not logged_in:
        print("Please log in first.")
        return
    
    professor_id = input("Enter professor ID: ")
    module_code = input("Enter module code: ")
    year = input("Enter teaching year: ")
    semester = input("Enter semester: ")
    rating = input("Enter rating (1-5): ")

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
    print(resp_json)

def main():
    global logged_in
    print("Welcome to the Professor Rating System")
    
    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "register":
            register()
        elif command == "login":
            login()
        elif command == "logout":
            logout()
        elif command == "list":
            list_modules()
        elif command == "view":
            view_ratings()
        elif command == "average":
            average_rating()
        elif command == "rate":
            rate_professor()
        elif command == "exit":
            print("Exiting program.")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == '__main__':
    main()
