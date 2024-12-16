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
    Submenu for DNS tools with expanded options, detailed explanations, and examples for each tool.
    Users can select a tool, input required parameters, and execute commands.
    """
    tools = ["dig", "nslookup", "host", "dnsenum", "fierce"]

    while True:
        print(f"{BOLD}{YELLOW}DNS Tools - Enhanced Options:{RESET}")
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

        # Handle specific tool requirements
        if tool == "dig":
            print(f"{BOLD}{YELLOW}Using 'dig' for DNS queries:{RESET}")
            print(f"{GREENISH}Examples of 'dig' commands:{RESET}")
            print(f"- Basic usage: dig <domain>\n"
                  f"- Query specific record types: dig <domain> A/MX/CNAME/NS\n"
                  f"- Use a custom DNS server: dig @8.8.8.8 <domain>\n"
                  f"- Perform reverse lookup: dig -x <IP address>\n"
                  f"- Query all record types: dig <domain> ANY")
            record_type = input(
                f"{BOLD}{YELLOW}Enter record type (A, MX, NS, etc.) [default: A]: {RESET}"
            ).strip() or "A"
            dns_server = input(
                f"{BOLD}{YELLOW}Enter DNS server [default: system default]: {RESET}"
            ).strip()
            command = f"dig {domain_or_ip} {record_type}" if not dns_server else f"dig @{dns_server} {domain_or_ip} {record_type}"

        elif tool == "nslookup":
            print(f"{BOLD}{YELLOW}Using 'nslookup' for DNS queries:{RESET}")
            print(f"{GREENISH}Examples of 'nslookup' commands:{RESET}")
            print(f"- Basic usage: nslookup <domain>\n"
                  f"- Specify a DNS server: nslookup <domain> <server>\n"
                  f"- Reverse lookup: nslookup <IP address>\n")
            dns_server = input(
                f"{BOLD}{YELLOW}Enter DNS server [default: system default]: {RESET}"
            ).strip()
            command = f"nslookup {domain_or_ip} {dns_server}" if dns_server else f"nslookup {domain_or_ip}"

        elif tool == "host":
            print(f"{BOLD}{YELLOW}Using 'host' for DNS lookups:{RESET}")
            print(f"{GREENISH}Examples of 'host' commands:{RESET}")
            print(f"- Basic usage: host <domain>\n"
                  f"- Reverse lookup: host <IP address>\n"
                  f"- Specify DNS server: host <domain> <server>")
            command = f"host {domain_or_ip}"

        elif tool == "dnsenum":
            print(f"{BOLD}{YELLOW}Using 'dnsenum' for DNS enumeration:{RESET}")
            print(f"{GREENISH}Examples of 'dnsenum' commands:{RESET}")
            print(f"- Basic usage: dnsenum <domain>\n"
                  f"- Use specific DNS server: dnsenum --dnsserver <server> <domain>\n"
                  f"- Perform zone transfer check: dnsenum --zonetransfer <domain>")
            additional_options = input(
                f"{BOLD}{YELLOW}Enter additional options (e.g., --dnsserver 8.8.8.8): {RESET}"
            ).strip()
            command = f"dnsenum {additional_options} {domain_or_ip}" if additional_options else f"dnsenum {domain_or_ip}"

        elif tool == "fierce":
            print(f"{BOLD}{YELLOW}Using 'fierce' for DNS enumeration:{RESET}")
            print(f"{GREENISH}Examples of 'fierce' commands:{RESET}")
            print(f"- Basic usage: fierce -dns <domain>\n"
                  f"- Specify DNS server: fierce -dns <domain> --dnsserver <server>\n")
            dns_server = input(
                f"{BOLD}{YELLOW}Enter DNS server [default: system default]: {RESET}"
            ).strip()
            command = f"fierce -dns {domain_or_ip} --dnsserver {dns_server}" if dns_server else f"fierce -dns {domain_or_ip}"

        else:
            print(f"{YELLOW}Tool not recognized. Skipping.{RESET}")
            continue

        # Execute and display the output
        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of {tool}:{RESET}\n{output}\n{'='*40}\n")

def run_all_dns_tools(domain_or_ip):
    """
    Runs all DNS tools sequentially for the given domain or IP.
    Consolidates the output from each tool and presents it in a single post.
    """
    print(f"{BOLD}{YELLOW}Running all DNS tools for: {domain_or_ip}{RESET}")
    
    results = []

    # 1. Run `dig`
    print(f"{BOLD}{YELLOW}Running 'dig'...{RESET}")
    dig_command = f"dig {domain_or_ip} ANY"
    dig_output = run_command(dig_command)
    results.append(f"{BOLD}{GREENISH}Output of 'dig':{RESET}\n{dig_output}\n{'='*40}\n")

    # 2. Run `nslookup`
    print(f"{BOLD}{YELLOW}Running 'nslookup'...{RESET}")
    nslookup_command = f"nslookup {domain_or_ip}"
    nslookup_output = run_command(nslookup_command)
    results.append(f"{BOLD}{GREENISH}Output of 'nslookup':{RESET}\n{nslookup_output}\n{'='*40}\n")

    # 3. Run `host`
    print(f"{BOLD}{YELLOW}Running 'host'...{RESET}")
    host_command = f"host {domain_or_ip}"
    host_output = run_command(host_command)
    results.append(f"{BOLD}{GREENISH}Output of 'host':{RESET}\n{host_output}\n{'='*40}\n")

    # 4. Run `dnsenum`
    print(f"{BOLD}{YELLOW}Running 'dnsenum'...{RESET}")
    dnsenum_command = f"dnsenum {domain_or_ip}"
    dnsenum_output = run_command(dnsenum_command)
    results.append(f"{BOLD}{GREENISH}Output of 'dnsenum':{RESET}\n{dnsenum_output}\n{'='*40}\n")

    # 5. Run `fierce`
    print(f"{BOLD}{YELLOW}Running 'fierce'...{RESET}")
    fierce_command = f"fierce -dns {domain_or_ip}"
    fierce_output = run_command(fierce_command)
    results.append(f"{BOLD}{GREENISH}Output of 'fierce':{RESET}\n{fierce_output}\n{'='*40}\n")

    # Consolidate results
    print(f"{BOLD}{SKY_BLUE}All DNS tool outputs consolidated:{RESET}")
    consolidated_output = "\n".join(results)
    print(consolidated_output)
    return consolidated_output


def recon_tools_submenu(domain_or_ip):
    """
    Submenu for Reconnaissance tools with expanded options, detailed explanations, and examples.
    Allows users to gather intelligence on a given domain or IP.
    """
    tools = ["dnsrecon", "theHarvester", "amass", "assetfinder"]

    while True:
        print(f"{BOLD}{YELLOW}Reconnaissance Tools - Enhanced Options:{RESET}")
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

        # Handle specific tool requirements
        if tool == "dnsrecon":
            print(f"{BOLD}{YELLOW}Using 'dnsrecon' for DNS reconnaissance:{RESET}")
            print(f"{GREENISH}Examples of 'dnsrecon' commands:{RESET}")
            print(f"- Basic usage: dnsrecon -d <domain>\n"
                  f"- Perform zone transfer: dnsrecon -d <domain> -t axfr\n"
                  f"- Brute-force subdomains: dnsrecon -d <domain> -D <wordlist> -t brt\n"
                  f"- Specify a nameserver: dnsrecon -d <domain> -n <nameserver>")
            additional_options = input(
                f"{BOLD}{YELLOW}Enter additional options (e.g., -t axfr, -D wordlist.txt): {RESET}"
            ).strip()
            command = f"dnsrecon -d {domain_or_ip} {additional_options}"

        elif tool == "theHarvester":
            print(f"{BOLD}{YELLOW}Using 'theHarvester' for gathering open-source intelligence (OSINT):{RESET}")
            print(f"{GREENISH}Examples of 'theHarvester' commands:{RESET}")
            print(f"- Basic usage: theHarvester -d <domain> -b all\n"
                  f"- Limit number of results: theHarvester -d <domain> -l 100 -b google\n"
                  f"- Use specific search engine: theHarvester -d <domain> -b google/bing/shodan/etc.")
            domain = input(f"{BOLD}{YELLOW}Enter the domain to scan [default: {domain_or_ip}]: {RESET}").strip() or domain_or_ip
            source = input(
                f"{BOLD}{YELLOW}Enter source (e.g., all, google, shodan) [default: all]: {RESET}"
            ).strip() or "all"
            limit = input(
                f"{BOLD}{YELLOW}Enter the result limit [default: 100]: {RESET}"
            ).strip() or "100"
            command = f"theHarvester -d {domain} -l {limit} -b {source}"

        elif tool == "amass":
            print(f"{BOLD}{YELLOW}Using 'amass' for in-depth subdomain enumeration:{RESET}")
            print(f"{GREENISH}Examples of 'amass' commands:{RESET}")
            print(f"- Basic enumeration: amass enum -d <domain>\n"
                  f"- Passive enumeration only: amass enum -d <domain> -passive\n"
                  f"- Active enumeration: amass enum -d <domain> -active\n"
                  f"- Save results to a file: amass enum -d <domain> -o output.txt")
            mode = input(
                f"{BOLD}{YELLOW}Enter mode (e.g., passive, active) [default: passive]: {RESET}"
            ).strip() or "passive"
            output_file = input(
                f"{BOLD}{YELLOW}Enter output file name [default: none]: {RESET}"
            ).strip()
            command = f"amass enum -d {domain_or_ip} -{mode}"
            if output_file:
                command += f" -o {output_file}"

        elif tool == "assetfinder":
            print(f"{BOLD}{YELLOW}Using 'assetfinder' for discovering subdomains:{RESET}")
            print(f"{GREENISH}Examples of 'assetfinder' commands:{RESET}")
            print(f"- Basic usage: assetfinder <domain>\n"
                  f"- Discover subdomains only: assetfinder --subs-only <domain>")
            subdomains_only = input(
                f"{BOLD}{YELLOW}Search for subdomains only? (y/n) [default: y]: {RESET}"
            ).strip().lower() or "y"
            if subdomains_only == "y":
                command = f"assetfinder --subs-only {domain_or_ip}"
            else:
                command = f"assetfinder {domain_or_ip}"

        else:
            print(f"{YELLOW}Tool not recognized. Skipping.{RESET}")
            continue

        # Execute and display the output
        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of {tool}:{RESET}\n{output}\n{'='*40}\n")
        
def puredns_tool(domain_or_ip):
    """
    Executes Puredns with expanded options, explanations, and examples.
    Allows users to perform DNS resolution with customized flags.
    """
    print(f"{BOLD}{YELLOW}Puredns - Enhanced Options:{RESET}")
    print(f"{GREENISH}Examples of 'puredns' commands:{RESET}")
    print(f"- Basic usage: puredns resolve <domain> -w <wordlist>\n"
          f"- Use specific resolvers: puredns resolve <domain> -w <wordlist> -r <resolvers.txt>\n"
          f"- Save results to file: puredns resolve <domain> -w <wordlist> -o <output.txt>\n"
          f"- Use brute force mode: puredns bruteforce <subdomains.txt> <domain>\n")
    
    # Select Wordlist
    wordlist = select_wordlist()
    if not wordlist:
        print(f"{YELLOW}Wordlist is required for Puredns. Exiting this option.{RESET}")
        return

    # Resolver File
    resolve_file = input(f"{BOLD}{YELLOW}Enter resolver file path (optional) [default: none]: {RESET}").strip()

    # Output File
    output_file = input(f"{BOLD}{YELLOW}Enter output file path (optional) [default: none]: {RESET}").strip()

    # Brute Force Option
    use_bruteforce = input(f"{BOLD}{YELLOW}Use brute force mode? (y/n) [default: n]: {RESET}").strip().lower() or "n"

    if use_bruteforce == "y":
        subdomains_file = input(
            f"{BOLD}{YELLOW}Enter path to subdomains file for brute force (required): {RESET}"
        ).strip()
        if not subdomains_file:
            print(f"{YELLOW}Subdomains file is required for brute force mode. Exiting.{RESET}")
            return
        command = f"puredns bruteforce {subdomains_file} {domain_or_ip}"
    else:
        command = f"puredns resolve {domain_or_ip} -w {wordlist}"

    # Append resolver file if specified
    if resolve_file:
        command += f" -r {resolve_file}"

    # Append output file if specified
    if output_file:
        command += f" -o {output_file}"

    print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
    output = run_command(command)
    print(f"{GREENISH}Output of Puredns:{RESET}\n{output}\n{'='*40}\n")


def directory_brute_force_submenu(domain_or_ip):
    """
    Submenu for Directory Brute Force tools with expanded options and detailed examples.
    Allows users to discover directories and files on web servers.
    """
    tools = ["gobuster", "feroxbuster"]

    while True:
        print(f"{BOLD}{YELLOW}Directory Brute Force Tools - Enhanced Options:{RESET}")
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
    Submenu for Gobuster options with detailed explanations and examples.
    """
    wordlist = select_wordlist()
    gobuster_modes = ["dir (Directory Brute Force)", "dns (DNS Enumeration)", "fuzz (Fuzz Testing)", "vhost (Virtual Hosts)"]

    while True:
        print(f"{BOLD}{YELLOW}Gobuster - Select a Mode:{RESET}")
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

        mode = gobuster_modes[int(choice) - 1].split(" ")[0]  # Extract the mode (e.g., "dir")

        print(f"{BOLD}{YELLOW}Using Gobuster in {mode} mode:{RESET}")
        if mode == "dir":
            print(f"{GREENISH}Examples for 'dir' mode:{RESET}")
            print(f"- Basic usage: gobuster dir -u <URL> -w <wordlist>\n"
                  f"- Filter by status codes: gobuster dir -u <URL> -w <wordlist> -s 200,301\n"
                  f"- Specify extensions: gobuster dir -u <URL> -w <wordlist> -x php,html\n")
            extensions = input(f"{BOLD}{YELLOW}Enter file extensions (e.g., php,html) [default: none]: {RESET}").strip()
            status_codes = input(f"{BOLD}{YELLOW}Enter status codes to filter (e.g., 200,301) [default: none]: {RESET}").strip()
            command = f"gobuster dir -u http://{domain_or_ip} -w {wordlist}"
            if extensions:
                command += f" -x {extensions}"
            if status_codes:
                command += f" -s {status_codes}"

        elif mode == "dns":
            print(f"{GREENISH}Examples for 'dns' mode:{RESET}")
            print(f"- Basic usage: gobuster dns -d <domain> -w <wordlist>\n"
                  f"- Use a specific DNS server: gobuster dns -d <domain> -w <wordlist> -r <DNS server>\n")
            dns_server = input(f"{BOLD}{YELLOW}Enter DNS server [default: system default]: {RESET}").strip()
            command = f"gobuster dns -d {domain_or_ip} -w {wordlist}"
            if dns_server:
                command += f" -r {dns_server}"

        elif mode == "fuzz":
            print(f"{GREENISH}Examples for 'fuzz' mode:{RESET}")
            print(f"- Basic usage: gobuster fuzz -u <URL> -w <wordlist> -z\n"
                  f"- Filter by status codes: gobuster fuzz -u <URL> -w <wordlist> -s 200,404\n")
            status_codes = input(f"{BOLD}{YELLOW}Enter status codes to filter (e.g., 200,404) [default: none]: {RESET}").strip()
            command = f"gobuster fuzz -u http://{domain_or_ip} -w {wordlist} -z"
            if status_codes:
                command += f" -s {status_codes}"

        elif mode == "vhost":
            print(f"{GREENISH}Examples for 'vhost' mode:{RESET}")
            print(f"- Basic usage: gobuster vhost -u <URL> -w <wordlist>\n"
                  f"- Append domain: gobuster vhost -u <URL> -w <wordlist> --append-domain\n")
            append_domain = input(f"{BOLD}{YELLOW}Append domain to results? (y/n) [default: y]: {RESET}").strip().lower() or "y"
            command = f"gobuster vhost -u http://{domain_or_ip} -w {wordlist}"
            if append_domain == "y":
                command += " --append-domain"

        print(f"{BOLD}{SKY_BLUE}Executing: {command}{RESET}")
        output = run_command(command)
        print(f"{GREENISH}Output of Gobuster {mode} mode:{RESET}\n{output}\n{'='*40}\n")

def feroxbuster_submenu(domain_or_ip):
    """
    Submenu for Feroxbuster options with detailed explanations and examples.
    """
    wordlist = select_wordlist()
    feroxbuster_options = [
        "basic scan",
        "set custom user-agent",
        "add query parameters",
        "filter responses by status codes",
        "increase verbosity",
        "custom recursion depth"
    ]

    while True:
        print(f"{BOLD}{YELLOW}Feroxbuster - Select an Option:{RESET}")
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

        print(f"{BOLD}{YELLOW}Using Feroxbuster with option: {option}{RESET}")
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
        print(f"{GREENISH}Output of Feroxbuster ({option}):{RESET}\n{output}\n{'='*40}\n")


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

def edit_domain_or_ip(current_domain_or_ip):
    """
    Allows the user to edit or re-enter a domain or IP.
    If the user presses Enter, the current domain/IP remains unchanged.
    """
    print(f"{BOLD}{YELLOW}Current Domain/IP: {SKY_BLUE}{current_domain_or_ip}{RESET}")
    new_domain_or_ip = input(f"{BOLD}{YELLOW}Enter a new domain/IP or press Enter to keep the current one: {RESET}").strip()

    if new_domain_or_ip:
        print(f"{BOLD}{GREENISH}Domain/IP updated to: {new_domain_or_ip}{RESET}")
        return new_domain_or_ip
    else:
        print(f"{BOLD}{GREENISH}Domain/IP remains unchanged: {current_domain_or_ip}{RESET}")
        return current_domain_or_ip

def main():
    """
    Main function to start the script.
    Displays the main menu and integrates all tool submenus, including an automated DNS tools option.
    """
    print(f"{BOLD}{YELLOW}Welcome to the Enhanced Reconnaissance Toolkit!{RESET}")
    print(f"{GREENISH}This toolkit allows you to use DNS tools, reconnaissance tools, "
          f"directory brute force tools, and more in a flexible and interactive way.{RESET}")

    domain_or_ip = None

    while True:
        if not domain_or_ip:
            print(f"{BOLD}{YELLOW}Enter the domain or IP to scan: {RESET}")
            domain_or_ip = input().strip()
            if not domain_or_ip:
                print(f"{YELLOW}No domain or IP provided. Please enter a valid input.{RESET}")
                continue

        print(f"\n{BOLD}{YELLOW}Main Menu:{RESET}")
        print("1. DNS Tools")
        print("2. Reconnaissance Tools")
        print("3. Directory Brute Force Tools")
        print("4. Puredns")
        print("5. Edit Domain or IP")
        print("6. Run All DNS Tools Automatically")
        print("0. Exit")

        choice = input(f"{BOLD}{YELLOW}Enter your choice: {RESET}").strip()

        if not choice.isdigit():
            print(f"{YELLOW}Invalid input. Please enter a number.{RESET}")
            continue

        choice = int(choice)

        if choice == 0:
            print(f"{BOLD}{YELLOW}Exiting. Goodbye!{RESET}")
            sys.exit(0)  # Exit with success status

        if choice == 5:
            domain_or_ip = edit_domain_or_ip(domain_or_ip)
            continue

        if choice == 6:
            run_all_dns_tools(domain_or_ip)
            continue

        # Route the user to the appropriate submenu
        if choice == 1:
            dns_tools_submenu(domain_or_ip)
        elif choice == 2:
            recon_tools_submenu(domain_or_ip)
        elif choice == 3:
            directory_brute_force_submenu(domain_or_ip)
        elif choice == 4:
            puredns_tool(domain_or_ip)
        else:
            print(f"{YELLOW}Invalid choice. Please select a valid option.{RESET}")


if __name__ == "__main__":
    main()
