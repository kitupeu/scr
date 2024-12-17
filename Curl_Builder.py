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
    print_colored("This tool will help you build a cURL command step-by-step:", YELLOW)
    print_colored("1. Scheme (http/https): Select the protocol. Example: http", GREENISH)
    print_colored("2. User Info: Optional credentials. Example: admin:admin@", GREENISH)
    print_colored("3. Host: Domain name or IP address. Example: 192.168.1.1", GREENISH)
    print_colored("4. Port: Optional port number. Example: :443", GREENISH)
    print_colored("5. Path: URL path. Example: /index.php", GREENISH)
    print_colored("6. Query String: Optional query parameters. Example: ?search=flag", GREENISH)
    print_colored("7. Fragment: Optional fragment. Example: #section1", GREENISH)
    print_colored("8. HTTP Method: Select a method like GET, POST, PUT, DELETE, etc.", GREENISH)
    print_colored("9. Headers: Add custom headers to your request.", GREENISH)
    print_colored("10. Data Payload: Include JSON or form data in the request.", GREENISH)
    print_colored("11. Custom Flags: Add additional cURL flags like --verbose or --insecure.", GREENISH)
    print_colored("12. Save Response: Option to save the response to a file.", GREENISH)
    print_colored("\nYou can skip any question by pressing Enter. At the end, you can view, edit, or execute the command.", YELLOW)
    print_colored("\nEnjoy using the tool!", GREENISH)

def select_http_method():
    """Prompt user to select an HTTP method."""
    print_colored("\nStep 8 - Select HTTP Method", SKY_BLUE)
    print_colored("Example: GET, POST, PUT, DELETE, PATCH", GREENISH)
    print_colored("1. GET", YELLOW)
    print_colored("2. POST", YELLOW)
    print_colored("3. PUT", YELLOW)
    print_colored("4. DELETE", YELLOW)
    print_colored("5. PATCH", YELLOW)
    print_colored("6. No HTTP Method", YELLOW)

    while True:
        choice = input_colored("Choose an HTTP method (1-6): ", YELLOW).strip()
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
            return ""
        else:
            print_colored("Invalid choice. Please enter a number between 1 and 6.", YELLOW)

def add_custom_headers():
    """Prompt user to add custom headers interactively."""
    headers = []
    print_colored("\nStep 9 - Add Custom Headers", SKY_BLUE)
    print_colored("Example: User-Agent: curl/7.77.0 or Authorization: Bearer <token>", GREENISH)
    print_colored("Press Enter to finish this step.", YELLOW)

    while True:
        header = input_colored("Enter a header (or press Enter to finish): ", YELLOW).strip()
        if not header:
            break
        headers.append(f"-H '{header}'")

    return " ".join(headers)

def add_data_payload():
    """Prompt user to add data payload."""
    print_colored("\nStep 10 - Add Data Payload", SKY_BLUE)
    print_colored("Example: {\"key\": \"value\"} for JSON or key=value for form data", GREENISH)
    print_colored("Press Enter to skip this step.", YELLOW)
    data = input_colored("Enter data payload: ", YELLOW).strip()
    return f"-d '{data}'" if data else ""

def add_custom_flags():
    """Prompt user to add custom cURL flags."""
    flags = []
    print_colored("\nStep 11 - Add Custom Flags", SKY_BLUE)
    print_colored("Example: --verbose, --insecure, --proxy http://proxy:8080", GREENISH)
    print_colored("Press Enter to finish this step.", YELLOW)

    while True:
        flag = input_colored("Enter a custom flag (or press Enter to finish): ", YELLOW).strip()
        if not flag:
            break
        flags.append(flag)

    return " ".join(flags)

def save_response_file():
    """Prompt user to specify a file to save the response."""
    print_colored("\nStep 12 - Save Response to File", SKY_BLUE)
    file_name = input_colored("Enter file name to save response (or press Enter to skip): ", YELLOW).strip()
    return f"-o {file_name}" if file_name else ""

def construct_url():
    """Ask questions continuously to construct the URL step-by-step."""
    print_colored("\nAnswer the following questions to build your URL. Press Enter to skip any question.", SKY_BLUE)
    
    # Initialize variables
    scheme = "http"
    user_info = ""
    host = ""
    port = ""
    path = ""
    query_string = ""
    fragment = ""

    print_colored("\nStep 1 - Scheme (http/https)", YELLOW)
    scheme = input_colored("Example: http or https [Default: http]: ", YELLOW).strip() or "http"

    print_colored("\nStep 2 - User Info (username:password)", YELLOW)
    user_info = input_colored("Example: admin:admin@ (Press Enter to skip): ", YELLOW).strip()

    print_colored("\nStep 3 - Host (Domain/IP)", YELLOW)
    while not host:
        host = input_colored("Example: 192.168.1.1 or example.com: ", YELLOW).strip()
        if not host:
            print_colored("Host cannot be empty. Please provide a valid domain or IP.", YELLOW)

    print_colored("\nStep 4 - Port", YELLOW)
    port = input_colored("Example: :443 (Press Enter to skip): ", YELLOW).strip()
    port = f":{port}" if port else ""

    print_colored("\nStep 5 - Path", YELLOW)
    path = input_colored("Example: /index.php (Press Enter to skip): ", YELLOW).strip()
    path = f"/{path.strip('/')}" if path else ""

    print_colored("\nStep 6 - Query String", YELLOW)
    query_string = input_colored("Example: ?search=flag (Press Enter to skip): ", YELLOW).strip()
    if query_string and not query_string.startswith("?"):
        query_string = f"?{query_string}"

    print_colored("\nStep 7 - Fragment", YELLOW)
    fragment = input_colored("Example: #section1 (Press Enter to skip): ", YELLOW).strip()
    fragment = f"#{fragment}" if fragment else ""

    return f"{scheme}://{user_info}{host}{port}{path}{query_string}{fragment}"

def assemble_curl_command():
    """Assemble the full cURL command with all options."""
    url = construct_url()
    http_method = select_http_method()
    headers = add_custom_headers()
    data_payload = add_data_payload()
    custom_flags = add_custom_flags()
    save_file = save_response_file()

    curl_command = "curl"
    if http_method:
        curl_command += f" {http_method}"
    if headers:
        curl_command += f" {headers}"
    if data_payload:
        curl_command += f" {data_payload}"
    if custom_flags:
        curl_command += f" {custom_flags}"
    if save_file:
        curl_command += f" {save_file}"
    curl_command += f" '{url}'"

    return curl_command

def main_menu():
    """Main menu to navigate and manage options."""
    while True:
        print_colored("\n--- Main Menu ---", SKY_BLUE)
        print_colored("1. Build and Execute cURL Command.", YELLOW)
        print_colored("2. Tutorial: How to Use the Tool.", YELLOW)
        print_colored("0. Exit.", YELLOW)
        choice = input_colored("Enter your choice: ", YELLOW)

        if choice == "1":
            curl_command = assemble_curl_command()
            print_colored("\nGenerated cURL Command:", SKY_BLUE)
            print_colored(curl_command, BOLD + GREENISH)

            execute = input_colored("\nDo you want to execute this command? (y/n): ", YELLOW).lower()
            if execute == "y":
                log_activity(f"Executed Command: {curl_command}")
                subprocess.run(curl_command, shell=True)
            else:
                print_colored("Command execution skipped.", YELLOW)
        elif choice == "2":
            show_tutorial()
        elif choice == "0":
            print_colored("Exiting. Goodbye!", GREENISH)
            break
        else:
            print_colored("Invalid choice. Please enter 0, 1, or 2.", YELLOW)

if __name__ == "__main__":
    print_colored("Welcome to the Ultimate cURL Command Builder!", GREENISH + BOLD)
    log_activity("Script started.")
    main_menu()
