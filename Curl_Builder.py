import os
import subprocess
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
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def print_colored(text, color):
    """Print text in the specified color."""
    print(f"{color}{text}{RESET}")

def input_colored(prompt, color):
    """Input with colored prompt."""
    try:
        return input(f"{color}{prompt}{RESET}")
    except EOFError:
        print_colored("\nInput terminated. Exiting script.", YELLOW)
        exit(0)

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
    while True:
        print_colored("\nStep 2: Add User Info (Optional Credentials)", SKY_BLUE)
        print_colored("Example: admin:admin@", GREENISH)
        print_colored("1. Add credentials (username:password)", YELLOW)
        print_colored("2. Skip this step", YELLOW)
        print_colored("0. Go Back", YELLOW)
        choice = input_colored("Choose an option (0, 1, or 2): ", YELLOW)
        if choice == "1":
            username = input_colored("Enter username: ", YELLOW).strip()
            password = input_colored("Enter password: ", YELLOW).strip()
            if username and password:
                return f"{username}:{password}@"
            print_colored("Invalid input. Both username and password are required.", YELLOW)
        elif choice == "2":
            return ""
        elif choice == "0":
            return None  # Go back
        print_colored("Invalid choice. Please enter 0, 1, or 2.", YELLOW)


def input_host():
    """Prompt user to enter the host (domain or IP)."""
    while True:
        print_colored("\nStep 3: Enter Host (Domain or IP)", SKY_BLUE)
        print_colored("Example: kitup.eu or 192.168.1.1", GREENISH)
        print_colored("0. Go Back", YELLOW)
        host = input_colored("Enter domain name or IP address (or '0' to Go Back): ", YELLOW).strip()
        if host == "0":
            return None  # Go back
        if host:
            return host
        print_colored("Host cannot be empty. Please enter a valid domain or IP.", YELLOW)

def select_port(scheme):
    """Prompt user to enter port, defaulting based on scheme."""
    while True:
        print_colored("\nStep 4: Enter Port Number (Optional)", SKY_BLUE)
        print_colored("Example: :80 for HTTP or :443 for HTTPS", GREENISH)
        print_colored("0. Go Back", YELLOW)
        default_port = "443" if scheme == "https" else "80"
        port = input_colored(f"Enter port number (Press Enter for default {default_port} or '0' to Go Back): ", YELLOW).strip()
        if port == "0":
            return None  # Go back
        if not port:
            return f":{default_port}"
        if port.isdigit():
            return f":{port}"
        print_colored("Invalid input. Port must be a numeric value.", YELLOW)


def input_path():
    """Prompt user to enter path."""
    while True:
        print_colored("\nStep 5: Enter Path", SKY_BLUE)
        print_colored("Example: /index.php or /dashboard", GREENISH)
        print_colored("0. Go Back", YELLOW)
        path = input_colored("Enter path (e.g., /index.php) or '0' to Go Back: ", YELLOW).strip()
        if path == "0":
            return None  # Go back
        return f"/{path.strip('/')}" if path else ""

def add_query_string():
    """Prompt user to add query parameters (optional)."""
    query_params = []
    print_colored("\nStep 6: Add Query String (Optional)", SKY_BLUE)
    print_colored("Example: ?user=admin&status=active", GREENISH)
    print_colored("Type 'done' to finish or '0' to Go Back", YELLOW)
    while True:
        param = input_colored("Enter parameter name: ", YELLOW).strip()
        if param.lower() == "0":
            return None  # Go back
        if param.lower() == "done":
            break
        value = input_colored(f"Enter value for '{param}': ", YELLOW).strip()
        if param and value:
            query_params.append(f"{param}={value}")
        else:
            print_colored("Both parameter name and value are required.", YELLOW)
    return f"?{'&'.join(query_params)}" if query_params else ""


def add_fragment():
    """Prompt user to add a fragment (optional)."""
    while True:
        print_colored("\nStep 7: Add Fragment (Optional)", SKY_BLUE)
        print_colored("Example: #section1", GREENISH)
        print_colored("0. Go Back", YELLOW)
        fragment = input_colored("Enter fragment (e.g., #section1) or '0' to Go Back: ", YELLOW).strip()
        if fragment == "0":
            return None  # Go back
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
            user_info = add_user_info() or user_info
        elif choice == "3":
            host = input_host() or host
        elif choice == "4":
            port = select_port(scheme) or port
        elif choice == "5":
            path = input_path() or path
        elif choice == "6":
            query_string = add_query_string() or query_string
        elif choice == "7":
            fragment = add_fragment() or fragment
        elif choice == "8":
            url = f"{scheme}://{user_info}{host}{port}{path}{query_string}{fragment}"
            print_colored("\nConstructed URL:", SKY_BLUE)
            print_colored(url, BOLD + GREENISH)
            return url
        elif choice == "0":
            return None  # Go back to the main menu
        else:
            print_colored("Invalid choice. Please enter a number between 0 and 8.", YELLOW)

def select_http_method():
    """Prompt user to select HTTP method, including an option for no method."""
    while True:
        print_colored("\nStep 8: Select HTTP Method", SKY_BLUE)
        print_colored("Example: GET, POST, PUT, DELETE, PATCH", GREENISH)
        print_colored("1. GET", YELLOW)
        print_colored("2. POST", YELLOW)
        print_colored("3. PUT", YELLOW)
        print_colored("4. DELETE", YELLOW)
        print_colored("5. PATCH", YELLOW)
        print_colored("6. Plain Method (No HTTP method)", YELLOW)
        print_colored("0. Go Back", YELLOW)

        choice = input_colored("Choose a method (0-6): ", YELLOW)
        if choice == "1":
            return "-X GET"
        elif choice == "2":
            return "-X POST"
        elif choice == "3":
            return "-X PUT"
        elif choice == "4":
            return "-X DELETE"
        elif choice == "5":
            return "-X PATCH"
        elif choice == "6":
            print_colored("Proceeding without specifying an HTTP method.", GREENISH)
            return ""  # Plain method: no HTTP method
        elif choice == "0":
            return None  # Go back
        print_colored("Invalid choice. Please enter a number between 0 and 6.", YELLOW)

def add_custom_flags():
    """Prompt user to add custom cURL flags, including a plain option and Go Back."""
    flags = []
    print_colored("\nStep 9: Add Custom Flags (Optional)", SKY_BLUE)
    print_colored("Example: -H 'Content-Type: application/json', -d 'key=value', --verbose", GREENISH)
    print_colored("Type 'done' when finished, '0' to Go Back, or leave blank for no flags.", YELLOW)

    while True:
        flag = input_colored("Enter a custom flag (or 'done' to finish, '0' to Go Back): ", YELLOW).strip()
        if flag.lower() == "0":
            return None  # Go back
        elif flag.lower() == "done":
            break  # Finish adding flags
        elif not flag:
            print_colored("Proceeding with no custom flags.", GREENISH)
            break  # Plain option: no flags
        else:
            flags.append(flag)

    return " ".join(flags) if flags else ""  # Combine all flags into one string


def execute_command(command):
    """Execute the constructed Linux command."""
    while True:
        choice = input_colored("Do you want to execute this command? (y/n): ", YELLOW).lower()
        if choice == "y":
            try:
                subprocess.run(command, shell=True, check=True, text=True)
                print_colored("Command executed successfully.", GREENISH)
            except subprocess.CalledProcessError as e:
                print_colored(f"Error executing the command: {e}", YELLOW)
            break
        elif choice == "n":
            print_colored("Command execution skipped.", YELLOW)
            break
        else:
            print_colored("Invalid choice. Please enter 'y' or 'n'.", YELLOW)

if __name__ == "__main__":
    print_colored("Welcome to the Linux Command Generator!", GREENISH + BOLD)
    log_activity("Script started.")

    while True:
        print_colored("\n--- Main Menu ---", SKY_BLUE)
        print_colored("1. Build a cURL command.", YELLOW)
        print_colored("2. Exit.", YELLOW)

        choice = input_colored("Enter your choice: ", YELLOW)

        if choice == "1":
            # Step 1: Construct URL
            url = construct_url()
            if not url:  # Go back handling
                continue

            # Step 2: Select HTTP method
            http_method = select_http_method()
            if http_method is None:  # Go back handling
                continue

            # Step 3: Add custom flags
            custom_flags = add_custom_flags()
            if custom_flags is None:  # Go back handling
                continue

            # Step 4: Assemble the full cURL command
            curl_command = f"curl {http_method} {custom_flags} '{url}'"
            print_colored("\nGenerated cURL Command:", SKY_BLUE)
            print_colored(curl_command, BOLD + GREENISH)

            # Log and optionally execute
            log_activity(f"Generated Command: {curl_command}")
            execute_command(curl_command)
        elif choice == "2":
            print_colored("Exiting. Goodbye!", GREENISH)
            log_activity("Script exited.")
            break
        else:
            print_colored("Invalid choice. Please enter 1 or 2.", YELLOW)


