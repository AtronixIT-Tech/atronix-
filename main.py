import os
import sys
import subprocess


def show_banner():
    """Display the tool banner."""
    banner = """
    ___    ___    ___    ___    _ _    _ __    _   _    ___    _     ___    ___    _    _  _    ___  
   | . ||_ _|| . \| . || \ || |\ \/   | ||_ _| < >   / __>| . || |  | | ||_ _|| || . || \ |/ __>
   |   | | | |   /| | ||   || | \ \   | | | |  /.\/  \__ \| | || |_ | ' | | | | || | ||   |\__ \ 
   |_|_| |_| |_\_\`___'|_\_||_|_/\_\  |_| |_|  \_/\  <___/`___'|___|`___' |_| |_|`___'|_\_|<___/
   
    🚀 Welcome to the Atronix CTF Automation Tool! 🚀

    This tool helps automate repetitive tasks in CTF challenges.

    ⚠️ This tool is intended for ethical and legal use only. Any misuse of this tool is strictly prohibited. ⚠️
    """
    print(banner)

def show_warning():
    """Display an ethical warning and require user agreement."""
    print("\n==================================================================")
    print("⚠️ WARNING: This tool is for ethical and educational purposes ONLY.")
    print("By using this tool, you agree to:")
    print("1. Use it only in authorized environments such as CTF competitions.")
    print("2. Never use it on unauthorized targets.")
    print("3. Comply with all applicable laws and ethical hacking guidelines.")
    print("==================================================================\n")

    agreement = input("Do you agree to these terms? [y for yes/ n for no]: ").strip().lower()
    if agreement != "y":
        print("⚠ You must agree to the terms to use this tool. Exiting...")
        sys.exit(1)

def run_script(script_path, args=""):
    """Run the script safely"""
    try:
        subprocess.run(f"python3 {script_path} {args}", shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"⚠ Error occurred while running {script_path}.")

### RECON MODULE ###
def recon_module():
    while True:
        print("""
	 +-+-+-+-+-+ +-+-+-+-+-+-+
	 |R|e|c|o|n| |M|o|d|u|l|e|
	 +-+-+-+-+-+ +-+-+-+-+-+-+ """)
        print("\n")

        print("1. Port & Service Discovery")
        print("2. Directory Enumeration")
        print("3. Go Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            run_script("Modules/Recon_Module/nmap_recon.py")
        elif choice == "2":
            run_script("Modules/Recon_Module/gobuster_enum.py")
        elif choice == "3":
            break
        else:
            print("⚠ Invalid choice. Please try again.")

### EXPLOIT MODULE ###
def exploit_module():
    while True:
        print("""
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+
	 |E|x|p|l|o|i|t| |M|o|d|u|l|e|
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+ """)
        print("\n")

        print("1. SQL Injection Testing")
        print("2. SSH Brute Forcing")
        print("3. Weak Login Test")
        print("4. Go Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            run_script("Modules/Exploit_Module/sqlmap_exploit.py") 
        elif choice == "2":
            authorization = input("Are you authorized to perform brute force testing? [y for yes/ n for no]: ").strip().lower()
            if authorization == "y":
                run_script("Modules/Exploit_Module/hydra_bruteforce.py")
            else:
                print("❌ Unauthorized access is prohibited. Returning to the menu...")
        elif choice == "3":
            run_script("Modules/Exploit_Module/Weak_login.py")  # Fixed Weak Login Test Path
        elif choice == "4":
            break
        else:
            print("⚠ Invalid choice. Please try again.")

### FLAG EXTRACTION MODULE ###
def flag_extraction_module():
    while True:
        print("""
	 +-+-+-+-+-+ +-+-+-+-+-+-+-+-+
	 |F|l|a|g| |E|x|t|r|a|c|t|i|o|n|
	 +-+-+-+-+-+ +-+-+-+-+-+-+-+-+ """)
        print("\n")

        print("1. File Extraction")
        print("2. Steganography Analysis")
        print("3. Go Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            run_script("Modules/Flag_Extraction_Module/flag_search.py")
        elif choice == "2":
            run_script("Modules/Flag_Extraction_Module/steg_extract.py")
        elif choice == "3":
            break
        else:
            print("⚠ Invalid choice. Please try again.")

### CRYPTO SOLVER MODULE ###
def crypto_solver_module():
    while True:
        print("""
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
	 |C|r|y|p|t|o| |S|o|l|v|e|r| |M|o|d|u|l|e|
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+ """)
        print("\n")

        print("1. Base64 & ROT13 Decoder")
        print("2. Hex & Binary Decoder")
        print("3. Caesar Cipher Brute Force")
        print("4. Go Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            run_script("Modules/Crypto_Module/Base64_ROT13.py")
        elif choice == "2":
            run_script("Modules/Crypto_Module/Hex_Binary.py")
        elif choice == "3":
            run_script("Modules/Crypto_Module/Caesar_Bruteforce.py")
        elif choice == "4":
            break
        else:
            print("⚠ Invalid choice. Please try again.")

### FORENSICS MODULE ###
def forensics_module():
    while True:
        print("""
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
	 |F|o|r|e|n|s|i|c|s| |M|o|d|u|l|e|
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+ """)
        print("\n")

        print("1. Memory Dump Analysis")
        print("2. PCAP File Analysis")
        print("3. Go Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            run_script("Modules/Forensic_Module/Memory_Dump.py")
        elif choice == "2":
            run_script("Modules/Forensic_Module/PCAP.py")
        elif choice == "3":
            break
        else:
            print("⚠ Invalid choice. Please try again.")

### MAIN MENU ###
def main_menu():
    """Display the main menu and handle user selection."""
    while True:
        print("\n========== Main Menu ==========:")
        print("1. Recon Module")
        print("2. Exploit Module")
        print("3. Flag Extraction Module")
        print("4. Crypto Solver Module")
        print("5. Forensics Module")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            recon_module()
        elif choice == "2":
            exploit_module()
        elif choice == "3":
            flag_extraction_module()
        elif choice == "4":
            crypto_solver_module()
        elif choice == "5":
            forensics_module()
        elif choice == "6":
            print("\n👋 Exiting... Thank you for using the CTF Automation Tool!")
            sys.exit(0)
        else:
            print("\n⚠ Invalid choice. Please try again.")

if __name__ == "__main__":
    show_banner()  # Atronix banner is shown here
    show_warning()  # Warning displayed here
    main_menu()  # Main menu is displayed here
