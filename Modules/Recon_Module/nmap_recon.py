import subprocess
import os
import logging
import ipaddress

# File paths
LOG_FILE = "logs/error_log.txt"
SCAN_RESULTS_FILE = "outputs/scan_results.txt"

def setup_logging():
    """
    Set up the logging configuration and ensure the logs directory exists.
    """
    try:
        os.makedirs('logs', exist_ok=True)
        if not os.access("logs", os.W_OK):
            raise PermissionError("The 'logs' directory is not writable.")
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    except PermissionError as e:
        print(f"\n⚠ Logging setup failed: {e}")
        print("⚠ Please ensure the 'logs' directory is writable and try again.")
        exit(1)

def log_error(message):
    """
    Log an error message to the file and print it to the console.
    """
    logging.error(message)
    print(f"\n⚠ ERROR: {message}")
    if os.path.exists(LOG_FILE):
        print(f"⚠ The error has been logged in: {LOG_FILE}")

def warn_if_uncontrolled_environment():
    """
    Display a warning to ensure the script is run in a controlled, private environment.
    """
    print("\n================================================================")
    print("WARNING: This script should only be used in a controlled environment.")
    print("Unauthorized scanning of external or public IPs may violate laws and policies.")
    print("Ensure you have proper permissions before proceeding.")
    print("================================================================\n")

def validate_ip_address(ip):
    """
    Validate if the given IP address is private and log unauthorized attempts.
    - Returns True if the IP is private.
    - Logs an error and returns False if the IP is invalid or public.
    """
    try:
        address = ipaddress.ip_address(ip)
        if not address.is_private:
            log_error(f"Unauthorized scan attempt on public IP address: {ip}")
            return False
        return True
    except ValueError:
        log_error(f"Invalid IP address format: {ip}")
        return False

def run_nmap_syn_scan(target_ip):
    """
    Run an Nmap SYN scan on all ports of the validated target IP address.
    - Outputs the results directly to the console.
    - Saves the results to a file (outputs/scan_results.txt).
    - Logs any errors encountered during the scan.
    """
    if not validate_ip_address(target_ip):
        return

    os.makedirs('outputs', exist_ok=True)
    command = ["sudo", "nmap", "-sS", "-vv", "-T4", target_ip]

    try:
        print(f"\nRunning Nmap SYN scan on all ports for {target_ip}...\n")
        result = subprocess.run(command, capture_output=True, text=True)

        print("Nmap Output:")
        print(result.stdout)

        with open(SCAN_RESULTS_FILE, "w") as file:
            file.write(result.stdout)

        print(f"\nScan results have been saved to {SCAN_RESULTS_FILE}\n")

        if result.stderr:
            log_error(f"Nmap command stderr for IP {target_ip}: {result.stderr}")
            print("Nmap Errors:")
            print(result.stderr)

        print("\n========================== OUTPUT EXPLANATION ==========================")
        print("- 'open': The port is actively accepting connections.")
        print("- 'closed': The port is accessible but no application is listening.")
        print("- 'filtered': The port is blocked by a firewall or filtering device.")
        print("========================================================================\n")

    except subprocess.SubprocessError as e:
        log_error(f"Subprocess error while scanning {target_ip}: {e}")
    except Exception as e:
        log_error(f"An unexpected error occurred: {e}")

def main():
    setup_logging()

    if os.geteuid() != 0:
        log_error("Root privileges are required to run this script. Exiting.")
        print("\n⚠ ERROR: Root privileges are required to run this script. Exiting.")
        exit(1)

    print("\n=============== Welcome to the NMAP Module! ===============")
    print("\n🚀 Welcome to the NMAP Tool! 🚀")
    print("\n⚠ This tool is for ethical hacking and learning purposes only.")
    print("⚠ Do not use it on unauthorized targets.")
    print("\n⚠ WARNING: This tool is for ethical use only.")
    print("By using this tool, you agree to:")
    print("1. Use it only in controlled environments (e.g., CTFs).")
    print("2. Never use it to scan unauthorized targets.")
    print("3. Abide by all applicable laws and policies.")
    agreement = input("\nDo you agree to these terms? [yes/no]: ").strip().lower()

    if agreement != 'yes':
        log_error("User did not agree to the ethical use terms. Exiting.")
        print("\n⚠ ERROR: User did not agree to the ethical use terms. Exiting.")
        if os.path.exists(LOG_FILE):
            print(f"⚠ The error has been logged in: {LOG_FILE}")
        print("⚠ You did not agree to the terms of use. Exiting.")
        exit(1)

    warn_if_uncontrolled_environment()

    target_ip = input("\nEnter target IP address: ").strip()
    if not target_ip:
        log_error("Target IP is required. Please try again.")
        print("\n⚠ Target IP is required. Please try again.")
        return

    if not validate_ip_address(target_ip):
        return

    run_nmap_syn_scan(target_ip)

if __name__ == "__main__":
    main()
