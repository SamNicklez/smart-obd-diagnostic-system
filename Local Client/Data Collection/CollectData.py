# Need to find the address of the OBD II bluetooth and bind it to a serial port.
# Binding command: sudo rfcomm bind rfcomm0 00:1D:A5:05:A4:E3

import mysql.connector
import obd
import time
import os
import signal
from datetime import datetime

data_dict = {}

available_commands = {"PIDS_A",
    "STATUS",
    "FREEZE_DTC",
    "FUEL_STATUS",
    "ENGINE_LOAD",
    "COOLANT_TEMP",
    "SHORT_FUEL_TRIM_1",
    "LONG_FUEL_TRIM_1",
    "SHORT_FUEL_TRIM_2",
    "LONG_FUEL_TRIM_2",
    "FUEL_PRESSURE",
    "INTAKE_PRESSURE",
    "RPM",
    "SPEED",
    "TIMING_ADVANCE",
    "INTAKE_TEMP",
    "MAF",
    "THROTTLE_POS",
    "AIR_STATUS",
    "O2_SENSORS",
    "O2_B1S1",
    "O2_B1S2",
    "O2_B1S3",
    "O2_B1S4",
    "O2_B2S1",
    "O2_B2S2",
    "O2_B2S3",
    "O2_B2S4",
    "OBD_COMPLIANCE",
    "O2_SENSORS_ALT",
    "AUX_INPUT_STATUS",
    "RUN_TIME",
    "PIDS_B",
    "DISTANCE_W_MIL",
    "FUEL_RAIL_PRESSURE_VAC",
    "FUEL_RAIL_PRESSURE_DIRECT",
    "O2_S1_WR_VOLTAGE",
    "O2_S2_WR_VOLTAGE",
    "O2_S3_WR_VOLTAGE",
    "O2_S4_WR_VOLTAGE",
    "O2_S5_WR_VOLTAGE",
    "O2_S6_WR_VOLTAGE",
    "O2_S7_WR_VOLTAGE",
    "O2_S8_WR_VOLTAGE",
    "COMMANDED_EGR",
    "EGR_ERROR",
    "EVAPORATIVE_PURGE",
    "FUEL_LEVEL",
    "WARMUPS_SINCE_DTC_CLEAR",
    "DISTANCE_SINCE_DTC_CLEAR",
    "EVAP_VAPOR_PRESSURE",
    "BAROMETRIC_PRESSURE",
    "O2_S1_WR_CURRENT",
    "O2_S2_WR_CURRENT",
    "O2_S3_WR_CURRENT",
    "O2_S4_WR_CURRENT",
    "O2_S5_WR_CURRENT",
    "O2_S6_WR_CURRENT",
    "O2_S7_WR_CURRENT",
    "O2_S8_WR_CURRENT",
    "CATALYST_TEMP_B1S1",
    "CATALYST_TEMP_B2S1",
    "CATALYST_TEMP_B1S2",
    "CATALYST_TEMP_B2S2",
    "PIDS_C",
    "STATUS_DRIVE_CYCLE",
    "CONTROL_MODULE_VOLTAGE",
    "ABSOLUTE_LOAD",
    "COMMANDED_EQUIV_RATIO",
    "RELATIVE_THROTTLE_POS",
    "AMBIANT_AIR_TEMP",
    "THROTTLE_POS_B",
    "THROTTLE_POS_C",
    "ACCELERATOR_POS_D",
    "ACCELERATOR_POS_E",
    "ACCELERATOR_POS_F",
    "THROTTLE_ACTUATOR",
    "RUN_TIME_MIL",
    "TIME_SINCE_DTC_CLEARED",
    "MAX_MAF",
    "FUEL_TYPE",
    "ETHANOL_PERCENT",
    "EVAP_VAPOR_PRESSURE_ABS",
    "EVAP_VAPOR_PRESSURE_ALT",
    "SHORT_O2_TRIM_B1",
    "LONG_O2_TRIM_B1",
    "SHORT_O2_TRIM_B2",
    "LONG_O2_TRIM_B2",
    "FUEL_RAIL_PRESSURE_ABS",
    "RELATIVE_ACCEL_POS",
    "HYBRID_BATTERY_REMAINING",
    "OIL_TEMP",
    "FUEL_INJECT_TIMING",
    "FUEL_RATE",
    "VIN",
    "GET_DTC",
    "GET_CURRENT_DTC",
    "ELM_VOLTAGE"
    }


# Database connection configuration
db_config = {
    'user': 'sloecke',
    'password': 'password',
    'host': 'localhost',
    'database': 'obd'
}

try:
    db_conn = mysql.connector.connect(**db_config)
    db_cursor = db_conn.cursor()
    print("Database connection established.")
except mysql.connector.Error as err:
    print(f"Failed to connect to database: {err}")
    db_conn = None


def cleanup():
    global keep_running
    keep_running = False
    if db_conn is not None and db_conn.is_connected():
        db_cursor.close()
        db_conn.close()
        print("Database connection closed.")
    print("\nExiting...")


# Global flag to control the loop
keep_running = True

# Ensure the logs directory exists and if not, make it
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Creating a file name with date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name = f"obd_data_{current_time}.txt"
log_file_path = os.path.join(logs_dir, log_file_name)

# Signal handler function to gracefully exit
def signal_handler(sig, frame):
    global keep_running
    keep_running = False
    print("\nExiting...")
    cleanup()

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

#portSelection = '/dev/rfcomm0'
portSelection = 'COM8'

# Function to wait for OBD connection
def wait_for_obd_connection(port=portSelection):
    connection = None
    while keep_running and connection is None:
        try:
            print("Attempting to connect to OBD-II sensor...")
            connection = obd.OBD(port, baudrate=115200)
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

# Convert Celsius to Fahrenheit
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

        if command.name == 'GET_DTC' and hasattr(response.value, 'magnitude'):
            # Set some alert for alerting the driver to a new code
            print("Code detected")    

        #data_dict[command.name] = response.value

        # Editing the units to be better
        if command.name == 'SPEED':
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_speed_to_mph(response.value.magnitude)
                unit = "MPH"
        elif unit == "degree_Celsius":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_celsius_to_fahrenheit(response.value.magnitude)
                unit = "Degrees F"        
        elif unit == "degree_Celsius [PASSED]":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_celsius_to_fahrenheit(response.value.magnitude)
                unit = "Degrees F [PASSED]"
        elif unit == "degree_Celsius [FAILED]":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                value = convert_celsius_to_fahrenheit(response.value.magnitude)
                unit = "Degrees F [FAILED]"
        elif unit == "percent":
            if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                unit = "%" 


         # Here's the key change: Ensure value is converted to a basic data type
        if hasattr(response.value, 'magnitude') and hasattr(response.value, 'units'):
            # Convert to float if it has magnitude; it's likely a numeric value
            processed_value = float(value)
        else:
            # Fallback: Convert directly to string
            processed_value = str(response.value)

        # Store the processed value instead of the raw response
        data_dict[command.name] = processed_value 

        return f"{timestamp} - {command.name}: {value} {unit}"
    else:
        return f"{timestamp} - {command.name}: Not Supported or No Data"
    

def insert_data_into_database(data_dict):
    """
    Insert data into the database without explicitly handling the timestamp.
    :param data_dict: A dictionary with command names as keys and their values.
    """
    if db_conn is not None and db_conn.is_connected():
        # Prepare the SQL query dynamically based on the data_dict keys.
        columns = ', '.join([f"`{key}`" for key in data_dict.keys()])
        placeholders = ', '.join(['%s'] * len(data_dict))
        query = f"INSERT INTO VehicleData ({columns}) VALUES ({placeholders})"
        values = list(data_dict.values())

        try:
            db_cursor.execute(query, values)
            db_conn.commit()
            print("Data inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to insert data into database: {err}")   

# Loop for logging the data
if connection and connection.is_connected():
    print(f"Connected to OBDII sensor. Logging data to {log_file_path}")

    with open(log_file_path, 'w') as file:
        dtc_check_counter = 0  # Counter to determine when to check DTCs
        
        supported_commands = connection.supported_commands # commands that the car supports

        while keep_running:
            if not connection.is_connected(): #or not check_engine_on():
                print("Lost connection to OBDII sensor or engine turned off. Exiting...")
                break  # Exit the loop if connection is lost or engine is off

            output = ["OBD Data Logging:"]

            # Grab the current time for keeping in at 1 second per loop
            start_time = time.time()

            # Query and log supported commands
            for command in supported_commands:
                if command.name in available_commands:   
                    command_output = log_command(command)
                    output.append(command_output)
                    time.sleep(.001)  # Short delay between commands
                # elif command.name not in available_commands and not command.name.startswith("DTC_"):
                #     print("Whoops! Command not supported: " + command.name)    

            insert_data_into_database(data_dict)

            # Write the collected data to file
            file.write('\n'.join(output) + '\n\n')
            file.flush()

            # Delay for a second minus the time it took to query
            delay_time = 1 - (time.time() - start_time)
            
            if delay_time > 0:
                time.sleep(delay_time)  # Delay for 1 second before the next cycle

    if connection and connection.is_connected():
        connection.close()
    print("Connection closed.")

else:
    print("Failed to connect to OBDII sensor.")