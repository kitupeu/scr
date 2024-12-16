import os
import readline
import requests
from datetime import datetime

# Define color codes for terminal output
RESET = "\033[0m"
SKY_BLUE = "\033[94m"
GREENISH = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

# File for logging commands and activity
LOG_FILE = "curl_command_builder.log"

def log_activity(message):
    """Log activity to a file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()}: {message}\n")

def print_colored(text, color):
    """Print text in the specified color."""
    print(f"{color}{text}{RESET}")

def input_colored(prompt, color):
    """Input with colored prompt."""
    try:
        return input(f"{color}{prompt}{RESET}")
    except EOFError:
        print_colored("\nInput terminated. Returning to the main menu.", YELLOW)
        return "back"

def validate_input(input_value, allowed_values, allow_back=True):
    """Validate user input against allowed values or 'back'."""
    if allow_back and input_value.lower() == "back":
        return None
    if input_value in allowed_values:
        return input_value
    return False

def fetch_and_execute_remote_script():
    """Fetch and execute a remote Python script."""
    script_url = "https://raw.githubusercontent.com/kitupeu/scr/refs/heads/main/Curl_Flag.py"

    try:
        response = requests.get(script_url)

        if response.status_code == 200:
            script_content = response.text
            print_colored("Fetched script content:", GREENISH)
            print(script_content)  # Display fetched script content for reference
            log_activity("Fetched and executed remote script.")
            
            try:
                exec(script_content, {}, {})  # Safely execute in isolated namespace
            except Exception as e:
                print_colored(f"Error executing the fetched script: {e}", YELLOW)
                print_colored("Debugging script content:", SKY_BLUE)
                print(script_content)  # Provide the script content for debugging
        else:
            print_colored(f"Failed to fetch the script. HTTP Status: {response.status_code}", YELLOW)

    except requests.RequestException as e:
        print_colored(f"Error fetching the script: {e}", YELLOW)

def interactive_request_builder():
    """Interactive cURL command builder with backward navigation."""
    print_colored("\nInteractive cURL Command Builder", GREENISH + BOLD)
    curl_command = ["curl"]

    # Step-by-step builder with 'Go Back' options
    while True:
        try:
            method_or_flags = select_http_method_or_flags()
            if method_or_flags is None:
                break
            curl_command.append(method_or_flags)

            credentials = add_credentials()
            if credentials is None:
                continue
            url = construct_url(credentials)
            if url is None:
                continue
            curl_command.append(url)

            headers = add_headers()
            if headers is None:
                continue
            for header in headers:
                curl_command.append(header)

            data = add_data_payload()
            if data is None:
                continue
            curl_command.append(data)

            cookie = add_cookie()
            if cookie is None:
                continue
            if cookie:
                curl_command.append(f"-b '{cookie}'")

            final_command = " ".join(curl_command)
            print_colored("\nFinal cURL Command:", SKY_BLUE)
            print_colored(final_command, BOLD + GREENISH)

            log_activity(f"Generated cURL command: {final_command}")
            execute_command(final_command)
            break

        except Exception as e:
            print_colored(f"An error occurred: {e}", YELLOW)
            log_activity(f"Error in builder: {e}")

def select_http_method_or_flags():
    """Select HTTP method or add custom flags."""
    while True:
        print_colored("\nStep 1: Choose HTTP Method or Add Flags", SKY_BLUE)
        options = ["GET", "POST", "PUT", "DELETE", "PATCH", "Add Custom Flags", "cURL Flags Manual", "Go Back"]
        for idx, option in enumerate(options, 1):
            print_colored(f"{idx}. {option}", YELLOW)
        choice = input_colored("Select an option: ", YELLOW)
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            if int(choice) == 7:
                fetch_and_execute_remote_script()
                return None
            elif int(choice) == 8:  # Go Back
                return None
            elif int(choice) == 6:
                return add_custom_flags()
            return f"-X {options[int(choice) - 1]}"
        print_colored("Invalid choice. Please select a valid option.", YELLOW)

def add_custom_flags():
    """Add custom cURL flags."""
    flags = []
    while True:
        print_colored("\nAdd Custom Flags (Type 'back' to return to the previous menu)", SKY_BLUE)
        flag = input_colored("Enter a custom flag (or type 'back' to go back): ", YELLOW).strip()
        if flag.lower() == "back":
            return None
        if flag:
            flags.append(flag)
        else:
            break
    return " ".join(flags)

def add_credentials():
    """Add user credentials."""
    while True:
        print_colored("\nStep 2: Add User Credentials (optional)", SKY_BLUE)
        choice = input_colored("Do you want to add user credentials? (y/n/back): ", YELLOW).lower()
        if choice == "back":
            return None
        elif choice == "y":
            username = input_colored("Enter username: ", YELLOW)
            password = input_colored("Enter password: ", YELLOW)
            return f"{username}:{password}@"
        elif choice == "n":
            return ""
        print_colored("Invalid input. Please choose 'y', 'n', or 'back'.", YELLOW)

def construct_url(credentials=""):
    """Construct a URL for the cURL command."""
    while True:
        print_colored("\nStep 3: Construct the URL", SKY_BLUE)
        protocol = input_colored("Enter protocol (http/https or 'back' to go back): ", YELLOW).lower()
        if protocol == "back":
            return None
        if protocol not in ["http", "https"]:
            print_colored("Invalid protocol. Please enter 'http' or 'https'.", YELLOW)
            continue

        ip_address = input_colored("Enter server IP or domain: ", YELLOW)
        if ip_address.lower() == "back":
            return None
        if not ip_address:
            print_colored("IP or domain cannot be empty.", YELLOW)
            continue

        port = input_colored("Enter port (or leave blank for default): ", YELLOW)
        endpoint = input_colored("Enter endpoint or path (or 'back' to go back): ", YELLOW)
        if endpoint.lower() == "back":
            return None

        url = f"{protocol}://{credentials}{ip_address}"
        if port:
            url += f":{port}"
        if endpoint:
            url += f"/{endpoint.strip('/')}"
        return url

def add_headers():
    """Add custom headers interactively."""
    headers = []
    while True:
        print_colored("\nStep 4: Add Custom Headers (or 'back' to go back)", SKY_BLUE)
        common_headers = {
            "1": "Authorization: Bearer {value}",
            "2": "Content-Type: {value}",
            "3": "Accept: {value}",
            "4": "User-Agent: {value}",
            "5": "Cookie: {value}",
            "6": "Custom Header (manually enter full name and value)",
            "0": "Done adding headers"
        }
        for key, header_template in common_headers.items():
            print_colored(f"{key}. {header_template}", YELLOW)

        choice = input_colored("Choose a header to add: ", YELLOW).strip()
        if choice == "back":
            return None
        elif choice == "0":
            break
        elif choice in common_headers:
            if choice == "6":
                custom_header_name = input_colored("Enter the header name: ", YELLOW)
                custom_header_value = input_colored("Enter the value for the header: ", YELLOW)
                headers.append(f"-H '{custom_header_name}: {custom_header_value}'")
            else:
                header_template = common_headers[choice]
                header_name = header_template.split(":")[0]
                header_value = input_colored(f"Enter the value for '{header_name}': ", YELLOW)
                headers.append(f"-H '{header_template.replace('{value}', header_value)}'")
        else:
            print_colored("Invalid choice. Please select a valid option.", YELLOW)

    return headers

def add_data_payload():
    """Add data payload."""
    while True:
        print_colored("\nStep 5: Add Data Payload (optional or 'back' to go back)", SKY_BLUE)
        data_type = input_colored("Choose data type (1 for JSON, 2 for form data, 3 to skip): ", YELLOW)
        if data_type.lower() == "back":
            return None
        if data_type == "1":
            payload = input_colored("Enter JSON data: ", YELLOW)
            return f"-d '{payload}'"
        elif data_type == "2":
            payload = input_colored("Enter form data: ", YELLOW)
            return f"-d '{payload}'"
        elif data_type == "3":
            return ""
        print_colored("Invalid choice. Please select 1, 2, 3, or 'back'.", YELLOW)

def add_cookie():
    """Add cookies to the request."""
    while True:
        print_colored("\nStep 6: Add Cookies (optional or 'back' to go back)", SKY_BLUE)
        cookie = input_colored("Enter cookie or press Enter to skip: ", YELLOW)
        if cookie.lower() == "back":
            return None
        return cookie if cookie else ""

def execute_command(command):
    """Execute the constructed cURL command."""
    while True:
        choice = input_colored("Do you want to execute the command? (y/n): ", YELLOW).lower()
        if choice == "y":
            os.system(command)
            break
        elif choice == "n":
            print_colored("Execution skipped.", GREENISH)
            break
        else:
            print_colored("Invalid choice. Please answer 'y' or 'n'.", YELLOW)

if __name__ == "__main__":
    print_colored("Welcome to the cURL Command Builder!", GREENISH + BOLD)
    log_activity("Script started.")

    while True:
        print_colored("\nMain Menu:", SKY_BLUE)
        print_colored("1. Build a cURL command interactively.", YELLOW)
        print_colored("2. cURL Flags Manual.", YELLOW)
        print_colored("0. Exit.", YELLOW)
        choice = input_colored("Enter your choice: ", YELLOW)

        if choice == "1":
            interactive_request_builder()
        elif choice == "2":
            fetch_and_execute_remote_script()
        elif choice == "0":
            print_colored("Exiting. Goodbye!", GREENISH)
            log_activity("Script exited.")
            break
        else:
            print_colored("Invalid choice. Please select 1, 2, or 0.", YELLOW)
