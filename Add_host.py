import os
import subprocess
import readline  # Enhances user input
import requests  # Optional for validation

# Define color codes for terminal output
RESET = "\033[0m"
SKY_BLUE = "\033[94m"
GREENISH = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

def display_menu():
    print(f"{SKY_BLUE}{BOLD}Manage /etc/hosts File{RESET}")
    print(f"{GREENISH}1. Add an IP and domain")
    print(f"2. Delete an IP and domain")
    print(f"3. Exit{RESET}")
    choice = input(f"{YELLOW}Enter your choice: {RESET}")
    return choice

def display_hosts_entries():
    with open("/etc/hosts", "r") as hosts_file:
        lines = hosts_file.readlines()
        entries = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return entries

def add_entry():
    ip_address = input(f"{YELLOW}Enter the IP address: {RESET}")
    domain_name = input(f"{YELLOW}Enter the domain name: {RESET}")
    entry = f"{ip_address} {domain_name}"
    try:
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(f"\n{entry}\n")
        print(f"{GREENISH}Successfully added the entry: {BOLD}{entry}{RESET}")
    except PermissionError:
        print(f"{YELLOW}Permission denied. Please run the script with root privileges.{RESET}")
    except Exception as e:
        print(f"{YELLOW}An error occurred: {e}{RESET}")

def delete_entry():
    try:
        # Display current entries
        entries = display_hosts_entries()
        if not entries:
            print(f"{YELLOW}No entries found in /etc/hosts to delete.{RESET}")
            return
        
        print(f"{SKY_BLUE}\nCurrent /etc/hosts entries:{RESET}")
        for idx, entry in enumerate(entries, 1):
            print(f"{idx}. {entry}")

        # Ask the user to select an entry to delete
        choice = int(input(f"\n{YELLOW}Select the entry number to delete: {RESET}"))
        if 1 <= choice <= len(entries):
            entry_to_delete = entries[choice - 1]
            print(f"{GREENISH}Deleting entry: {BOLD}{entry_to_delete}{RESET}")
            
            # Update the hosts file
            with open("/etc/hosts", "r") as hosts_file:
                lines = hosts_file.readlines()
            with open("/etc/hosts", "w") as hosts_file:
                for line in lines:
                    if line.strip() != entry_to_delete:
                        hosts_file.write(line)
            print(f"{GREENISH}Successfully deleted the entry.{RESET}")
        else:
            print(f"{YELLOW}Invalid choice. No changes made.{RESET}")
    except ValueError:
        print(f"{YELLOW}Invalid input. Please enter a number.{RESET}")
    except PermissionError:
        print(f"{YELLOW}Permission denied. Please run the script with root privileges.{RESET}")
    except Exception as e:
        print(f"{YELLOW}An error occurred: {e}{RESET}")

def main():
    while True:
        choice = display_menu()
        if choice == "1":
            add_entry()
        elif choice == "2":
            delete_entry()
        elif choice == "3":
            print(f"{SKY_BLUE}Exiting...{RESET}")
            break
        else:
            print(f"{YELLOW}Invalid choice. Please try again.{RESET}")

if __name__ == "__main__":
    main()
