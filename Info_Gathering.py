import subprocess
import sys
import threading

# Define color codes for terminal output
RESET = "\033[0m"
SKY_BLUE = "\033[94m"
GREENISH = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

def run_command(command, timeout=45):
    """
    Executes a shell command with a timeout.
    Returns command output or error message.
    """
    result = None

    def target():
        nonlocal result
        try:
            result = subprocess.run(
                command, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        except subprocess.CalledProcessError as e:
            result = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return f"Timeout after {timeout} seconds."

    if isinstance(result, subprocess.CalledProcessError):
        return f"Error executing command: {result.stderr.strip()}"

    return result.stdout.strip()

def dns_tools_submenu(domain_or_ip):
    """
    Submenu for DNS tools.
    """
    tools = [
        "dig", "nslookup", "host", "dnsenum", "fierce", "dnsrecon", 
        "theHarvester", "amass", "assetfinder", "puredns"
    ]

    while True:
        print(f"{BOLD}{YELLOW}DNS Tools:{RESET}")
        for idx, tool in enumerate(tools, 1):
            print(f"{idx}. {tool}")
        print(f"0. Exit")

        choice = input(f"{BOLD}{YELLOW}Enter your choice: {RESET}").strip()

        if not choice.isdigit() or not (0 <= int(choice) <= len(tools)):
            print(f"{YELLOW}Invalid choice. Please try again.{RESET}")
            continue

        if int(choice) == 0:
            print(f"{BOLD}{YELLOW}Returning to main menu.{RESET}")
            break

        tool = tools[int(choice) - 1]

        # Special handling for tools requiring additional arguments
        if tool == "theHarvester":
            domain = input(f"{BOLD}{YELLOW}Enter the domain to scan: {RESET}").strip()
            if not domain:
                print(f"{YELLOW}Domain is required for theHarvester.{RESET}")
                continue
            command = f"theHarvester -d {domain} -l 100 -b all"

        elif tool == "dnsenum":
            command = f"dnsenum {domain_or_ip}"

        elif tool == "fierce":
            command = f"fierce -dns {domain_or_ip}"

        elif tool == "dnsrecon":
            command = f"dnsrecon -d {domain_or_ip}"

        else:
            command = f"{tool} {domain_or_ip}"

        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of {tool}:{RESET}\n{output}\n{'='*40}\n")

def directory_brute_force_submenu(domain_or_ip):
    """
    Submenu for Directory Brute Force tools.
    """
    tools = ["gobuster", "feroxbuster"]

    while True:
        print(f"{BOLD}{YELLOW}Directory Brute Force Tools:{RESET}")
        for idx, tool in enumerate(tools, 1):
            print(f"{idx}. {tool}")
        print(f"0. Exit")

        choice = input(f"{BOLD}{YELLOW}Enter your choice: {RESET}").strip()

        if not choice.isdigit() or not (0 <= int(choice) <= len(tools)):
            print(f"{YELLOW}Invalid choice. Please try again.{RESET}")
            continue

        if int(choice) == 0:
            print(f"{BOLD}{YELLOW}Returning to main menu.{RESET}")
            break

        tool = tools[int(choice) - 1]

        if tool == "gobuster":
            gobuster_submenu(domain_or_ip)
        elif tool == "feroxbuster":
            feroxbuster_submenu(domain_or_ip)

def gobuster_submenu(domain_or_ip):
    """
    Submenu for Gobuster options.
    """
    wordlist = select_wordlist()
    gobuster_modes = ["dir", "dns", "fuzz", "vhost"]

    while True:
        print(f"{BOLD}{YELLOW}Select a Gobuster mode:{RESET}")
        for idx, mode in enumerate(gobuster_modes, 1):
            print(f"{idx}. {mode}")
        print(f"0. Exit")

        choice = input(f"{BOLD}{YELLOW}Enter the number of your choice: {RESET}").strip()

        if not choice.isdigit() or not (0 <= int(choice) <= len(gobuster_modes)):
            print(f"{YELLOW}Invalid choice. Please try again.{RESET}")
            continue

        if int(choice) == 0:
            print(f"{BOLD}{YELLOW}Returning to Directory Brute Force menu.{RESET}")
            break

        mode = gobuster_modes[int(choice) - 1]
        command = f"gobuster {mode} -u http://{domain_or_ip} -w {wordlist}"

        if mode == "vhost":
            command += " --append-domain"

        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of Gobuster {mode}:{RESET}\n{output}\n{'='*40}\n")

def feroxbuster_submenu(domain_or_ip):
    """
    Submenu for Feroxbuster options.
    """
    wordlist = select_wordlist()
    feroxbuster_options = [
        "basic scan", "set custom user-agent", "add query parameters",
        "filter responses by status codes", "increase verbosity",
        "custom recursion depth"
    ]

    while True:
        print(f"{BOLD}{YELLOW}Select a Feroxbuster option:{RESET}")
        for idx, option in enumerate(feroxbuster_options, 1):
            print(f"{idx}. {option}")
        print(f"0. Exit")

        choice = input(f"{BOLD}{YELLOW}Enter the number of your choice: {RESET}").strip()

        if not choice.isdigit() or not (0 <= int(choice) <= len(feroxbuster_options)):
            print(f"{YELLOW}Invalid choice. Please try again.{RESET}")
            continue

        if int(choice) == 0:
            print(f"{BOLD}{YELLOW}Returning to Directory Brute Force menu.{RESET}")
            break

        option = feroxbuster_options[int(choice) - 1]
        command = f"feroxbuster -u http://{domain_or_ip} -w {wordlist}"

        if option == "set custom user-agent":
            user_agent = input(f"{BOLD}{YELLOW}Enter custom User-Agent: {RESET}").strip()
            command += f" -a \"{user_agent}\""
        elif option == "add query parameters":
            query = input(f"{BOLD}{YELLOW}Enter query parameters (key=value): {RESET}").strip()
            command += f" -Q \"{query}\""
        elif option == "filter responses by status codes":
            status_codes = input(f"{BOLD}{YELLOW}Enter status codes to filter (comma-separated): {RESET}").strip()
            command += f" -C {status_codes}"
        elif option == "increase verbosity":
            command += " -v"
        elif option == "custom recursion depth":
            depth = input(f"{BOLD}{YELLOW}Enter recursion depth: {RESET}").strip()
            command += f" -d {depth}"

        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of Feroxbuster {option}:{RESET}\n{output}\n{'='*40}\n")

def select_wordlist():
    """
    Prompts the user to enter a path to a wordlist and validates it.
    """
    print(f"{BOLD}{YELLOW}Enter the path to your wordlist: {RESET}")
    wordlist = input().strip()
    if not wordlist:
        print(f"{YELLOW}No wordlist provided. Exiting.{RESET}")
        sys.exit(0)  # Exit with status 0 (success)
    return wordlist

def main():
    """
    Main function to start the script.
    """
    print(f"{BOLD}{YELLOW}Enter the domain or IP to scan: {RESET}")
    domain_or_ip = input().strip()

    if not domain_or_ip:
        print(f"{YELLOW}No domain or IP provided. Exiting.{RESET}")
        sys.exit(0)  # Exit with status 0 (success)

    while True:
        print(f"{BOLD}{YELLOW}Main Menu:{RESET}")
        print("1. DNS Tools")
        print("2. Directory Brute Force Tools")
        print("0. Exit")

        choice = input(f"{BOLD}{YELLOW}Enter your choice: {RESET}").strip()

        if choice == "0":
            print(f"{BOLD}{YELLOW}Exiting. Goodbye!{RESET}")
            sys.exit(0)

        if choice == "1":
            dns_tools_submenu(domain_or_ip)
        elif choice == "2":
            directory_brute_force_submenu(domain_or_ip)
        else:
            print(f"{YELLOW}Invalid choice. Please try again.{RESET}")

if __name__ == "__main__":
    main()
