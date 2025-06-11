import subprocess
import os
import time

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\n[!] Operation interrupted.")
    finally:
        exit()

def openvpn_menu():
    print("\n[OpenVPN]")
    search_paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~"),
        "/etc/openvpn",
        "/root/Desktop"
    ]

    found_files = []
    for path in search_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".ovpn"):
                    found_files.append(os.path.join(path, file))

    if not found_files:
        print("[!] No .ovpn files found, bro.")
        time.sleep(2)
        return

    print("➤ Found .ovpn files:")
    for i, file in enumerate(found_files):
        print(f"[{i+1}] {file}")

    choice = input("➤ Which one do you want to select? ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(found_files):
            config_path = found_files[index]
            print(f"[+] Selected: {config_path}")
            cmd = f"openvpn --config \"{config_path}\""
            run_command(cmd)
        else:
            print("[!] Wrong choice, bro.")
            time.sleep(1)
    except ValueError:
        print("[!] Please enter a number, bro.")
        time.sleep(1)


def nmap_menu():
    print("\n[Nmap]")
    target = input("➤ Target IP or domain: ")
    print("""
[1] Deep and fast scan (-p- -A --open -T4)
[2] TCP SYN Scan (-sS)
[3] Service Version Detection (-sV)
[4] OS Detection (-O)
[5] Full Scan (-sS -sV -O)
[6] Enter your own scan type
    """)
    scan_choice = input("➤ Choose scan number: ")

    if scan_choice == "1":
        scan_type = "-p- -A --open -T4"
    elif scan_choice == "2":
        scan_type = "-sS"
    elif scan_choice == "3":
        scan_type = "-sV"
    elif scan_choice == "4":
        scan_type = "-O"
    elif scan_choice == "5":
        scan_type = "-sS -sV -O"
    elif scan_choice == "6":
        scan_type = input("➤ Enter your own `nmap` parameters: ")
    else:
        print("[!] Wrong choice, bro!")
        time.sleep(1)
        return

    cmd = f"nmap {scan_type} {target}"
    run_command(cmd)

def sherlock_menu():
    print("\n[Sherlock]")
    username = input("➤ Username: ").strip()
    
    # Automatic sherlock path
    sherlock_path = os.path.expanduser("~/sherlock/sherlock_project/sherlock.py")

    if os.path.exists(sherlock_path):
        print(f"[+] Sherlock found: {sherlock_path}")

        save = input("➤ Do you want to save the result to a file? (y/n): ").strip().lower()
        if save == "y":
            file_name = input("➤ File name (default: sherlock_output.txt): ").strip()
            if not file_name:
                file_name = "sherlock_output.txt"
            cmd = f"python3 \"{sherlock_path}\" {username} > {file_name}"
        else:
            cmd = f"python3 \"{sherlock_path}\" {username}"

        run_command(cmd)
    else:
        print("[!] Sherlock not found, bro. Check the path.")
        time.sleep(2)


import re

def is_valid_ip(ip):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip)

def is_valid_domain(domain):
    return re.match(r"^(?!\-)(?:[a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,}$", domain)

def whois_menu():
    print("\n[Whois]")
    target = input("➤ Domain or IP address: ").strip()

    if not (is_valid_ip(target) or is_valid_domain(target)):
        print("[!] Wrong domain or IP format, bro.")
        time.sleep(2)
        return

    save = input("➤ Do you want to save the result to a file? (y/n): ").strip().lower()
    if save == "y":
        file_name = input("➤ File name (default: whois_output.txt): ").strip()
        if not file_name:
            file_name = "whois_output.txt"
        cmd = f"whois {target} > {file_name}"
    else:
        cmd = f"whois {target}"

    run_command(cmd)


def hydra_menu():
    print("\n[Hydra]")
    ip = input("➤ Target IP: ")
    service = input("➤ Service (ssh, ftp, http, etc): ")
    user = input("➤ Username: ")
    passlist = input("➤ Password list path: ")
    cmd = f"hydra -l {user} -P {passlist} {ip} {service}"
    run_command(cmd)

def gobuster_menu():
    print("\n[Gobuster]")
    url = input("➤ URL (http://ip): ")
    wordlist = input("➤ Wordlist path: ")
    cmd = f"gobuster dir -u {url} -w {wordlist}"
    run_command(cmd)

def hash_identifier_menu():
    print("\n[Hash Cracker Menu]")

    hash_value = input("➤ Enter hash value: ").strip()
    with open("temp_hash.txt", "w") as f:
        f.write(hash_value + "\n")

    # Use hashid to identify hash type
    print("\n[+] Detecting hash type...\n")
    try:
        output = subprocess.check_output(f"echo '{hash_value}' | hashid -m", shell=True, text=True)
    except Exception as e:
        print("[!] hashid error:", e)
        time.sleep(2)
        return

    print("[+] Possible hash types:\n")
    print(output)

    # Manual selection for hashcat
    print("➤ Select the most appropriate hash type:")
    print("""
[1] MD5 (-m 0)
[2] SHA1 (-m 100)
[3] SHA256 (-m 1400)
[4] bcrypt (-m 3200)
[5] NTLM (-m 1000)
[6] SHA512 (-m 1700)
    """)
    method = input("➤ Choice: ").strip()

    hashcat_modes = {
        "1": "0",       # MD5
        "2": "100",     # SHA1
        "3": "1400",    # SHA256
        "4": "3200",    # bcrypt
        "5": "1000",    # NTLM
        "6": "1700"     # SHA512
    }

    if method not in hashcat_modes:
        print("[!] Wrong choice, bro.")
        time.sleep(2)
        return

    mode = hashcat_modes[method]
    wordlist = input("➤ Wordlist path: ").strip()

    cmd = f"hashcat -a 0 -m {mode} temp_hash.txt {wordlist}"
    run_command(cmd)



def steghide_menu():
    print("\n[Steghide]")
    mode = input("➤ Select mode (extract/embed): ")
    if mode == "extract":
        file = input("➤ Stego file: ")
        cmd = f"steghide extract -sf {file}"
    else:
        carrier = input("➤ Image file: ")
        sec
