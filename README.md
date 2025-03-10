# CTF Automation Tool

## Overview
The **CTF Automation Tool** is a Python-based solution designed to automate reconnaissance tasks commonly required in Capture-the-Flag (CTF) challenges. This tool:

The tool is intended for use in **isolated virtual environments**, such as Kali Linux or any system supporting Python.

⚖️ Legal Disclaimer
This tool is strictly for educational purposes. It is designed to be used in legal and authorized environments only, such as:

Capture-the-Flag (CTF) competitions
Cybersecurity learning and research
Testing in a controlled lab environment
By using this tool, you agree to take full responsibility for any misuse.


# 🚀 CTF Automation Tool

## 📖 Overview
The **CTF Automation Tool** is a comprehensive Python-based project designed to automate **common penetration testing and Capture-the-Flag (CTF) tasks**. It provides a streamlined workflow for **reconnaissance, exploitation, analysis, and flag extraction** — everything needed to assess and investigate a target system.

---

## 🛠️ Features

✔️ **Port Scanning** using `nmap`  
✔️ **Directory Enumeration** using `gobuster`  
✔️ **SQL Injection Testing** using `sqlmap`  
✔️ **SSH Brute Force Attack** using `hydra`  
✔️ **Weak Login Detection** using custom checks  
✔️ **Steganography Analysis** for hidden messages in images  
✔️ **File Extraction** from hidden or suspicious files  
✔️ **Base64 & ROT13 Decoding** automation  
✔️ **Hex & Binary Decoding** automation  
✔️ **Caesar Cipher Brute Force**  
✔️ **Memory Dump Analysis** for forensic inspection  
✔️ **PCAP Analysis** for network traffic review  

---

## 📂 Project Structure

| Tool # | Tool Name               | Description |
|---|---|---|
| 1️⃣  | Port Scan (nmap)         | Scan for open ports & services |
| 2️⃣  | Directory Scan (gobuster) | Find hidden directories/files |
| 3️⃣  | SQL Injection Test (sqlmap) | Detect & exploit SQL injection |
| 4️⃣  | SSH Brute Force (hydra)   | Brute force SSH credentials |
| 5️⃣  | Weak Login Checker        | Detect weak/default logins |
| 6️⃣  | Steganography Analysis    | Uncover hidden messages in images |
| 7️⃣  | File Extraction           | Analyze and extract file contents |
| 8️⃣  | Base64 & ROT13 Decoder    | Decode encoded messages |
| 9️⃣  | Hex & Binary Decoder      | Convert encoded data into readable form |
| 🔟  | Caesar Cipher Brute Force | Crack Caesar Cipher messages |
| 1️⃣1️⃣ | Memory Dump Analysis     | Inspect system memory for sensitive data |
| 1️⃣2️⃣ | PCAP Analysis           | Analyze network traffic for clues |

---

1. Cloning or Copying the Project
Click on code and download zip, after unzip the folder and in the settings of your VM plavce it into the shared folder and check auto-mount.
If you have downloaded the project or placed it in a VirtualBox Shared Folder, follow these steps:

Open a terminal in Kali Linux.

Navigate to the /media directory to check if the shared folder is available:

ls /media/
You should see something like sf_atronix--main.

Copy the folder to your home directory:

cp -r /media/sf_atronix--main ~/atronix--main
If the shared folder has a (1) at the end, you must escape the parentheses like this:

cp -r /media/sf_atronix--main_\(1\) ~/atronix--main
3. Navigate to the Project Directory
Once copied, move into the project folder:

cd ~/atronix--main/atronix--main
4. Verify Files
Check if main.py and required folders exist:

ls -l
You should see main.py and directories like Modules, Logs, and Outputs.

5. Install Dependencies
Ensure required dependencies are installed:

pip3 install -r requirements.txt
6. Run the Tool
Start the CTF Automation Tool by running:
python3 main.py

🛠️ How to Use Each Module
Once you run main.py, you will be presented with a main menu to select different modules.

🔍 Recon Module
Port & Service Discovery: Runs nmap to identify open ports.
Directory Enumeration: Uses gobuster to scan hidden directories.
💥 Exploitation Module
SQL Injection Testing: Uses sqlmap to check for SQL vulnerabilities.
SSH Brute Force: Uses hydra to brute force SSH logins.
Weak Login Testing: Checks for default and weak credentials.
🏴 Flag Extraction
Steganography Analysis: Uses steghide to detect hidden data in images.
File Extraction: Identifies and extracts data from suspicious files.
🔑 Crypto Solver
Base64 & ROT13 Decoder: Converts encoded text back to plaintext.
Hex & Binary Decoder: Converts hex/binary to readable text.
Caesar Cipher Brute Force: Cracks Caesar cipher messages.
🕵️ Forensics Module
Memory Dump Analysis: Analyzes memory dumps for sensitive data.
PCAP Analysis: Reviews captured network traffic.

📬 Contact
For inquiries, bugs, or improvements, please open an issue in the repository.


