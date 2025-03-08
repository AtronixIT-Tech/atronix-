import os
import logging
import string

# Setup Logging
LOG_FILE = "logs/crypto_solver.log"
OUTPUT_FILE = "outputs/caesar_bruteforce_results.txt"

# Ensure necessary directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def log_message(message):
    """Log information and display it."""
    logging.info(message)
    print(message)


def log_error(message):
    """Log an error message and display it."""
    logging.error(message)
    print(f"[!] ERROR: {message} - The error has been logged in {LOG_FILE}")


def caesar_cipher(text, shift):
    """Apply a Caesar cipher shift (decrypting by brute force)."""
    decrypted_text = ""
    for char in text:
        if char in string.ascii_uppercase:
            decrypted_text += chr(((ord(char) - 65 - shift) % 26) + 65)
        elif char in string.ascii_lowercase:
            decrypted_text += chr(((ord(char) - 97 - shift) % 26) + 97)
        else:
            decrypted_text += char  # Leave non-alphabet characters unchanged
    return decrypted_text


def brute_force_caesar(ciphertext):
    """Brute-force all 25 shifts of a Caesar Cipher."""
    if not ciphertext.strip():
        error_message = "[ERROR] Input cannot be empty. Please enter an encrypted message."
        log_error(error_message)
        return

    # Check if the input contains only alphabetic characters (since Caesar cipher works on letters)
    if not all(char.isalpha() or char.isspace() for char in ciphertext):
        error_message = "[ERROR] Invalid format entered. Please enter only alphabetic characters."
        log_error(error_message)
        return

    log_message("\n[+] Starting Caesar Cipher Brute-Force Attack...\n")
    results = []

    for shift in range(1, 26):  # Try all shifts (excluding shift 0)
        decrypted_text = caesar_cipher(ciphertext, shift)
        result = f"Shift {shift}: {decrypted_text}"
        results.append(result)
        print(result)  

    # Save results to a file
    with open(OUTPUT_FILE, "w") as file:
        file.write("\n".join(results))

    log_message("\n[SUCCESS] Brute-force attack completed!")
    log_message(f"[SUCCESS] All possible shifts saved in: {OUTPUT_FILE}")
    log_message("[INFO] Please review the results manually to find the correct decryption.\n")


def main():
    """Main function to run the script."""
    print("\n=============== Brute-Force Caesar Cipher ===============")
    encrypted_text = input("\n🔐 Enter the encrypted text: ").strip()

    if not encrypted_text:
        log_error("[ERROR] Input cannot be empty. Please enter an encrypted message.")
        return

    brute_force_caesar(encrypted_text)


if __name__ == "__main__":
    main()
