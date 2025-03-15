import paramiko
import getpass
import os
import logging
import ipaddress

# Setup logging directories
os.makedirs("memory_errors", exist_ok=True)
os.makedirs("memory_outputs", exist_ok=True)

ERROR_LOG_FILE = "memory_errors/log"
RESULTS_LOG_FILE = "memory_outputs/results.log"

# Configure error logging
logging.basicConfig(
    filename=ERROR_LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_inform(error_message):
    logging.error(error_message)
    print(f"[-] {error_message}")
    print(f"[!] This error has been logged in: {ERROR_LOG_FILE}\n")

def log_result(result_message):
    with open(RESULTS_LOG_FILE, "a") as log_file:
        log_file.write(result_message + "\n")
    print(f"[+] Result saved to: {RESULTS_LOG_FILE}\n")

def validate_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if not ip_obj.is_private:
            log_and_inform("Public IP addresses are forbidden for this tool.")
            return False
        return True
    except ValueError:
        log_and_inform("Invalid IP format. Please try again.")
        return False

def connect_ssh(host, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=user, password=password)
        print("\n[+] Connected to remote machine successfully.")
        return client
    except Exception as e:
        log_and_inform(f"SSH Connection Failed: {str(e)}")
        exit(1)

def list_files(client):
    stdin, stdout, stderr = client.exec_command("ls -lh /tmp/*.lime 2>/dev/null")
    files = stdout.read().decode().strip()
    if not files:
        log_and_inform("No memory dump files found in /tmp/")
        return None
    print("\n[+] Available Memory Dump Files:\n")
    print(files)
    return files.split("\n")

def view_memory_dump(client):
    dump_files = list_files(client)
    if not dump_files:
        return

    dump_choice = input("\nEnter the FULL PATH of the memory dump you want to view: ").strip()
    if not dump_choice:
        log_and_inform("Memory dump file path is required. User entered nothing.")
        return

    print(f"\n[+] Displaying Full Contents of {dump_choice} (this may take a while)...\n")
    stdin, stdout, stderr = client.exec_command(f"strings {dump_choice}")
    content = stdout.read().decode()
    print(content)

    log_result(f"--- Full Content of {dump_choice} ---\n{content}\n")

    # Explanation for beginners
    explanation = f"""
--- Explanation for Beginners ---

What is a Memory Dump?
----------------------
A memory dump is a snapshot of the active memory (RAM) of a machine at a specific point in time.
It contains all the data stored in memory, including running processes, passwords, files being edited, network connections, and more.

What did this tool do?
----------------------
- It connected to the remote machine over SSH.
- It listed available memory dump files in /tmp.
- You selected a file, and the tool extracted all printable strings from it using the `strings` command.
- This helps you look for passwords, usernames, IP addresses, and other clues.

Why is this useful?
-------------------
Memory dumps are crucial in forensics, malware analysis, and incident response because attackers often leave traces in memory. 
Even if files are deleted, traces may still exist in memory. 

Further Learning:
------------------
- Try searching for keywords like 'password', 'user', or 'flag'.
- Read about tools like `Volatility`, which can analyze memory dumps in even more detail.

This educational output was automatically generated by your tool.
"""
    print(explanation)
    log_result(explanation)

    # Search Feature
    search_word = input("\n[+] Enter a keyword to search in the dump (or press Enter to skip): ").strip()
    if search_word:
        print(f"\n[+] Searching for '{search_word}' in {dump_choice}...\n")
        stdin, stdout, stderr = client.exec_command(f"strings {dump_choice} | grep -i {search_word}")
        search_results = stdout.read().decode().strip()

        if search_results:
            print(search_results)
            log_result(f"--- Search Results for '{search_word}' in {dump_choice} ---\n{search_results}\n")
        else:
            print(f"[-] No results found for '{search_word}'.")
            log_result(f"--- No results found for '{search_word}' in {dump_choice} ---\n")

def crack_hash():
    hash_input = input("\nEnter the hash you want to crack: ").strip()
    if not hash_input:
        log_and_inform("Hash input is required. User entered nothing.")
        return

    with open("hashes.txt", "w") as file:
        file.write(hash_input + "\n")

    print("\n[+] Identifying hash type...")
    os.system("john --list=formats | grep -i md5")

    print("\n[+] Attempting to crack hash using MD5 format...\n")
    os.system("john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt")

    result = os.popen("john --show --format=Raw-MD5 hashes.txt").read()
    print("\n[+] Cracked Passwords:\n", result if result else "[-] No password cracked.")

    log_result(f"--- Cracked Hash: {hash_input} ---\n{result if result else 'No password cracked.'}\n")

if __name__ == "__main__":
    print("🚀 Memory Dump Viewer & Hash Cracker 🚀\n")

    host = input("Enter Remote Machine IP: ").strip()
    if not host:
        log_and_inform("Target IP is required. User left it blank.")
        exit(1)
    if not validate_ip(host):
        exit(1)

    user = input("Enter SSH Username: ").strip()
    if not user:
        log_and_inform("SSH username is required. User left it blank.")
        exit(1)

    password = getpass.getpass("Enter SSH Password: ").strip()
    if not password:
        log_and_inform("SSH password is required. User left it blank.")
        exit(1)

    client = connect_ssh(host, user, password)

    while True:
        print("\n[+] Select an option:")
        print("1️⃣ View and analyze memory dumps")
        print("2️⃣ Crack a password hash")
        print("3️⃣ Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_memory_dump(client)
        elif choice == "2":
            crack_hash()
        elif choice == "3":
            print("Exiting... Goodbye!")
            client.close()
            exit(0)
        else:
            log_and_inform(f"Invalid choice entered: {choice}")

