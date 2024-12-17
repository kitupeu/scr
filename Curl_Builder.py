import os
import subprocess
import readline
import requests
import base64
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
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def print_colored(text, color):
    """Print text in the specified color."""
    print(f"{color}{text}{RESET}")

def input_colored(prompt, color):
    """Input with colored prompt."""
    try:
        return input(f"{color}{prompt}{RESET}")
    except EOFError:
        print_colored("\nInput terminated. Returning to previous menu.", YELLOW)
        return None

def show_tutorial():
    """Display a tutorial for how to use the program."""
    print_colored("\n--- How to Use the cURL Command Builder ---", SKY_BLUE)
    print_colored("1. Follow each step to construct your URL and customize options.", YELLOW)
    print_colored("2. You can edit each component individually (scheme, host, port, etc.).", YELLOW)
    print_colored("3. Use the 'Finish and View URL' option to finalize your URL.", YELLOW)
    print_colored("4. Choose HTTP methods, headers, and other advanced options.", YELLOW)
    print_colored("5. Use templates and predictions to automate input based on prior data.", YELLOW)
    print_colored("6. Finally, execute the generated cURL command.", YELLOW)
    print_colored("\nEnjoy using the tool!", GREENISH)

def select_scheme():
    """Prompt user to select HTTP or HTTPS."""
    while True:
        print_colored("\nStep 1: Select Protocol (Scheme)", SKY_BLUE)
        print_colored("Example: http or https", GREENISH)
        print_colored("1. http", YELLOW)
        print_colored("2. https", YELLOW)
        print_colored("0. Go Back", YELLOW)
        choice = input_colored("Choose the protocol (0, 1, or 2): ", YELLOW)
        if choice == "1":
            return "http"
        elif choice == "2":
            return "https"
        elif choice == "0":
            return None  # Go back
        print_colored("Invalid choice. Please enter 0, 1, or 2.", YELLOW)

def add_user_info():
    """Prompt user to add credentials (optional)."""
    print_colored("\nStep 2: Add User Info (Optional Credentials)", SKY_BLUE)
    print_colored("Example: admin:admin@", GREENISH)
    print_colored("Press Enter to skip this step.", YELLOW)

    username = input_colored("Enter username (or press Enter to skip): ", YELLOW).strip()
    if not username:  # Skip if username is empty
        return ""
    password = input_colored("Enter password: ", YELLOW).strip()
    if password:
        return f"{username}:{password}@"
    else:
        print_colored("Password cannot be empty. Skipping User Info.", YELLOW)
        return ""

def input_host():
    """Prompt user to enter the host (domain or IP)."""
    while True:
        print_colored("\nStep 3: Enter Host (Domain or IP)", SKY_BLUE)
        print_colored("Example: kitup.eu or 192.168.1.1", GREENISH)
        host = input_colored("Enter domain name or IP address: ", YELLOW).strip()
        if host:
            return host.strip()
        print_colored("Host cannot be empty.", YELLOW)

def select_port(scheme):
    """Prompt user to enter port, defaulting based on scheme."""
    while True:
        print_colored("\nStep 4: Enter Port Number (Optional)", SKY_BLUE)
        print_colored("Example: :80 for HTTP or :443 for HTTPS", GREENISH)
        default_port = "443" if scheme == "https" else "80"
        port = input_colored(f"Enter port number (default {default_port}): ", YELLOW).strip()
        if not port:
            return f":{default_port}"
        if port.isdigit():
            return f":{port}"
        print_colored("Invalid input. Port must be numeric.", YELLOW)

def input_path():
    """Prompt user to enter path."""
    print_colored("\nStep 5: Enter Path", SKY_BLUE)
    print_colored("Example: /index.php or /dashboard", GREENISH)
    path = input_colored("Enter path: ", YELLOW).strip()
    return f"/{path.strip('/')}" if path else ""

def add_query_string():
    """Prompt user to add query string."""
    print_colored("\nStep 6: Add Query String", SKY_BLUE)
    print_colored("Example: ?search=flag", GREENISH)
    query = input_colored("Enter query string: ", YELLOW).strip()
    return f"?{query}" if query and not query.startswith("?") else query

def add_fragment():
    """Prompt user to add a fragment."""
    print_colored("\nStep 7: Add Fragment", SKY_BLUE)
    print_colored("Example: #section1", GREENISH)
    fragment = input_colored("Enter fragment: ", YELLOW).strip()
    return f"#{fragment}" if fragment else ""

def construct_url():
    """Construct and edit the URL step-by-step."""
    scheme = "http"
    user_info = ""
    host = ""
    port = ""
    path = ""
    query_string = ""
    fragment = ""

    while True:
        print_colored("\n--- URL Builder Menu ---", SKY_BLUE)
        print_colored(f"1. Scheme (http/https): {scheme}", YELLOW)
        print_colored(f"2. User Info (username:password): {user_info}", YELLOW)
        print_colored(f"3. Host (Domain/IP): {host}", YELLOW)
        print_colored(f"4. Port: {port}", YELLOW)
        print_colored(f"5. Path: {path}", YELLOW)
        print_colored(f"6. Query String: {query_string}", YELLOW)
        print_colored(f"7. Fragment: {fragment}", YELLOW)
        print_colored("8. Finish and View URL", GREENISH)
        print_colored("0. Go Back to Main Menu", YELLOW)

        choice = input_colored("Select a component to edit (0-8): ", YELLOW)

        if choice == "1":
            scheme = select_scheme() or scheme
        elif choice == "2":
            user_info = add_user_info()
        elif choice == "3":
            host = input_host()
        elif choice == "4":
            port = select_port(scheme)
        elif choice == "5":
            path = input_path()
        elif choice == "6":
            query_string = add_query_string()
        elif choice == "7":
            fragment = add_fragment()
        elif choice == "8":
            url = f"{scheme}://{user_info}{host}{port}{path}{query_string}{fragment}"
            print_colored(f"Constructed URL: {url}", GREENISH + BOLD)
            return url
        elif choice == "0":
            return None

if __name__ == "__main__":
    print_colored("Welcome to the Ultimate cURL Command Builder!", GREENISH + BOLD)
    log_activity("Script started.")
    while True:
        print_colored("\n--- Main Menu ---", SKY_BLUE)
        print_colored("1. Build URL", YELLOW)
        print_colored("2. Show Tutorial", YELLOW)
        print_colored("0. Exit", YELLOW)

        choice = input_colored("Enter choice: ", YELLOW)
        if choice == "1":
            construct_url()
        elif choice == "2":
            show_tutorial()
        elif choice == "0":
            print_colored("Goodbye!", GREENISH)
            break
