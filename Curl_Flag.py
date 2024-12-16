import os

# Define cURL flags and descriptions
# Dictionary to store cURL flags and their descriptions, grouped by categories
curl_flags = {
    "Basic Usage": {
        "-#": "Display progress as a simple bar",
        "-d": "Send specified data in a POST request",
        "-F": "Specify multipart form data",
        "-I": "Fetch the headers only",
        "-X": "Specify custom HTTP request method",
        "-G": "Send the data as a GET request",
        "-L": "Follow HTTP redirects",
        "-o": "Write output to file",
        "-O": "Save file using remote name",
        "-s": "Suppress progress meter and error messages (silent mode)",
    },
    "Authentication": {
        "-u": "Set HTTP basic auth credentials",
        "--proxy-user": "Set proxy authentication credentials",
        "--anyauth": "Use any available authentication",
        "--basic": "Use HTTP Basic authentication",
        "--digest": "Use HTTP Digest authentication",
        "--ntlm": "Use NTLM authentication",
        "--negotiate": "Use GSS-Negotiate authentication",
        "--oauth2-bearer": "Use OAuth 2 Bearer token",
    },
    "Headers and Cookies": {
        "-H": "Add custom HTTP headers",
        "-b": "Send cookies from a file or as a string",
        "-c": "Write cookies to a file",
    },
    "Connection": {
        "--connect-timeout": "Maximum time to wait for a connection",
        "--keepalive-time": "Interval for sending keepalive probes",
        "--limit-rate": "Limit data transfer speed",
        "--retry": "Retry on transient errors",
        "--retry-delay": "Delay between retries",
        "--retry-max-time": "Maximum time for retries",
    },
    "SSL/TLS": {
        "-k": "Allow insecure connections",
        "--cacert": "Provide CA certificate file",
        "--cert": "Use client certificate",
        "--key": "Use client private key",
        "--ssl": "Force SSL/TLS usage",
        "--tlsv1.2": "Use specific TLS version",
        "--ciphers": "Specify SSL ciphers to use",
    },
    "Proxy": {
        "-x": "Use a proxy",
        "--proxy-header": "Add custom headers for the proxy",
        "--proxy-digest": "Use Digest authentication with proxy",
        "--proxy-basic": "Use Basic authentication with proxy",
    },
    "Output": {
        "--stderr": "Redirect error messages to a file",
        "--trace": "Write full trace of communication",
        "--trace-ascii": "Trace communication as ASCII",
    },
    "HTTP": {
        "--http1.1": "Use HTTP version 1.1",
        "--http2": "Use HTTP version 2",
        "--http3": "Use HTTP version 3",
    },
    "Data and Upload": {
        "--data-urlencode": "URL encode the POST data",
        "--form-string": "Specify form data without filename",
    },
    "FTP/FTPS": {
        "--ftp-method": "Specify FTP method to use",
        "--ftp-create-dirs": "Create missing directories",
        "--ftp-ssl": "Use SSL/TLS for FTP",
        "--ftp-account": "Specify FTP account data",
    },
    "Debugging": {
        "-v": "Provide verbose output",
        "--trace-time": "Add timestamps to trace/verbose output",
        "--libcurl": "Write equivalent libcurl code to file",
    },
    "File Transfer": {
        "-T": "Upload a file",
        "-z": "Only transfer files modified after time",
        "-C": "Resume file transfer from a specific offset",
    },
    "Miscellaneous": {
        "--compressed": "Request compressed response",
        "-Z": "Perform requests in parallel",
        "--config": "Use configuration file",
        "-": "Read from stdin",
    },
}

# Function to display cURL flags grouped by category with interactive menu options
def display_flags_by_category():
    """Display cURL flags grouped by category with an option to view each category."""
    while True:
        # Display the list of categories to the user
        print("\nAvailable Categories:")
        # Extract the list of categories from the curl_flags dictionary
        categories = list(curl_flags.keys())
        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")
        print(f"{len(categories) + 1}. Exit")

        choice = input("\nChoose a category to view or exit: ").strip()
        # Check if the user selected a valid category number
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            # Get the category selected by the user
            selected_category = categories[int(choice) - 1]
            print(f"\n{selected_category}:")
            print("-" * len(selected_category))
            # Loop through the flags and descriptions of the selected category
            for flag, description in curl_flags[selected_category].items():
                print(f"  {flag}: {description}")
            back = input("\nPress the left arrow key (<-) to return to the main menu: ").strip()
            if back == "<-":
                continue
        elif choice.lower() == "exit" or choice == str(len(categories) + 1):
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Entry point of the program, welcoming the user
    print("Welcome to the cURL Flag Viewer!")
    display_flags_by_category()
