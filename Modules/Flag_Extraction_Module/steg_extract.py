import os
import subprocess
import logging

# Setup folders
LOG_DIR = "logs"
OUTPUT_DIR = "output"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "stego_analysis.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define error logging function
def log_error(message):
    with open(ERROR_LOG_FILE, "a") as error_log:
        error_log.write(f"[ERROR] {message}\n")
    logging.error(message)
    print(f"[ERROR] {message}")
    print(f"⚠ The error has been logged in: {ERROR_LOG_FILE}")

# Validate file input
def validate_file(image_path):
    if not image_path:  
        log_error("No input provided. Please enter a valid file path.")
        exit()
    if not os.path.isfile(image_path):  
        log_error(f"File does not exist: {image_path}")
        return False
    return True

def check_hidden_data(image_path):
    """Checks if an image contains hidden data using steghide."""
    try:
        result = subprocess.run(["steghide", "info", image_path], capture_output=True, text=True)
        output = result.stdout.strip().lower()

        print("\n[DEBUG] Steghide Output:\n", output, "\n")
        logging.info("[INFO] Steghide output for %s: %s", image_path, output)

        if "no embedded data" in output or "nothing to do" in output:
            print("[INFO] No hidden data found.")
            logging.info("[INFO] No hidden data in %s", image_path)
            return False
        
        print("[SUCCESS] Hidden data detected!")
        logging.info("[SUCCESS] Hidden data found in %s", image_path)
        return True

    except Exception as e:
        log_error(f"Error checking hidden data: {e}")
        return False

def extract_hidden_data(image_path, password=None):
    """Extracts hidden data from an image using steghide."""
    output_file = os.path.join(OUTPUT_DIR, "extracted_data.txt")

    try:
        if os.path.exists(output_file):
            os.remove(output_file)

        cmd = ["steghide", "extract", "-sf", image_path, "-xf", output_file]
        if password:
            cmd.extend(["-p", password])

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.lower()

        if "could not extract" in output or not os.path.exists(output_file):
            log_error(f"Failed to extract data from {image_path}")
            return False
        
        if os.path.getsize(output_file) == 0:
            log_error(f"Extraction resulted in an empty file: {output_file}")
            return False
        
        print(f"[SUCCESS] Hidden data extracted to {output_file}")
        logging.info("[SUCCESS] Extracted hidden data from %s to %s", image_path, output_file)
        return True
    except Exception as e:
        log_error(f"Error extracting data: {e}")
        return False

def brute_force(image_path, wordlist):
    """Attempts to brute-force the steghide password using a wordlist."""
    try:
        if not os.path.exists(wordlist):
            log_error(f"Wordlist file not found: {wordlist}")
            return False

        with open(wordlist, "r", encoding="ISO-8859-1", errors="ignore") as f:
            passwords = f.read().splitlines()

        for password in passwords:
            print(f"[INFO] Trying password: {password}")
            if extract_hidden_data(image_path, password):
                print(f"[SUCCESS] Password found: {password}")
                logging.info("[SUCCESS] Brute-force success: Password %s", password)
                return True

        log_error(f"Brute-force failed on {image_path}")
        return False
    except Exception as e:
        log_error(f"Error during brute-force: {e}")
        return False

def display_results(image_path, hidden_data_found, extracted_data_path):
    """Displays a summary of the analysis and extraction process."""
    print("\n📊 **Summary of Actions Taken** 📊")
    print("-----------------------------------------------------")
    print(f"🔍 **Image Analyzed**: {image_path}")
    print("🛠 **Tool Used**: Steghide (Steganography Detection & Extraction)")
    print("🧐 **Process Performed**:")
    print("   - Checked if the image contains hidden data using `steghide info`")
    print("   - Attempted extraction if hidden data was detected")

    if hidden_data_found:
        print("✅ **Hidden Data Found**: Yes")
        print(f"📂 **Extracted Data Location**: {extracted_data_path}")
    else:
        print("❌ **Hidden Data Found**: No")

    print("-----------------------------------------------------")
    print("📌 **How Steghide Works:**")
    print("Steghide is a tool used to **hide and extract** secret data inside images or audio files.")
    print("1️⃣ It scans the file to check if **hidden content** exists.")
    print("2️⃣ If detected, it attempts to **extract the data** (requires a password).")
    print("3️⃣ If the password is unknown, a **brute-force attack** can try common passwords.")
    print("4️⃣ If successful, the hidden content is **saved in a separate text file**.")

    print("\n📌 **Next Steps:**")
    print("- 🔍 **If extraction failed**, try using a **different password or wordlist**.")
    print("- 🛠 **For encrypted hidden data**, consider **decryption techniques**.")
    print("- 📜 **Try checking other file types** (audio, video) for steganographic content.")

    print("\n🚀 **This tool automates steganography detection & extraction, making it easier to uncover hidden messages!**")

if __name__ == "__main__":
    image = input("Enter the path of the image (e.g., /home/kali/image.jpg): ").strip()

    if not validate_file(image):  
        exit()

    print("Press 'ENTER' to continue...")
    input()  

    hidden_data_found = check_hidden_data(image)
    extracted_data_path = os.path.join(OUTPUT_DIR, "extracted_data.txt")

    if hidden_data_found:
        choice = input("Do you know the password? (y/n): ").strip().lower()
        if choice == "y":
            password = input("Enter the password: ")
            extract_hidden_data(image, password)
        else:
            use_bruteforce = input("Do you want to try brute-force? (y/n): ").strip().lower()
            if use_bruteforce == "y":
                wordlist = input("Enter the path of the wordlist (e.g., /usr/share/wordlists/rockyou.txt): ")
                brute_force(image, wordlist)

    display_results(image, hidden_data_found, extracted_data_path)

