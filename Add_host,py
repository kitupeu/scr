import os
import subprocess
import readline  # Enables better input functionality
import requests  # Can be used if you need to validate the IP/domain externally

# Define color codes for terminal output
RESET = "\033[0m"
SKY_BLUE = "\033[94m"
GREENISH = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

def update_hosts():
    # Prompt for user input with colorized text
    print(f"{SKY_BLUE}{BOLD}Update /etc/hosts File{RESET}")
    ip_address = input(f"{YELLOW}Enter the IP address: {RESET}")
    domain_name = input(f"{YELLOW}Enter the domain name: {RESET}")

    # Create the entry
    entry = f"{ip_address} {domain_name}"

    try:
        # Append the entry to /etc/hosts
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(f"\n{entry}\n")
        
        print(f"{GREENISH}Successfully added the entry: {BOLD}{entry}{RESET}")
    
        # Display the contents of /etc/hosts
        print(f"\n{SKY_BLUE}Current /etc/hosts content:{RESET}")
        subprocess.run(["cat", "/etc/hosts"])
    
    except PermissionError:
        print(f"{YELLOW}Permission denied. Please run the script with root privileges (e.g., using sudo).{RESET}")
    except Exception as e:
        print(f"{YELLOW}An error occurred: {e}{RESET}")

if __name__ == "__main__":
    update_hosts()
