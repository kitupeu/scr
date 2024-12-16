import subprocess
import sys
import requests
import threading

# Define color codes for terminal output
RESET = "\033[0m"
SKY_BLUE = "\033[94m"
GREENISH = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

def run_command(command, timeout=45):
    result = None

    def target():
        nonlocal result
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            result = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print(f"{YELLOW}Command timed out after {timeout} seconds. Skipping.{RESET}")
        return f"Timeout after {timeout} seconds."

    if isinstance(result, subprocess.CalledProcessError):
        return f"Error executing command: {result.stderr}"

    return result.stdout

def select_wordlist():
    print(f"{BOLD}{YELLOW}Enter the path to the wordlist for brute force: {RESET}", end="")
    wordlist = input().strip()
    if not wordlist:
        print(f"{YELLOW}No wordlist provided. Please enter a valid path.{RESET}")
        sys.exit(1)
    return wordlist

def execute_dns_query_option(domain_or_ip):
    options = [
        "dig",
        "nslookup",
        "host",
        "dnsenum",
        "fierce",
        "dnsrecon",
        "theHarvester",
        "amass",
        "assetfinder",
        "puredns",
        "gobuster",
        "feroxbuster",
        "ffuf",
        "Exit"
    ]

    while True:
        print(f"{BOLD}{YELLOW}Select a tool to execute:{RESET}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        print(f"{BOLD}{YELLOW}Enter the number of your choice: {RESET}", end="")
        choice = input().strip()

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print(f"{YELLOW}Invalid choice. Please select a valid option.{RESET}")
            continue

        tool = options[int(choice) - 1]

        if tool == "Exit":
            print(f"{BOLD}{YELLOW}Exiting the session. Goodbye!{RESET}")
            break

        if tool in ["dnsenum", "puredns", "gobuster", "feroxbuster", "ffuf"]:
            wordlist = select_wordlist()

        command = ""
        if tool == "dig":
            command = f"dig {domain_or_ip}"
        elif tool == "nslookup":
            command = f"nslookup {domain_or_ip}"
        elif tool == "host":
            command = f"host {domain_or_ip}"
        elif tool == "dnsenum":
            command = f"dnsenum --enum {domain_or_ip} -f {wordlist} -r"
        elif tool == "fierce":
            command = f"fierce --domain {domain_or_ip}"
        elif tool == "dnsrecon":
            command = f"dnsrecon -d {domain_or_ip}"
        elif tool == "theHarvester":
            command = f"theHarvester -d {domain_or_ip} -b google"
        elif tool == "amass":
            command = f"amass enum -d {domain_or_ip}"
        elif tool == "assetfinder":
            command = f"assetfinder --subs-only {domain_or_ip}"
        elif tool == "puredns":
            command = f"puredns bruteforce {wordlist} {domain_or_ip}"
        elif tool == "gobuster":
            command = f"gobuster dns -d {domain_or_ip} -w {wordlist}"
        elif tool == "feroxbuster":
            command = f"feroxbuster -u http://{domain_or_ip} -w {wordlist}"
        elif tool == "ffuf":
            command = f"ffuf -u http://{domain_or_ip} -w {wordlist} -H \"Host: FUZZ.{domain_or_ip}\""

        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of {tool}:{RESET}\n{output}\n{'='*40}\n")

def main():
    print(f"{BOLD}{YELLOW}Enter the IP or domain to scan: {RESET}", end="")
    domain_or_ip = input().strip()

    if not domain_or_ip:
        print(f"{BOLD}{YELLOW}Invalid input. Please enter a valid domain or IP.{RESET}")
        sys.exit(1)

    execute_dns_query_option(domain_or_ip)

if __name__ == "__main__":
    main()
