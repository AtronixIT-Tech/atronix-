import os
import logging
import subprocess
from urllib.parse import urlparse
import ipaddress

# Setup Logging
LOG_FILE = "logs/gobuster_errors.log"
OUTPUT_FILE = "outputs/gobuster_results.txt"

def setup_logging():
    """
    Set up logging for the script. Ensure the logs directory is writable.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        if not os.access("logs", os.W_OK):
            raise PermissionError("The 'logs' directory is not writable.")
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    except PermissionError as e:
        print(f"⚠ Logging setup failed: {e}")
        print("⚠ Please ensure the 'logs' directory is writable and try again.")
        exit(1)

def log_error(message):
    """
    Log an error message to the log file and print it to the console.
    """
    logging.error(message)
    print(f"⚠ ERROR: {message}")
    if os.path.exists(LOG_FILE):
        print(f"⚠ The error has been logged in: {LOG_FILE}")

def check_root_privileges():
    """
    Check if the script is run with root privileges.
    """
    if os.geteuid() != 0:
        log_error("Root privileges are required to run this script. Exiting.")
        print("⚠ Root privileges are required to run this script. Please run it using 'sudo'. Exiting.")
        exit(1)

def show_warning():
    """
    Show an ethical use warning and require user agreement.
    """
    print("\n=============== Welcome to the Gobuster Module! ===============")
    print("\n🚀 Welcome to the Gobuster tool! 🚀")
    print("\n⚠ This tool is for ethical hacking and learning purposes only.")
    print("⚠ Do not use it on unauthorized targets.")
    print("\n⚠ WARNING: This tool is for ethical use only.")
    print("By using this tool, you agree to:")
    print("1. Use it only in controlled environments (e.g., CTFs).")
    print("2. Never use it to scan unauthorized targets.")
    print("3. Abide by all applicable laws and policies.")
    agreement = input("\nDo you agree to these terms? [yes/no]: ").strip().lower()
    if agreement == "no":
        log_error("User declined the ethical use agreement.")
        print("⚠ You must agree to the terms to use this tool. Exiting.")
        exit(1)
    elif agreement != "yes":
        log_error(f"Invalid response to ethical agreement: '{agreement}'.")
        print("⚠ Invalid input. Please restart the script and respond with 'yes' or 'no'. Exiting.")
        exit(1)

    print("\n================================================================")
    print("WARNING: This script should only be used in a controlled environment.")
    print("Unauthorized scanning of external or public IPs may violate laws and policies.")
    print("Ensure you have proper permissions before proceeding.")
    print("================================================================\n")

def validate_url_or_ip(target):
    """
    Validate if the given target is a valid URL or IP address.
    - Returns True if valid.
    - Logs an error and returns False if invalid.
    """
    try:
        parsed = urlparse(target)
        if parsed.scheme in ["http", "https"]:
            return True  # Assume URL is valid
        else:
            ip = ipaddress.ip_address(parsed.path)  # This will raise ValueError if not a valid IP
            if ip.is_private:
                return True
            else:
                error_msg = f"⚠ ERROR: Unauthorized scan attempt on public IP address {ip}. Exiting."
                log_error(error_msg)
                print(error_msg)
                return False
    except ValueError:
        error_msg = f"⚠ ERROR: Invalid format for URL or IP address: {target}. Exiting."
        log_error(error_msg)
        print(error_msg)
        return False

def run_gobuster(url):
    """
    Test Gobuster to enumerate directories on a given URL.
    """
    wordlist = "/usr/share/wordlists/dirb/big.txt"
    extensions = "php,txt,html,js"
    output_file = "outputs/gobuster_results.txt"
    command = [
        'gobuster', 'dir', '-u', url, '-w', wordlist,
        '-b', '302,404', '-x', extensions, '-k',
        '-o', output_file
    ]
    
    try:
        print("Executing command...")
        subprocess.run(command, check=True, text=True)
        print(f"Gobuster scan completed. Results are saved to '{output_file}'")
        print("\nWhat is Gobuster?")
        print("Gobuster is a tool used to brute-force:\n- URIs (directories and files) in web sites.\n- DNS subdomains (with wildcard support).")
        print("\nWhat can you do next with the results?")
        print("1. Review the list of discovered directories and files.")
        print("2. Investigate any unusual or unexpected endpoints.")
        print("3. Attempt to access secured areas or files indicated in the results.")
        print("4. Use the findings to further assess the security of the target application.")
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to run Gobuster: {str(e)}")
        print(f"⚠ An error occurred while running Gobuster: {str(e)}")

if __name__ == "__main__":
    setup_logging()
    check_root_privileges()
    show_warning()
    url = input("Enter the target URL or IP address (e.g., http://192.168.56.105): ").strip()
    if validate_url_or_ip(url):
        run_gobuster(url)
