# traffic_generator_wizard

1. Script Summary Section:

Summary: Traffic Generator Wizard is a Python script designed to generate network traffic and simulate communication with a specified destination. It allows users to customize the number, size, and type of packets to be sent over TCP, UDP, or both. The script logs the traffic generation process, providing insights into the sent packets.

2. Requirements Section:

Requirements:

Python 3
Ensure Python 3 is installed before running the script.
Installation: sudo apt install python3 -y

Netcat (nc) utility
Ensure netcat is installed before running the script.
Installation: sudo apt install netcat -y

3. Execution Section:

Execution Instructions:
Download the script using:

curl -sLo /tmp/traffic_generator_wizard.py https://raw.githubusercontent.com/edino/traffic_generator_wizard/main/traffic_generator_wizard.py

Run the script using:

sudo python3 /tmp/traffic_generator_wizard.py

or

curl -s https://raw.githubusercontent.com/edino/traffic_generator_wizard/main/traffic_generator_wizard.py | python3 -

4. Code Explanation:

The script checks if Python 3 is installed and exits if not.

It verifies the presence of the netcat (nc) utility and exits if not found, providing installation instructions.

Logs are configured using the logging module, and a log file named traffic_generator_wizard.log is created.

User inputs are collected for IP address, packet count, packet size, packet interval, destination port, and port type (TCP, UDP, or Both).

The generate_traffic function is responsible for sending packets based on user inputs using netcat.

Traffic can be sent over TCP, UDP, or both, with appropriate logging for each case.

The main function initiates the script execution, handling user inputs and calling the traffic generation function.

5. How to Use:

Clone the repository or download the script from the provided URL.

Ensure Python 3 and netcat are installed on your system.

Run the script using the provided execution instructions.

Follow the prompts to customize the traffic generation parameters.

Analyze the logs for insights into the sent packets and traffic generation process.
