import os
import subprocess
import readline
import requests
import base64
from datetime import datetime
import time
import sys
import tty
import termios

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

def print_progress(message):
    """Print progress updates."""
    print_colored(f"[Progress] {message}...", GREENISH)
    time.sleep(0.5)  # Simulate a small delay for visual effect

def get_arrow_key():
    """Detect UP or DOWN arrow keys."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':  # ESC sequence
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            if ch2 == '[' and ch3 == 'A':
                return "UP"
            elif ch2 == '[' and ch3 == 'B':
                return "DOWN"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None


def print_progress(message):
    """Print progress updates."""
    print_colored(f"[Progress] {message}...", GREENISH)
    time.sleep(0.5)  # Simulate a small delay for visual effect

def show_tutorial():
    """Display a tutorial for how to use the program."""
    print_colored("\n--- How to Use the cURL Command Builder ---", SKY_BLUE)
    steps = [
        "1. Scheme (http/https): Select the protocol. Example: http",
        "2. User Info: Optional credentials. Example: admin:admin@",
        "3. Host: Domain name or IP address. Example: 192.168.1.1",
        "4. Port: Optional port number. Example: :443",
        "5. Path: URL path. Example: /index.php",
        "6. Query String: Optional query parameters. Example: ?search=flag",
        "7. Fragment: Optional fragment. Example: #section1",
        "8. HTTP Method: Select a method like GET, POST, PUT, DELETE, etc.",
        "9. Headers: Add custom headers to your request.",
        "10. Data Payload: Include JSON or form data in the request.",
        "11. Custom Flags: Add additional cURL flags like --verbose or --insecure.",
        "12. Save Response: Option to save the response to a file."
    ]
    for step in steps:
        print_colored(step, GREENISH)
    print_colored("\nPress Enter to skip any question or type 'back' to return to the previous step.", YELLOW)

def go_back_option(current_step):
    """Ask user if they want to go back to a previous step."""
    while True:
        go_back = input_colored("Would you like to go back to the previous step? (y/n): ", YELLOW).strip().lower()
        if go_back == 'y':
            return current_step - 1
        elif go_back == 'n':
            return current_step
        else:
            print_colored("Invalid choice. Please enter 'y' or 'n'.", YELLOW)

def construct_url():
    """Construct the URL step-by-step with UP/DOWN arrow navigation."""
    print_colored("\nAnswer the following questions to build your URL. Press Enter to accept defaults.", SKY_BLUE)

    steps = [
        {"name": "Scheme", "example": "http or https", "default": "http"},
        {"name": "User Info", "example": "admin:admin@", "default": ""},
        {"name": "Host", "example": "example.com or 192.168.1.1", "default": ""},
        {"name": "Port", "example": ":443", "default": ""},
        {"name": "Path", "example": "/index.php", "default": ""},
        {"name": "Query String", "example": "?search=flag", "default": ""},
        {"name": "Fragment", "example": "#section1", "default": ""},
    ]
    answers = [""] * len(steps)
    current_step = 0

    while current_step < len(steps):
        # Display step info
        step = steps[current_step]
        print_progress(f"Step {current_step + 1}: {step['name']}")
        print_colored(f"Example: {step['example']}", GREENISH)

        # Show previous value or default
        previous_value = answers[current_step] or step["default"]
        user_input = input_colored(f"Enter value [{previous_value}]: ", YELLOW).strip()
        answers[current_step] = user_input if user_input else previous_value

        # Detect navigation with arrow keys
        key = get_arrow_key()
        if key == "UP" and current_step > 0:
            current_step -= 1
        elif key == "DOWN" and current_step < len(steps) - 1:
            current_step += 1
        else:
            current_step += 1

    # Assemble URL
    url = f"{answers[0]}://{answers[1]}{answers[2]}{answers[3]}{answers[4]}{answers[5]}{answers[6]}"
    print_colored("\nConstructed URL:", SKY_BLUE)
    print_colored(url, BOLD + GREENISH)
    return url

def select_http_method():
    """Prompt user to select an HTTP method."""
    print_colored("\nStep 8 - Select HTTP Method", SKY_BLUE)
    print_colored("1. GET", YELLOW)
    print_colored("2. POST", YELLOW)
    print_colored("3. PUT", YELLOW)
    print_colored("4. DELETE", YELLOW)
    print_colored("5. PATCH", YELLOW)
    print_colored("6. No HTTP Method", YELLOW)

    while True:
        choice = input_colored("Choose an HTTP method (1-6): ", YELLOW).strip()
        if choice == "1": return "-X GET"
        elif choice == "2": return "-X POST"
        elif choice == "3": return "-X PUT"
        elif choice == "4": return "-X DELETE"
        elif choice == "5": return "-X PATCH"
        elif choice == "6": return ""
        else: print_colored("Invalid choice. Please enter 1-6.", YELLOW)

def add_custom_headers():
    headers = []
    while True:
        header = input_colored("Enter header (or press Enter to finish): ", YELLOW).strip()
        if not header: break
        headers.append(f"-H '{header}'")
    return " ".join(headers)

def add_data_payload():
    data = input_colored("Enter data payload (e.g., JSON or form data): ", YELLOW).strip()
    return f"-d '{data}'" if data else ""

def add_custom_flags():
    flags = []
    while True:
        flag = input_colored("Enter a flag (or press Enter to finish): ", YELLOW).strip()
        if not flag: break
        flags.append(flag)
    return " ".join(flags)

def save_response_file():
    file_name = input_colored("Save response to file (or press Enter to skip): ", YELLOW).strip()
    return f"-o {file_name}" if file_name else ""


def assemble_curl_command():
    """Assemble the full cURL command with all options."""
    url = construct_url()
    print_progress("Selecting HTTP Method")
    http_method = select_http_method()
    print_progress("Adding Custom Headers")
    headers = add_custom_headers()
    print_progress("Adding Data Payload")
    data_payload = add_data_payload()
    print_progress("Adding Custom Flags")
    custom_flags = add_custom_flags()
    print_progress("Saving Response File")
    save_file = save_response_file()

    curl_command = "curl"
    for option in [http_method, headers, data_payload, custom_flags, save_file, f"'{url}'"]:
        if option:
            curl_command += f" {option}"

    return curl_command


def main_menu():
    """Main menu to navigate and manage options."""
    while True:
        print_colored("\n--- Main Menu ---", SKY_BLUE)
        print_colored("1. Build and Execute cURL Command.", YELLOW)
        print_colored("2. Tutorial.", YELLOW)
        print_colored("0. Exit.", YELLOW)
        choice = input_colored("Enter your choice: ", YELLOW)

        if choice == "1":
            command = assemble_curl_command()
            print_colored(f"\nGenerated cURL Command:\n{command}", SKY_BLUE)
            execute = input_colored("Execute this command? (y/n): ", YELLOW).lower()
            if execute == "y":
                subprocess.run(command, shell=True)
        elif choice == "2":
            show_tutorial()
        elif choice == "0":
            print_colored("Exiting. Goodbye!", GREENISH)
            log_activity("Script exited.")
            break
        else:
            print_colored("Invalid choice. Please enter 0, 1, or 2.", YELLOW)

if __name__ == "__main__":
    print_colored("Welcome to the Ultimate cURL Command Builder!", GREENISH + BOLD)
    log_activity("Script started.")
    main_menu()
