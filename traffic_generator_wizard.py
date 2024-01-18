# Copyright Section
# File: traffic_generator_wizard.py
# Copyright © 2024 Edino De Souza
# Repository: https://github.com/edino/traffic_generator_wizard
# License: GNU General Public License v3.0 - https://github.com/edino/traffic_generator_wizard/blob/main/LICENSE
# This file is part of the Traffic Generator Wizard.

# Script Summary Section
# Summary: Traffic Generator Wizard is a Python script designed to generate network traffic and simulate communication with a specified destination. 
# It allows users to customize the number, size, and type of packets to be sent over TCP, UDP, or both. 
# The script logs the traffic generation process, providing insights into the sent packets.
# Author: Edino De Souza Repository: https://github.com/edino/traffic_generator_wizard

# Requirements Section
# Requirements:
#   - Python 3
# Ensure Python 3 is installed before running the script.
# sudo apt install python3 -y

#   - netcat (nc) utility
# Install netcat using: sudo apt-get install netcat
# sudo apt install netcat -y

# BuildDate: 5:51 PM EST 2024-01-17 - Working.

# Execution Section
# Execution Instructions:
# 1. Download the script using:
#    curl -sLo /tmp/traffic_generator_wizard.py https://raw.githubusercontent.com/edino/traffic_generator_wizard/main/traffic_generator_wizard.py
# 2. Run the script using:
#    sudo python3 /tmp/traffic_generator_wizard.py
# or
#    curl -s https://raw.githubusercontent.com/edino/traffic_generator_wizard/main/traffic_generator_wizard.py | python3 -



import subprocess
import sys
import logging
from datetime import datetime, timezone
import os

LOG_FILE = os.path.join(os.getcwd(), "traffic_generator_wizard.log")

def get_user_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        logging.info("Script execution terminated.")
        sys.exit(0)

def generate_traffic(destination, count, size, interval, port, port_type, verbose=False):
    log_file = os.path.abspath(LOG_FILE)

    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S %Z")
        print(f"\nLive verbose view enabled. Press Ctrl+C to stop viewing and continue with script execution.")
        print(f"Script Location: {os.path.abspath(__file__)}")
        print(f"Log File Path: {log_file}")

    if port_type.lower() == "both":
        tcp_count = int(count) // 2
        udp_count = int(count) - tcp_count

        # Send TCP packets
        tcp_command = f"nc -w 1 {destination} {port}"
        logging.info(f"Sending {tcp_count} TCP packets")
        for _ in range(tcp_count):
            subprocess.run(tcp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Send UDP packets
        udp_command = f"nc -w 1 -u {destination} {port}"
        logging.info(f"Sending {udp_count} UDP packets")
        for _ in range(udp_count):
            subprocess.run(udp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    elif port_type.lower() == "udp":
        command = f"nc -w 1 -u {destination} {port}"
        logging.info(f"Sending {count} UDP packets")
        for _ in range(int(count)):
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    elif port_type.lower() == "tcp":
        command = f"nc -w 1 {destination} {port}"
        logging.info(f"Sending {count} TCP packets")
        for _ in range(int(count)):
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    else:
        logging.warning("Invalid port type. No packets sent.")

    logging.info(f"Traffic generation completed at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")

def main():
    print("\nWelcome to the Traffic Generator Wizard Python Script!")

    # Ask the user if they want a live verbose view
    verbose = get_user_input("\nDo you want to see a live verbose view of the execution? (y/n): ").lower() == 'y'

    destination = get_user_input("\nEnter the IP Address or hostname to send traffic to, example.com or 8.8.8.8: ")
    count = get_user_input("\nEnter the number of packets to send: ")
    size = get_user_input("\nEnter the size of each packet in bytes: ")
    interval = get_user_input("\nEnter the interval between packets in seconds: ")
    port = get_user_input("\nEnter the destination port: ")
    port_type = get_user_input("\nEnter the type of port (TCP, UDP, or Both): ")

    generate_traffic(destination, count, size, interval, port, port_type, verbose)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Script execution terminated.")
        sys.exit(0)
