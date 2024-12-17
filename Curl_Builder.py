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



def input_path():
    """Prompt user to enter path."""
    print_colored("\nStep 5: Enter Path", SKY_BLUE)
    print_colored("Example: /index.php or /dashboard", GREENISH)
    print_colored("Press Enter to skip this step (default to root).", YELLOW)

    path = input_colored("Enter path (e.g., /index.php): ", YELLOW).strip()
    return f"/{path.strip('/')}" if path else ""


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
    print_colored("Press Enter to skip this step.", YELLOW)

    while True:
        param = input_colored("Enter parameter name (or press Enter to finish): ", YELLOW).strip()
        if not param:  # If user presses Enter without input, finish this step
            break
        value = input_colored(f"Enter value for '{param}': ", YELLOW).strip()
        if value:
            query_params.append(f"{param}={value}")
        else:
            print_colored("Value cannot be empty. Try again.", YELLOW)

    return f"?{'&'.join(query_params)}" if query_params else ""


def add_fragment():
    """Prompt user to add a fragment (optional)."""
    print_colored("\nStep 7: Add Fragment (Optional)", SKY_BLUE)
    print_colored("Example: #section1", GREENISH)
    print_colored("Press Enter to skip this step.", YELLOW)

    fragment = input_colored("Enter fragment (e.g., #section1): ", YELLOW).strip()
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
            # Assemble the final URL
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
    """Prompt user to add custom cURL flags."""
    flags = []
    print_colored("\nStep 10: Add Custom Flags (Optional)", SKY_BLUE)
    print_colored("Example: --verbose, --insecure, --proxy http://proxy:8080", GREENISH)
    print_colored("Press Enter to finish this step.", YELLOW)

    while True:
        flag = input_colored("Enter a custom flag (or press Enter to finish): ", YELLOW).strip()
        if not flag:  # If user presses Enter, finish adding flags
            break
        flags.append(flag)

    return " ".join(flags) if flags else ""



def generate_authorization(username, password):
    """Generate a Base64-encoded Authorization header."""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Authorization: Basic {encoded_credentials}"

def assemble_curl_command(url, user_info, http_method, custom_flags, headers, data, save_file):
    """Assemble the full cURL command."""
    curl_command = ["curl"]

    # Verbose mode
    verbose = input_colored("Enable verbose mode? (y/n): ", YELLOW).strip().lower()
    if verbose == "y":
        curl_command.append("-v")

    # HTTP Method
    if http_method:
        curl_command.append(http_method)

    # Authorization Header (if user_info provided)
    if user_info:
        username, password = user_info.split(":")
        auth_header = generate_authorization(username, password)
        curl_command.append(f"-H '{auth_header}'")

    # Custom Headers
    for header in headers:
        curl_command.append(f"-H '{header}'")

    # Data Payload
    if data:
        curl_command.append(f"-d '{data}'")

    # Custom Flags
    if custom_flags:
        curl_command.append(custom_flags)

    # Save Response to File
    if save_file:
        curl_command.append(f"-o {save_file}")

    # Final URL
    curl_command.append(f"'{url}'")

    return " ".join(curl_command)


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
    print_colored("Welcome to the Ultimate cURL Command Builder!", GREENISH + BOLD)
    log_activity("Script started.")

    while True:
        print_colored("\n--- Main Menu ---", SKY_BLUE)
        print_colored("1. Build and Execute cURL Command.", YELLOW)
        print_colored("2. Exit.", YELLOW)

        choice = input_colored("Enter your choice: ", YELLOW)

        if choice == "1":
            # Step 1: Construct URL
            url = construct_url()
            if not url:
                continue

            # Step 2: Select HTTP Method
            http_method = select_http_method()
            if http_method is None:
                continue

            # Step 3: Add Custom Flags
            custom_flags = add_custom_flags()
            if custom_flags is None:
                continue

            # Step 4: Add Headers
            headers = []
            while True:
                header = input_colored("Enter a custom header (or 'done' to finish): ", YELLOW).strip()
                if header.lower() == "done":
                    break
                if header:
                    headers.append(header)

            # Step 5: Add Data Payload
            data = input_colored("Enter data payload (leave blank if none): ", YELLOW).strip()

            # Step 6: Save Response to File
            save_file = input_colored("Enter file name to save response (leave blank if none): ", YELLOW).strip()

            # Step 7: Assemble and Display Command
            curl_command = assemble_curl_command(url, user_info, http_method, custom_flags, headers, data, save_file)
            print_colored("\nGenerated cURL Command:", SKY_BLUE)
            print_colored(curl_command, BOLD + GREENISH)

            # Step 8: Execute Command
            execute_choice = input_colored("Do you want to execute this command? (y/n): ", YELLOW).strip().lower()
            if execute_choice == "y":
                try:
                    subprocess.run(curl_command, shell=True, check=True, text=True)
                    print_colored("Command executed successfully.", GREENISH)
                except subprocess.CalledProcessError as e:
                    print_colored(f"Error executing the command: {e}", YELLOW)
                log_activity(f"Executed Command: {curl_command}")
            else:
                print_colored("Command execution skipped.", YELLOW)
        elif choice == "2":
            print_colored("Exiting. Goodbye!", GREENISH)
            log_activity("Script exited.")
            break
        else:
            print_colored("Invalid choice. Please enter 1 or 2.", YELLOW)



