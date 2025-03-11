import paramiko
import logging
import os
from ipaddress import ip_address, ip_network

# Setup the logging directory and file
log_directory = 'logs'
log_filename = 'Fileextraction_errors.log'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, log_filename)

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    filemode='a',  # Append mode
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_private_ip(ip):
    """ Check if an IP address is private. """
    try:
        ip_obj = ip_address(ip)
        private_networks = [
            ip_network('10.0.0.0/8'),
            ip_network('172.16.0.0/12'),
            ip_network('192.168.0.0/16'),
            ip_network('127.0.0.0/8')  # Including loopback addresses as private
        ]
        return any(ip_obj in net for net in private_networks)
    except ValueError:
        return False  # If IP is invalid, treat it as non-private

def list_files_in_common_dirs(host, ssh_user, ssh_password, directories):
    """ List files in common directories on a remote machine via SSH. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    results = {}
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        for directory in directories:
            command = f'ls -la {directory}'
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            
            if stdout.channel.recv_exit_status() == 0:
                results[directory] = output.split('\n')
            else:
                results[directory] = [f"Error listing directory: {stderr.read().decode().strip()}"]

    finally:
        client.close()
    return results

if __name__ == "__main__":
    target_host = input("Enter the target host IP or hostname: ").strip()
    if not target_host:
        logging.error("ERROR: Target IP required. Please try again.")
        print(f"⚠ ERROR: Target IP required. Please try again. Your error has been logged in {log_file_path}.")
        exit()

    if not is_private_ip(target_host):
        logging.error(f"ERROR: Unauthorized scan attempt on public IP address {target_host}. Exiting.")
        print(f"⚠ ERROR: Unauthorized scan attempt on public IP address {target_host}. Exiting. Your error has been logged in {log_file_path}.")
        exit()

    username = input("Enter SSH username: ").strip()
    password = input("Enter SSH password: ").strip()

    # Show the hint immediately after credentials are entered
    print("\n💡 **Hint:** Don't forget to download images for steganography analysis and any files that seem important! 🔍\n")

    common_directories = ["/home", "/root", "/var/www", "/etc", "/etc/shadow"]

    directory_contents = list_files_in_common_dirs(target_host, username, password, common_directories)
    
    print("\n🔍 Listing files in specified directories...\n")
    for directory, content in directory_contents.items():
        print(f"📂 Directory: {directory}")
        for line in content:
            print(f"   {line}")
        print("\n")

    # Continuous File Viewing & Keyword Search Loop
    while True:
        print("\n💡 Options: ")
        print("1️⃣ View the contents of a directory")
        print("2️⃣ View the content of a file")
        print("3️⃣ Search for a keyword in a file")
        print("4️⃣ Download a file to your local machine")
        print("5️⃣ Exit")

        choice = input("\nSelect an option (1/2/3/4/5): ").strip()

        if choice == "5":
            print("\n🚀 **Task complete. Exiting.**")
            break

    # **Ensuring the hint appears AFTER exiting**
    print("\n💡 **Hint:** Don't forget to download images for steganography analysis and any files that seem important! 🔍")





