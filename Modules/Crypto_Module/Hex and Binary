import binascii
import logging
import re
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

def hex_to_text(hex_string):
    """Convert Hexadecimal to Plaintext with error handling."""
    hex_string = hex_string.strip()
    if not hex_string:
        log_error("No input provided for Hex decoding.")
        return "[ERROR] No input provided!"

    if not re.fullmatch(r"[0-9A-Fa-f ]+", hex_string):  # Ensure only valid Hex characters
        log_error("Invalid Hex input! Allowed: 0-9, A-F.")
        return "[ERROR] Invalid Hex input!"

    try:
        decoded_text = bytes.fromhex(hex_string).decode("utf-8")
        save_decoded_message(decoded_text, "Hex")
        return decoded_text
    except ValueError:
        log_error("Invalid Hex input! Decoding failed.")
        return "[ERROR] Invalid Hex input!"

def binary_to_text(binary_string):
    """Convert Binary to Plaintext with error handling."""
    binary_string = binary_string.strip()
    if not binary_string:
        log_error("No input provided for Binary decoding.")
        return "[ERROR] No input provided!"

    if not re.fullmatch(r"[01 ]+", binary_string):  # Ensure only 0 and 1
        log_error("Invalid Binary input! Only 0s and 1s allowed.")
        return "[ERROR] Invalid Binary input!"

    try:
        binary_values = binary_string.split()
        ascii_characters = [chr(int(b, 2)) for b in binary_values]
        decoded_text = "".join(ascii_characters)
        save_decoded_message(decoded_text, "Binary")
        return decoded_text
    except ValueError:
        log_error("Invalid Binary input! Decoding failed.")
        return "[ERROR] Invalid Binary input!"

if __name__ == "__main__":
    print("🚀 Hex & Binary Decoder Tool 🚀")

    try:
        while True:
            print("\nChoose an option:")
            print("1. Decode Hex to Text")
            print("2. Decode Binary to Text")
            print("3. Exit")

            choice = input("Enter choice (1/2/3): ").strip()

            if not choice:
                log_error("No input provided for menu selection.")
                print("[ERROR] You must enter 1, 2, or 3.")
                continue

            if choice == "1":
                hex_input = input("Enter Hex string: ").strip()
                decoded_text = hex_to_text(hex_input)
                print(f"🔍 Decoded Text: {decoded_text}")

            elif choice == "2":
                binary_input = input("Enter Binary string (separate each byte with a space): ").strip()
                decoded_text = binary_to_text(binary_input)
                print(f"🔍 Decoded Text: {decoded_text}")

            elif choice == "3":
                print("🔚 Exiting...")
                break

            else:
                log_error(f"Invalid menu choice: {choice}")
                print("[ERROR] Invalid choice! Please select 1, 2, or 3.")

    except KeyboardInterrupt:
        print("\n[INFO] Program terminated by user. Exiting...")
