import os
import sys
import subprocess

# Ensure required directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

def show_banner():
    """Display the tool banner."""
    banner = """
 🚀 Welcome to the CTF Automation Tool! 🚀

This tool helps automate repetitive tasks in CTF challenges.

⚠️ This tool is intended for ethical and legal use only. Any misuse of this tool is strictly prohibited. ⚠️


<!-- /=========================================================================================================================\ -->
<!-- ||                                                                                                                       || -->
<!-- ||    _  _____ ____   ___  _   _ _____  __    ___ _____     ___       ____   ___  _    _   _ _____ ___ ___  _   _ ____   || -->
<!-- ||   / \|_   _|  _ \ / _ \| \ | |_ _\ \/ /   |_ _|_   _|   ( _ )     / ___| / _ \| |  | | | |_   _|_ _/ _ \| \ | / ___|  || -->
<!-- ||  / _ \ | | | |_) | | | |  \| || | \  /     | |  | |     / _ \/\   \___ \| | | | |  | | | | | |  | | | | |  \| \___ \  || -->
<!-- || / ___ \| | |  _ <| |_| | |\  || | /  \     | |  | |    | (_>  <    ___) | |_| | |__| |_| | | |  | | |_| | |\  |___) | || -->
<!-- ||/_/   \_\_| |_| \_|\___/|_| \_|___/_/\_\   |___| |_|     \___/\/   |____/ \___/|_____\___/  |_| |___\___/|_| \_|____/  || -->
<!-- ||                                                                                                                       || -->
<!-- \=========================================================================================================================/ -->
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

def exploit_module():
    """Exploit Module based on the Blueprint."""
    while True:
        print("""
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+
	 |E|x|p|l|o|i|t| |M|o|d|u|l|e|
	 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+ """)
        print("\n")

        print("1. SQL Injection Testing")
        print("2. SSH Brute Forcing")
        print("3. Go Back")

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
            break
        else:
            print("⚠ Invalid choice. Please try again.")

def flag_extraction_module():
    """Flag Extraction Module (Under Construction)."""
    print("\n🏴 Launching Flag Extraction Module...\n")
    print("⚠ This module is under construction.")

def crypto_solver_module():
    """Crypto Solver Module (Under Construction)."""
    print("\n🔑 Launching Crypto Solver Module...\n")
    print("⚠ This module is under construction.")

def forensics_module():
    """Forensics Module (Under Construction)."""
    print("\n🔬 Launching Forensics Module...\n")
    print("⚠ This module is under construction.")

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
    show_banner()
    show_warning()
    main_menu()
