import paramiko
import logging
import os
from ipaddress import ip_address, ip_network

# Setup the logging directory and file
log_directory = 'logs'
log_filename = 'Pcap_extraction_errors.log'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, log_filename)

# Configure logging to log errors to a file
logging.basicConfig(
    filename=log_file_path,
    filemode='a',  # Append mode
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to check if an IP address is private or public
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

# Function to list PCAP files in specified directories on the target machine
def list_pcap_files_in_dirs(host, ssh_user, ssh_password, directories):
    """ Search for PCAP files in specified directories on a remote machine via SSH. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pcap_files = []
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        for directory in directories:
            command = f'find {directory} -name "*.pcap"'
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            if output:
                pcap_files.extend(output.split('\n'))
    finally:
        client.close()
    return pcap_files

# Function to view the contents of a PCAP file
def view_pcap_file_contents(host, ssh_user, ssh_password, file_path):
    """ Display a summary of the contents of a PCAP file using tshark. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        
        # Using tshark (a command-line version of Wireshark) to read the PCAP file
        command = f"tshark -r {file_path}"  # tshark command for packet details
        stdin, stdout, stderr = client.exec_command(command)
        contents = stdout.read().decode().strip()
        error_message = stderr.read().decode().strip()

        if error_message:
            return f"❌ Error reading {file_path}: {error_message}"

        if not contents:
            return f"❌ No packets found in {file_path}, or unable to read the file contents."

        return contents
    
    finally:
        client.close()

# Function to download a file from the remote target to the local machine
def download_file(host, ssh_user, ssh_password, file_path, download_path):
    """ Download a file from the target machine to the local machine. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.get(file_path, download_path)
        sftp.close()
        return f"File {file_path} downloaded successfully to {download_path}"
    
    finally:
        client.close()

if __name__ == "__main__":
    # Get the target host IP from the user
    target_host = input("Enter the target host IP or hostname: ").strip()
    
    # Check if the IP address is empty
    if not target_host:
        logging.error("ERROR: Target IP required. Please try again.")
        print(f"⚠ ERROR: Target IP is required. Your error has been logged in {log_file_path}.")
        exit()

    # Validate if the IP is a valid address
    try:
        ip_address(target_host)  # Validate IP
    except ValueError:
        logging.error(f"ERROR: Invalid IP address {target_host}. Exiting.")
        print(f"⚠ ERROR: Invalid IP address {target_host}. Your error has been logged in {log_file_path}.")
        exit()

    # Check if the IP is private or public
    if not is_private_ip(target_host):
        logging.error(f"ERROR: Public IP address {target_host} is forbidden. Exiting.")
        print(f"⚠ ERROR: Public IP address {target_host} is forbidden. Your error has been logged in {log_file_path}.")
        exit()

    # Get the SSH username and password from the user
    username = input("Enter SSH username: ").strip()
    password = input("Enter SSH password: ").strip()
    common_directories = ["/home", "/root", "/var/www", "/etc", "/etc/shadow"]

    # List PCAP files
    pcap_files = list_pcap_files_in_dirs(target_host, username, password, common_directories)

    if not pcap_files:
        print("\n⚠ No PCAP files found.")
    else:
        print("\nFound the following PCAP files:")
        for pcap in pcap_files:
            print(f"📄 PCAP File: {pcap}")
        
        # Option to view the contents of a PCAP file
        file_to_view = input("\nWould you like to view the contents of a PCAP file? (yes/no): ").strip()
        if file_to_view.lower() == "yes":
            file_to_view = input("📄 Enter the full path of the PCAP file you want to view: ").strip()
            pcap_content = view_pcap_file_contents(target_host, username, password, file_to_view)
            print("\n📄 File contents:")
            print(pcap_content)

            # Explanation to the user
            print("\n📄 **Explanation**: The contents displayed above are captured network packets.")
            print("Each packet has a timestamp, the sender and receiver information (MAC address/IP), and the data type.")
            print("This information can be used for network analysis to detect network issues or malicious activity.")

        # Option to download a PCAP file
        file_to_download = input("\nWould you like to download a PCAP file? (yes/no): ").strip()
        if file_to_download.lower() == "yes":
            file_to_download = input("📄 Enter the full path of the PCAP file you want to download: ").strip()
            download_location = input("📂 Enter the full path where you want to save the file (including filename): ").strip()
            download_status = download_file(target_host, username, password, file_to_download, download_location)
            print(download_status)

            # Explanation to the user
            print("\n📄 **Explanation**: By downloading this PCAP file, you can analyze it further on your local machine.")
            print("You can open the file in tools like Wireshark to gain deeper insights into the captured network traffic.")
