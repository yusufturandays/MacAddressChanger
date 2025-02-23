# MAC Address Changer

## Description
This project is a command-line utility written in Python for changing the MAC address of a network interface. It allows network administrators or security professionals to modify the MAC addresses of their network interfaces.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Eraybeylik/MacAddressChanger

# USAGE
Run the script from your terminal or command prompt. Administrative privileges may be required.

## Basic Usage
    python MacAddressChanger.py -i [interface] -m [new_mac_address]
## Example 
    python MacAddressChanger.py -i eth0 -m 00:11:22:33:44:55

# Options
    -i or --interface: The network interface whose MAC address you want to change (e.g., eth0).
    -m or --mac: The new MAC address you want to assign to the interface.
    -v or --verbose: Enable verbose output for detailed information.

## Verbose Mode
    To get detailed output during the operation, use the -v or --verbose option:
        python MacAddressChanger.py -i eth0 -m 00:11:22:33:44:55 -v
