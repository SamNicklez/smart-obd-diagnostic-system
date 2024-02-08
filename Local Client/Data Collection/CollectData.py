# Need to find the address of the OBD II bluetooth and bind it to a serial port.
# Binding command: sudo rfcomm bind rfcomm0 00:1D:A5:05:A4:E3

import obd
import time
import os
import signal
from datetime import datetime

# Global flag to control the loop
keep_running = True

# Ensure the logs directory exists and if not, make it
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

#log_file_path = os.path.join(logs_dir, "obd_data.txt")

# Creating a file name with date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name = f"obd_data_{current_time}.txt"
log_file_path = os.path.join(logs_dir, log_file_name)

# Signal handler function to gracefully exit
def signal_handler(sig, frame):
    global keep_running
    keep_running = False
    print("\nExiting...")

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Function to wait for OBD connection
def wait_for_obd_connection(port='/dev/rfcomm0'):
    connection = None
    while keep_running and connection is None:
        try:
            print("Attempting to connect to OBD-II sensor...")
            connection = obd.OBD(port)
            if not connection.is_connected():
                print("Unable to connect, retrying...")
                connection.close()
                connection = None
                time.sleep(5)  # Wait for 5 seconds before retrying
        except InterruptedError:
            print("Connection attempt interrupted. Exiting...")
            break  # Exit the loop if interrupted
        except Exception as e:
            print(f"Error establishing connection: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
    return connection

# Function for checking if the engine is on
def check_engine_on():
    rpm_response = connection.query(obd.commands.RPM)
    if rpm_response.is_null() or rpm_response.value.magnitude == 0:
        return False  # Engine is off or not responding
    return True  # Engine is on

# Establishing connection
connection = wait_for_obd_connection()

# Functions for unit conversion
def convert_speed_to_mph(speed_km_per_hr):
    return speed_km_per_hr * 0.621371

def convert_celsius_to_fahrenheit(temp_celsius):
    return (temp_celsius * 9/5) + 32

# Function to log a single command
def log_command(command):
    response = connection.query(command)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not response.is_null():
        # Handle responses that are lists
        if isinstance(response.value, list):
            # Join list elements into a string or handle them as needed
            value = ', '.join(str(v) for v in response.value)
            unit = ""  # List responses might not have a unified unit
        else:
            value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value
            unit = str(response.value.units) if hasattr(response.value, 'units') else ""

        # Editing the units to be better
        if command.name == 'SPEED':
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_speed_to_mph(response.value.magnitude)
                unit = "mph"
        elif unit == "degree_Celsius [PASSED]":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_celsius_to_fahrenheit(response.value.magnitude)
                unit = "°F [PASSED]"
        elif unit == "degree_Celsius [FAILED]":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_celsius_to_fahrenheit(response.value.magnitude)
                unit = "°F [FAILED]"
        elif unit == "percent":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                unit = "%" 

        return f"{timestamp} - {command.name}: {value} {unit}"
    else:
        return f"{command.name}: Not Supported or No Data"

# Loop for logging the data
if connection and connection.is_connected():
    print(f"Connected to OBDII sensor. Logging data to {log_file_path}")

    with open(log_file_path, 'w') as file:
        dtc_check_counter = 0  # Counter to determine when to check DTCs
        supported_commands = connection.supported_commands
        while keep_running:
            if not connection.is_connected() or not check_engine_on():
                print("Lost connection to OBDII sensor or engine turned off. Exiting...")
                break  # Exit the loop if connection is lost or engine is off

            output = ["OBD Data Logging:"]

            # Query for DTCs every 30 seconds
            if dtc_check_counter >= 30:
                dtc_response = connection.query(obd.commands.GET_DTC)
                if dtc_response.value:
                    dtc_codes = ', '.join([code for code, description in dtc_response.value])
                    output.append(f"DTC Codes: {dtc_codes}")
                else:
                    output.append("DTC Codes: None")
                dtc_check_counter = 0  # Reset counter after checking
            else:
                dtc_check_counter += 1

            # Query and log supported commands
            for command in supported_commands:
                command_output = log_command(command)
                output.append(command_output)
                time.sleep(.1)  # Short delay between commands

            # Write the collected data to file
            file.write('\n'.join(output) + '\n\n')
            file.flush()

            time.sleep(1)  # Delay for 1 second before the next cycle

    if connection and connection.is_connected():
        connection.close()
    print("Connection closed.")

else:
    print("Failed to connect to OBDII sensor.")