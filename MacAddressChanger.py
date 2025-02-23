import subprocess
import argparse
import re
import sys

def is_valid_mac(mac_address):
    """MAC adresinin geçerli formatta olup olmadığını kontrol eder."""
    mac_regex = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
    return mac_regex.match(mac_address) is not None

def get_current_mac(interface, verbose):
    """Verilen arayüz için mevcut MAC adresini döndürür."""
    try:
        if verbose:
            print(f"Fetching current MAC address for interface {interface}...")
        output = subprocess.check_output(["ifconfig", interface]).decode()
        for line in output.split('\n'):
            if "ether" in line:
                if verbose:
                    print(f"Current MAC address found: {line.split()[1]}")
                return line.split()[1]
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while fetching MAC address: {e}")
    return None

def change_mac(interface, new_mac, verbose):
    """MAC adresini değiştirir."""
    try:
        if verbose:
            print(f"Changing MAC address for interface {interface} to {new_mac}...")
        subprocess.check_call(["sudo", "ifconfig", interface, "down"])
        subprocess.check_call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.check_call(["sudo", "ifconfig", interface, "up"])
        if verbose:
            print(f"MAC address successfully changed to {new_mac} on {interface}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while changing MAC address: {e}")
        sys.exit(1)

def confirm_action(message):
    """Kullanıcıdan onay alır."""
    response = input(f"{message} (yes/no): ").strip().lower()
    if response not in ["yes", "y"]:
        print("Operation canceled.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="MACChanger: Change the MAC address of a network interface.")
    parser.add_argument("-i", "--interface", dest="interface", type=str, help="Interface to change", required=True)
    parser.add_argument("-m", "--mac", dest="mac_address", type=str, help="New MAC address", required=True)
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    if not is_valid_mac(args.mac_address):
        print("Invalid MAC address format. Please use the format XX:XX:XX:XX:XX:XX")
        sys.exit(1)

    current_mac = get_current_mac(args.interface, args.verbose)
    if current_mac:
        print(f"Current MAC Address: {current_mac}")
    else:
        print(f"Could not read MAC address for interface {args.interface}")
        sys.exit(1)

    confirm_action(f"Are you sure you want to change the MAC address for {args.interface} to {args.mac_address}?")

    change_mac(args.interface, args.mac_address, args.verbose)

    new_mac = get_current_mac(args.interface, args.verbose)
    if new_mac == args.mac_address:
        print(f"MAC address successfully changed to {new_mac} on {args.interface}")
    else:
        print(f"Failed to change MAC address. Current MAC address is {new_mac}")

if _name_ == "_main_":
    main()
