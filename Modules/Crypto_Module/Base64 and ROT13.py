import base64
import codecs
import logging
import os
from datetime import datetime

# Ensure necessary directories exist
OUTPUT_DIR = "outputs"
DECODED_FILES_DIR = os.path.join(OUTPUT_DIR, "decoded_files")
LOG_FILE = os.path.join(OUTPUT_DIR, "decoder_errors.log")

os.makedirs(DECODED_FILES_DIR, exist_ok=True)

# Setup logging
try:
    logging.basicConfig(
        filename=LOG_FILE, 
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
except Exception as e:
    print(f"[ERROR] Logging setup failed: {e}")

def log_error(message):
    """Logs error messages to a file and prints to console."""
    try:
        logging.error(message)
    except Exception as e:
        print(f"[ERROR] Could not write to log file: {e}")
    print(f"[ERROR] {message}")
    print(f"⚠ The error has been logged in: {LOG_FILE}")

def save_decoded_message(decoded_text, encoding_type):
    """Saves decoded messages to a separate file in the decoded_files folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{encoding_type}_decoded_{timestamp}.txt"
    file_path = os.path.join(DECODED_FILES_DIR, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(decoded_text)
        print(f"📂 Decoded message saved in: {file_path}")
    except Exception as e:
        log_error(f"Could not save decoded message: {e}")

def decode_base64(encoded_string):
    """Decodes a Base64 encoded string and saves it."""
    encoded_string = encoded_string.strip()
    if not encoded_string:
        log_error("No input provided for Base64 decoding.")
        return "[ERROR] No input provided!"

    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_text = decoded_bytes.decode("utf-8")
        save_decoded_message(decoded_text, "Base64")
        return decoded_text
    except Exception:
        log_error("Invalid Base64 input! Decoding failed.")
        return "[ERROR] Invalid Base64 input!"

def decode_rot13(encoded_string):
    """Decodes a ROT13 encoded string and saves it."""
    encoded_string = encoded_string.strip()
    
    if not encoded_string:
        log_error("No input provided for ROT13 decoding.")
        return "[ERROR] No input provided!"

    try:
        decoded_text = codecs.decode(encoded_string, "rot_13")
        save_decoded_message(decoded_text, "ROT13")
        return decoded_text
    except Exception:
        log_error("ROT13 decoding failed.")
        return "[ERROR] ROT13 decoding failed!"

if __name__ == "__main__":
    print("🚀 Base64 & ROT13 Decoder Tool 🚀")

    try:
        while True:
            print("\nChoose an option:")
            print("1. Decode Base64")
            print("2. Decode ROT13")
            print("3. Exit")

            choice = input("Enter choice (1/2/3): ").strip()

            if not choice:
                log_error("No input provided for menu selection.")
                print("[ERROR] You must enter 1, 2, or 3.")
                continue

            if choice == "1":
                base64_input = input("Enter Base64 string: ").strip()
                decoded_text = decode_base64(base64_input)
                print(f"🔍 Decoded Text: {decoded_text}")

            elif choice == "2":
                rot13_input = input("Enter ROT13 string: ").strip()
                decoded_text = decode_rot13(rot13_input)
                print(f"🔍 Decoded Text: {decoded_text}")

            elif choice == "3":
                print("🔚 Exiting...")
                break

            else:
                log_error(f"Invalid menu choice: {choice}")
                print("[ERROR] Invalid choice! Please select 1, 2, or 3.")

    except KeyboardInterrupt:
        print("\n[INFO] Program terminated by user. Exiting...")
