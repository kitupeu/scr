import os
import readline
import requests

# Define color codes for terminal output
RESET = "\033[0m"
SKY_BLUE = "\033[94m"
GREENISH = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

def print_colored(text, color):
    """Print text in the specified color."""
    print(f"{color}{text}{RESET}")

def input_colored(prompt, color):
    """Input with colored prompt."""
    return input(f"{color}{prompt}{RESET}")

def fetch_and_execute_remote_script():
    """Fetch and execute a remote script without saving it locally."""
    script_url = "https://kitup.eu/scripts/py/Master_cURL.py"

    try:
        # Fetch the script content
        response = requests.get(script_url)

        if response.status_code == 200:
            # Execute the script directly from the fetched content
            script_content = response.text
            print_colored("Fetched script content:", GREENISH)
            print(script_content)  # Display fetched script content for reference

            try:
                exec(script_content)  # Directly execute the script content
            except Exception as e:
                print_colored(f"Error executing the fetched script: {e}", YELLOW)
        else:
            print_colored(f"Failed to fetch the script. HTTP Status: {response.status_code}", YELLOW)

    except requests.RequestException as e:
        print_colored(f"Error fetching the script: {e}", YELLOW)

def interactive_request_builder():
    """Step-by-step interactive cURL command builder."""
    print_colored("\nInteractive cURL Command Builder", GREENISH + BOLD)

    curl_command = ["curl"]

    # Step 1: Add HTTP method or flags
    method_or_flags = select_http_method_or_flags()
    if method_or_flags:
        curl_command.append(method_or_flags)

    # Step 2: Add user credentials (optional)
    credentials = add_credentials()

    # Step 3: Add the URL
    url = construct_url(credentials)
    curl_command.append(url)

    # Step 4: Add custom headers
    headers = add_headers()
    for header in headers:
        curl_command.append(header)

    # Step 5: Add data payload (JSON or form data)
    data = add_data_payload()
    if data:
        curl_command.append(data)

    # Step 6: Add cookies (optional)
    cookie = add_cookie()
    if cookie:
        curl_command.append(f"-b '{cookie}'")

    # Final cURL command
    final_command = " ".join(curl_command)
    print_colored("\nFinal cURL Command:", SKY_BLUE)
    print_colored(final_command, BOLD + GREENISH)

    # Optionally execute the command
    execute_command(final_command)

def select_http_method_or_flags():
    """Select HTTP method or choose to add custom flags."""
    print_colored("\nStep 1: Choose HTTP Method or Add Flags", SKY_BLUE)
    options = ["GET", "POST", "PUT", "DELETE", "PATCH", "Add Custom Flags", "Fetch and Execute Remote Script"]
    for idx, option in enumerate(options, 1):
        print_colored(f"{idx}. {option}", YELLOW)
    choice = input_colored("Select an option: ", YELLOW)
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        if int(choice) == 6:  # Custom Flags
            return add_custom_flags()
        elif int(choice) == 7:  # Fetch and Execute Remote Script
            fetch_and_execute_remote_script()
            return None
        return f"-X {options[int(choice) - 1]}"
    print_colored("Invalid choice. Please select a valid option.", YELLOW)
    return None

def add_custom_flags():
    """Add custom cURL flags."""
    print_colored("\nAdd Custom Flags", SKY_BLUE)
    flags = []
    while True:
        flag = input_colored("Enter a custom flag (or press Enter to finish): ", YELLOW).strip()
        if not flag:
            break
        flags.append(flag)
    return " ".join(flags)

def add_credentials():
    """Add user credentials."""
    print_colored("\nStep 2: Add User Credentials (optional)", SKY_BLUE)
    choice = input_colored("Do you want to add user credentials? (y/n): ", YELLOW).lower()
    if choice == "y":
        username = input_colored("Enter username: ", YELLOW)
        password = input_colored("Enter password: ", YELLOW)
        return f"{username}:{password}@"
    return ""

def construct_url(credentials=""):
    """Construct URL, appending credentials if provided."""
    print_colored("\nStep 3: Construct the URL", SKY_BLUE)
    protocol = input_colored("Enter protocol (http/https): ", YELLOW).lower()
    ip_address = input_colored("Enter server IP or domain: ", YELLOW)
    port = input_colored("Enter port (or leave blank for default): ", YELLOW)
    endpoint = input_colored("Enter endpoint or path: ", YELLOW)

    # Construct URL with optional credentials
    url = f"{protocol}://{credentials}{ip_address}"
    if port:
        url += f":{port}"
    if endpoint:
        url += f"/{endpoint}"
    return url

def add_headers():
    """Add custom headers interactively."""
    print_colored("\nStep 4: Add Custom Headers", SKY_BLUE)
    headers = []
    common_headers = {
        "1": "Authorization: Bearer {value}",
        "2": "Content-Type: {value}",
        "3": "Accept: {value}",
        "4": "User-Agent: {value}",
        "5": "Cookie: {value}",
        "6": "Custom Header (manually enter full name and value)"
    }

    while True:
        print_colored("\nCommon Header Options:", YELLOW)
        for key, header_template in common_headers.items():
            if "Custom Header" in header_template:
                print_colored(f"{key}. {header_template}", YELLOW)
            else:
                header_name = header_template.split(":")[0]
                print_colored(f"{key}. {header_name}", YELLOW)

        print_colored("0. Done adding headers", YELLOW)

        choice = input_colored("Choose a header to add (enter number): ", YELLOW).strip()

        if choice == "0":
            break
        elif choice in common_headers:
            if choice == "6":  # Custom header
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
    """Add JSON or form data payload."""
    print_colored("\nStep 5: Add Data Payload (optional)", SKY_BLUE)
    data_type = input_colored("Choose data type (1 for JSON, 2 for form data, 3 to skip): ", YELLOW)
    if data_type == "1":
        payload = input_colored("Enter JSON data (e.g., '{\"key\":\"value\"}'): ", YELLOW)
        return f"-d '{payload}'"
    elif data_type == "2":
        payload = input_colored("Enter form data (e.g., 'key=value&key2=value2'): ", YELLOW)
        return f"-d '{payload}'"
    return None

def add_cookie():
    """Add cookies to the request."""
    print_colored("\nStep 6: Add Cookies (optional)", SKY_BLUE)
    cookie = input_colored("Enter cookie (e.g., 'PHPSESSID=12345') or press Enter to skip: ", YELLOW)
    return cookie if cookie else None

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

    while True:
        print_colored("\nMain Menu:", SKY_BLUE)
        print_colored("1. Build a cURL command interactively.", YELLOW)
        print_colored("2. Fetch and Execute Remote Script.", YELLOW)
        print_colored("0. Exit.", YELLOW)
        choice = input_colored("Enter your choice: ", YELLOW)

        if choice == "1":
            interactive_request_builder()
        elif choice == "2":
            fetch_and_execute_remote_script()
        elif choice == "0":
            print_colored("Exiting. Goodbye!", GREENISH)
            break
        else:
            print_colored("Invalid choice. Please select 1, 2, or 0.", YELLOW)
