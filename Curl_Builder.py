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
        print_colored("1. http", YELLOW)
        print_colored("2. https", YELLOW)
        choice = input_colored("Choose the protocol (1 or 2): ", YELLOW)
        if choice == "1":
            return "http"
        elif choice == "2":
            return "https"
        print_colored("Invalid choice. Please enter 1 or 2.", YELLOW)

def add_user_info():
    """Prompt user to add credentials (optional)."""
    while True:
        print_colored("\nStep 2: Add User Info (Optional Credentials)", SKY_BLUE)
        print_colored("1. Add credentials (username:password)", YELLOW)
        print_colored("2. Skip this step", YELLOW)
        choice = input_colored("Choose an option (1 or 2): ", YELLOW)
        if choice == "1":
            username = input_colored("Enter username: ", YELLOW).strip()
            password = input_colored("Enter password: ", YELLOW).strip()
            if username and password:
                return f"{username}:{password}@"
            print_colored("Invalid input. Both username and password are required.", YELLOW)
        elif choice == "2":
            return ""
        print_colored("Invalid choice. Please enter 1 or 2.", YELLOW)

def input_host():
    """Prompt user to enter the host (domain or IP)."""
    while True:
        print_colored("\nStep 3: Enter Host (Domain or IP)", SKY_BLUE)
        host = input_colored("Enter domain name or IP address: ", YELLOW).strip()
        if host:
            return host
        print_colored("Host cannot be empty. Please enter a valid domain or IP.", YELLOW)

def select_port(scheme):
    """Prompt user to enter port, defaulting based on scheme."""
    while True:
        print_colored("\nStep 4: Enter Port Number (Optional)", SKY_BLUE)
        default_port = "443" if scheme == "https" else "80"
        port = input_colored(f"Enter port number (Press Enter for default {default_port}): ", YELLOW).strip()
        if not port:
            return f":{default_port}"
        if port.isdigit():
            return f":{port}"
        print_colored("Invalid input. Port must be a numeric value.", YELLOW)

def input_path():
    """Prompt user to enter path."""
    while True:
        print_colored("\nStep 5: Enter Path", SKY_BLUE)
        path = input_colored("Enter path (e.g., /dashboard.php) or leave blank for root: ", YELLOW).strip()
        return f"/{path.strip('/')}" if path else ""

def add_query_string():
    """Prompt user to add query parameters (optional)."""
    query_params = []
    print_colored("\nStep 6: Add Query String (Optional)", SKY_BLUE)
    while True:
        param = input_colored("Enter parameter name (or type 'done' to finish): ", YELLOW).strip()
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
    print_colored("\nStep 7: Add Fragment (Optional)", SKY_BLUE)
    fragment = input_colored("Enter fragment (e.g., status) or leave blank: ", YELLOW).strip()
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
        print_colored("1. Scheme (http/https): " + scheme, YELLOW)
        print_colored("2. User Info (username:password): " + user_info, YELLOW)
        print_colored("3. Host (Domain/IP): " + host, YELLOW)
        print_colored("4. Port: " + port, YELLOW)
        print_colored("5. Path: " + path, YELLOW)
        print_colored("6. Query String: " + query_string, YELLOW)
        print_colored("7. Fragment: " + fragment, YELLOW)
        print_colored("8. Finish and View URL", GREENISH)
        
        choice = input_colored("Select a component to edit (1-8): ", YELLOW)
        
        if choice == "1":
            scheme = select_scheme()
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
            # Assemble the final URL
            url = f"{scheme}://{user_info}{host}{port}{path}{query_string}{fragment}"
            print_colored("\nConstructed URL:", SKY_BLUE)
            print_colored(url, BOLD + GREENISH)
            return url
        else:
            print_colored("Invalid choice. Please enter a number between 1 and 8.", YELLOW)
def select_http_method():
    """Prompt user to select HTTP method."""
    while True:
        print_colored("\nSelect HTTP Method:", SKY_BLUE)
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        for idx, method in enumerate(methods, 1):
            print_colored(f"{idx}. {method}", YELLOW)
        choice = input_colored("Choose a method (1-5): ", YELLOW)
        if choice.isdigit() and 1 <= int(choice) <= len(methods):
            return f"-X {methods[int(choice) - 1]}"
        print_colored("Invalid choice. Please enter a number between 1 and 5.", YELLOW)

def add_custom_flags():
    """Prompt user to add custom cURL flags."""
    flags = []
    print_colored("\nAdd Custom Flags (e.g., -H, -d, --verbose). Type 'done' when finished:", SKY_BLUE)
    while True:
        flag = input_colored("Enter flag (or 'done' to finish): ", YELLOW).strip()
        if flag.lower() == "done":
            break
        if flag:
            flags.append(flag)
        else:
            print_colored("Flag cannot be empty. Try again.", YELLOW)
    return " ".join(flags)

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
            
            # Step 2: Select HTTP method
            http_method = select_http_method()
            
            # Step 3: Add custom flags
            custom_flags = add_custom_flags()
            
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


