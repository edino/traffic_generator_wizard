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
from datetime import datetime, timezone, timedelta
import os

LOG_FILE = os.path.join(os.getcwd(), "traffic_generator_wizard.log")

def get_user_input(prompt, default=None, instructions=None):
    full_prompt = f"{prompt}{' (default: ' + f'{default})' if default else ''}: "
    if instructions:
        full_prompt += f"\n{instructions}"
    try:
        user_input = input(full_prompt)
        logging.info(f"User input: {user_input}")
        return user_input if user_input else default
    except (EOFError, KeyboardInterrupt):
        logging.info("Script execution terminated.")
        sys.exit(0)

def validate_positive_integer(value, error_message):
    while True:
        try:
            num = int(value)
            if num <= 0:
                raise ValueError("Please enter a positive integer.")
            return num
        except ValueError:
            value = get_user_input(error_message)

def validate_port_type(port_type):
    valid_port_types = ["tcp", "udp", "both"]
    while True:
        if port_type.lower() in valid_port_types:
            return port_type.lower()
        else:
            port_type = get_user_input("\nEnter a valid port type (TCP, UDP, or Both)", instructions="(default: Both)")

def generate_traffic(destination, count, size, interval, port, port_type, verbose=False, execution_time=None):
    log_file = os.path.abspath(LOG_FILE)
    script_location = os.path.abspath(__file__)

    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S %Z")
        print(f"\nLive verbose view enabled. Press Ctrl+C to stop viewing and continue with script execution.")
        print(f"Script Location: {script_location}")
        print(f"Log File Path: {log_file}")

    if count == '' or count == float('inf'):
        count = sys.maxsize
    else:
        count = validate_positive_integer(count, "\nEnter the number of packets to send (e.g., 100)")

    if execution_time:
        execution_time = validate_positive_integer(
            execution_time,
            "\nEnter the duration of script execution in seconds (e.g., 30)"
        )
    else:
        print("\nRunning the script until terminated.")

    size = validate_positive_integer(size, "\nEnter the size of each packet in bytes (e.g., 1500)")
    interval = validate_positive_integer(interval, "\nEnter the interval between packets in seconds (e.g., 1)")
    port = validate_positive_integer(port, "\nEnter the destination port (e.g., 9000)")
    port_type = validate_port_type(get_user_input("\nEnter the type of port (TCP, UDP, or Both)", instructions="(default: Both)"))

    try:
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(seconds=execution_time) if execution_time else None

        while True:
            # Rest of the code...
            if count > 0 or (end_time and datetime.now(timezone.utc) < end_time):
                count -= 1
            else:
                logging.info("Script execution terminated. Reason: Packet count or execution time reached.")
                break
    except KeyboardInterrupt:
        logging.info("Script execution terminated. Reason: User interrupt.")

    logging.info(f"Traffic generation completed at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")

def main():
    print("\nWelcome to the Traffic Generator Wizard Python Script!")

    destination = get_user_input("\nEnter the destination IP or hostname", instructions="(e.g., example.com or 8.8.8.8)")
    count = get_user_input("\nEnter the number of packets to send", default="", instructions="(press Enter to run until terminated)")
    
    if not count:
        execution_time = None
        ask_execution_time = get_user_input("\nDo you want to specify the duration of script execution?", instructions="(press Enter to run until terminated)").lower() == 'y'
        
        if ask_execution_time:
            execution_time = validate_positive_integer(get_user_input("\nEnter the duration of script execution in seconds (e.g., 30)"), "Invalid input. Please enter a positive integer.")
        
    else:
        count = validate_positive_integer(count, "\nEnter the number of packets to send (e.g., 100)")
        execution_time = None

    size = validate_positive_integer(get_user_input("\nEnter the size of each packet in bytes", instructions="(press Enter to run Default MSS Packet Size 1460)"), default=1460)
    interval = validate_positive_integer(get_user_input("\nEnter the interval between packets in seconds", instructions="(press Enter to run default interval of 1 second)"), default=1)
    port = validate_positive_integer(get_user_input("\nEnter the destination port", instructions="(press Enter to run default port 443)"), default=443)
    port_type = validate_port_type(get_user_input("\nEnter the type of port (TCP, UDP, or Both)", instructions="(press Enter to run default which is both)"))

    verbose = get_user_input("\nDo you want to see a live verbose view of the execution?", default="y", instructions="(press Enter to run default which is with live view showing timestamps in verbose enabled)").lower() == 'y'

    generate_traffic(destination, count, size, interval, port, port_type, verbose, execution_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Script execution terminated. Reason: User interrupt.")
        sys.exit(0)
