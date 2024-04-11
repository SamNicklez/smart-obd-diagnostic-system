# Need to find the address of the OBD II bluetooth and bind it to a serial port.
# Binding command: sudo rfcomm bind rfcomm0 00:1D:A5:05:A4:E3

import os
import time
from datetime import datetime

import mysql.connector
import obd

from PrintInColor import printc


class DataCollector:
    def __init__(self, update_gui_callback=None):

        ############################################################################################################
        ## SET THESE TWO VARIABLES BEFORE RUNNING
        ## IF RUNNING IN CAR, USE THIS COMMAND FIRST: sudo rfcomm bind rfcomm0 00:1D:A5:05:A4:E3
        ############################################################################################################
        # Set this to true if running on the pi
        isPi = False
        # Set this to true if running in the actual car
        isCar = False

        # List for all the collected data that gets updated every read from the sensor
        self.data_dict = {}

        # Call back for the GUI to grab the current data
        self.update_gui_callback = update_gui_callback

        # List of filtered commands that is all the available commands that are also supported in the current car
        self.filtered_commands = set()

        # List of available commands from the Python-OBD Library
        self.available_commands = {
            "PIDS_A": {"command": "PIDS_A", "name": "PIDs A", "unit": ""},
            "STATUS": {"command": "STATUS", "name": "Status", "unit": ""},
            "FREEZE_DTC": {"command": "FREEZE_DTC", "name": "Freeze DTC", "unit": "TEST"},
            "FUEL_STATUS": {"command": "FUEL_STATUS", "name": "Fuel Status", "unit": ""},
            "ENGINE_LOAD": {"command": "ENGINE_LOAD", "name": "Engine Load", "unit": "%"},
            "COOLANT_TEMP": {"command": "COOLANT_TEMP", "name": "Coolant Temp", "unit": "°F"},
            "SHORT_FUEL_TRIM_1": {"command": "SHORT_FUEL_TRIM_1", "name": "Short Fuel Trim #1", "unit": "%"},
            "LONG_FUEL_TRIM_1": {"command": "LONG_FUEL_TRIM_1", "name": "Long Fuel Trim #1", "unit": "%"},
            "SHORT_FUEL_TRIM_2": {"command": "SHORT_FUEL_TRIM_2", "name": "Short Fuel Trim #2", "unit": "%"},
            "LONG_FUEL_TRIM_2": {"command": "LONG_FUEL_TRIM_2", "name": "Long Fuel Trim #2", "unit": "%"},
            "FUEL_PRESSURE": {"command": "FUEL_PRESSURE", "name": "Fuel Pressure", "unit": "kPa"},
            "INTAKE_PRESSURE": {"command": "INTAKE_PRESSURE", "name": "Intake Pressure", "unit": "kPa"},
            "RPM": {"command": "RPM", "name": "RPM", "unit": "RPM"},
            "SPEED": {"command": "SPEED", "name": "Speed", "unit": "MPH"},
            "TIMING_ADVANCE": {"command": "TIMING_ADVANCE", "name": "Timing Advance", "unit": "°"},
            "INTAKE_TEMP": {"command": "INTAKE_TEMP", "name": "Intake Temp", "unit": "°F"},
            "MAF": {"command": "MAF", "name": "MAF", "unit": "g/s"},
            "THROTTLE_POS": {"command": "THROTTLE_POS", "name": "Throttle Position", "unit": "%"},
            "AIR_STATUS": {"command": "AIR_STATUS", "name": "Air Status", "unit": ""},
            "O2_SENSORS": {"command": "O2_SENSORS", "name": "O2 Sensors Present", "unit": ""},
            "O2_B1S1": {"command": "O2_B1S1", "name": "O2 Bank #1 Sensor #1", "unit": "Volts"},
            "O2_B1S2": {"command": "O2_B1S2", "name": "O2 Bank #1 Sensor #2", "unit": "Volts"},
            "O2_B1S3": {"command": "O2_B1S3", "name": "O2 Bank #1 Sensor #3", "unit": "Volts"},
            "O2_B1S4": {"command": "O2_B1S4", "name": "O2 Bank #1 Sensor #4", "unit": "Volts"},
            "O2_B2S1": {"command": "O2_B2S1", "name": "O2 Bank #2 Sensor #1", "unit": "Volts"},
            "O2_B2S2": {"command": "O2_B2S2", "name": "O2 Bank #2 Sensor #2", "unit": "Volts"},
            "O2_B2S3": {"command": "O2_B2S3", "name": "O2 Bank #2 Sensor #3", "unit": "Volts"},
            "O2_B2S4": {"command": "O2_B2S4", "name": "O2 Bank #2 Sensor #4", "unit": "Volts"},
            "OBD_COMPLIANCE": {"command": "OBD_COMPLIANCE", "name": "OBD Compliance", "unit": ""},
            "O2_SENSORS_ALT": {"command": "O2_SENSORS_ALT", "name": "O2 Sensors Present (Alternate)", "unit": ""},
            "AUX_INPUT_STATUS": {"command": "AUX_INPUT_STATUS", "name": "Aux Input Status (Power Take Off)",
                                 "unit": ""},
            "RUN_TIME": {"command": "RUN_TIME", "name": "Run Time", "unit": "Seconds"},
            "PIDS_B": {"command": "PIDS_B", "name": "PIDs B", "unit": ""},
            "DISTANCE_W_MIL": {"command": "DISTANCE_W_MIL", "name": "Distance with MIL", "unit": "km"},
            "FUEL_RAIL_PRESSURE_VAC": {"command": "FUEL_RAIL_PRESSURE_VAC",
                                       "name": "Fuel Rail Pressure (relative to Vacuum)", "unit": "kPa"},
            "FUEL_RAIL_PRESSURE_DIRECT": {"command": "FUEL_RAIL_PRESSURE_DIRECT",
                                          "name": "Fuel Rail Pressure (direct inject)", "unit": "kPa"},
            "O2_S1_WR_VOLTAGE": {"command": "O2_S1_WR_VOLTAGE", "name": "02 Sensor 1 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S2_WR_VOLTAGE": {"command": "O2_S2_WR_VOLTAGE", "name": "02 Sensor 2 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S3_WR_VOLTAGE": {"command": "O2_S3_WR_VOLTAGE", "name": "02 Sensor 3 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S4_WR_VOLTAGE": {"command": "O2_S4_WR_VOLTAGE", "name": "02 Sensor 4 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S5_WR_VOLTAGE": {"command": "O2_S5_WR_VOLTAGE", "name": "02 Sensor 5 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S6_WR_VOLTAGE": {"command": "O2_S6_WR_VOLTAGE", "name": "02 Sensor 6 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S7_WR_VOLTAGE": {"command": "O2_S7_WR_VOLTAGE", "name": "02 Sensor 7 WR Lambda Voltage",
                                 "unit": "Volts"},
            "O2_S8_WR_VOLTAGE": {"command": "O2_S8_WR_VOLTAGE", "name": "02 Sensor 8 WR Lambda Voltage",
                                 "unit": "Volts"},
            "COMMANDED_EGR": {"command": "COMMANDED_EGR", "name": "Commanded EGR", "unit": "%"},
            "EGR_ERROR": {"command": "EGR_ERROR", "name": "EGR Error", "unit": "%"},
            "EVAPORATIVE_PURGE": {"command": "EVAPORATIVE_PURGE", "name": "Commanded Evaporative Purge", "unit": "%"},
            "FUEL_LEVEL": {"command": "FUEL_LEVEL", "name": "Fuel Level", "unit": "%"},
            "WARMUPS_SINCE_DTC_CLEAR": {"command": "WARMUPS_SINCE_DTC_CLEAR", "name": "Warmups since DTC Clear",
                                        "unit": "times"},
            "DISTANCE_SINCE_DTC_CLEAR": {"command": "DISTANCE_SINCE_DTC_CLEAR", "name": "Distance Since DTC Clear",
                                         "unit": "miles"},
            "EVAP_VAPOR_PRESSURE": {"command": "EVAP_VAPOR_PRESSURE", "name": "Evap Vapor Pressure", "unit": "Pa"},
            "BAROMETRIC_PRESSURE": {"command": "BAROMETRIC_PRESSURE", "name": "Barometric Pressure", "unit": "kPa"},
            "O2_S1_WR_CURRENT": {"command": "O2_S1_WR_CURRENT", "name": "02 Sensor 1 WR Lambda Current", "unit": "mA"},
            "O2_S2_WR_CURRENT": {"command": "O2_S2_WR_CURRENT", "name": "02 Sensor 2 WR Lambda Current", "unit": "mA"},
            "O2_S3_WR_CURRENT": {"command": "O2_S3_WR_CURRENT", "name": "02 Sensor 3 WR Lambda Current", "unit": "mA"},
            "O2_S4_WR_CURRENT": {"command": "O2_S4_WR_CURRENT", "name": "02 Sensor 4 WR Lambda Current", "unit": "mA"},
            "O2_S5_WR_CURRENT": {"command": "O2_S5_WR_CURRENT", "name": "02 Sensor 5 WR Lambda Current", "unit": "mA"},
            "O2_S6_WR_CURRENT": {"command": "O2_S6_WR_CURRENT", "name": "02 Sensor 6 WR Lambda Current", "unit": "mA"},
            "O2_S7_WR_CURRENT": {"command": "O2_S7_WR_CURRENT", "name": "02 Sensor 7 WR Lambda Current", "unit": "mA"},
            "O2_S8_WR_CURRENT": {"command": "O2_S8_WR_CURRENT", "name": "02 Sensor 8 WR Lambda Current", "unit": "mA"},
            "CATALYST_TEMP_B1S1": {"command": "CATALYST_TEMP_B1S1", "name": "Catalyst Temperature: Bank 1 - Sensor 1",
                                   "unit": "°F"},
            "CATALYST_TEMP_B2S1": {"command": "CATALYST_TEMP_B2S1", "name": "Catalyst Temperature: Bank 2 - Sensor 1",
                                   "unit": "°F"},
            "CATALYST_TEMP_B1S2": {"command": "CATALYST_TEMP_B1S2", "name": "Catalyst Temperature: Bank 1 - Sensor 2",
                                   "unit": "°F"},
            "CATALYST_TEMP_B2S2": {"command": "CATALYST_TEMP_B2S2", "name": "Catalyst Temperature: Bank 2 - Sensor 2",
                                   "unit": "°F"},
            "PIDS_C": {"command": "PIDS_C", "name": "PIDs C", "unit": ""},
            "STATUS_DRIVE_CYCLE": {"command": "STATUS_DRIVE_CYCLE", "name": "Status Drive Cycle", "unit": ""},
            "CONTROL_MODULE_VOLTAGE": {"command": "CONTROL_MODULE_VOLTAGE", "name": "Control Module Voltage",
                                       "unit": "Volts"},
            "ABSOLUTE_LOAD": {"command": "ABSOLUTE_LOAD", "name": "Absolute Load", "unit": "%"},
            "COMMANDED_EQUIV_RATIO": {"command": "COMMANDED_EQUIV_RATIO", "name": "Commanded Equiv Ratio", "unit": ""},
            "RELATIVE_THROTTLE_POS": {"command": "RELATIVE_THROTTLE_POS", "name": "Relative Throttle Position",
                                      "unit": "%"},
            "AMBIANT_AIR_TEMP": {"command": "AMBIANT_AIR_TEMP", "name": "Ambiant Air Temp", "unit": "°F"},
            "THROTTLE_POS_B": {"command": "THROTTLE_POS_B", "name": "Throttle Position B", "unit": "%"},
            "THROTTLE_POS_C": {"command": "THROTTLE_POS_C", "name": "Throttle Position C", "unit": "%"},
            "ACCELERATOR_POS_D": {"command": "ACCELERATOR_POS_D", "name": "Accelerator Position D", "unit": "%"},
            "ACCELERATOR_POS_E": {"command": "ACCELERATOR_POS_E", "name": "Accelerator Position E", "unit": "%"},
            "ACCELERATOR_POS_F": {"command": "ACCELERATOR_POS_F", "name": "Accelerator Position F", "unit": "%"},
            "THROTTLE_ACTUATOR": {"command": "THROTTLE_ACTUATOR", "name": "Commanded Throttle Actuator", "unit": "%"},
            "RUN_TIME_MIL": {"command": "RUN_TIME_MIL", "name": "Time run with MIL on", "unit": "Minutes"},
            "TIME_SINCE_DTC_CLEARED": {"command": "TIME_SINCE_DTC_CLEARED", "name": "Time Since DTC Cleared",
                                       "unit": "Minutes"},
            "MAX_MAF": {"command": "MAX_MAF", "name": "Max MAF", "unit": "g/s"},
            "FUEL_TYPE": {"command": "FUEL_TYPE", "name": "Fuel Type", "unit": ""},
            "ETHANOL_PERCENT": {"command": "ETHANOL_PERCENT", "name": "Ethanol Fuel Percent", "unit": "%"},
            "EVAP_VAPOR_PRESSURE_ABS": {"command": "EVAP_VAPOR_PRESSURE_ABS", "name": "Absolute Evap Vapor Pressure",
                                        "unit": "kPa"},
            "EVAP_VAPOR_PRESSURE_ALT": {"command": "EVAP_VAPOR_PRESSURE_ALT", "name": "Evap Vapor Pressure Alt",
                                        "unit": "Pa"},
            "SHORT_O2_TRIM_B1": {"command": "SHORT_O2_TRIM_B1", "name": "Short term secondary O2 trim - Bank 1",
                                 "unit": "%"},
            "LONG_O2_TRIM_B1": {"command": "LONG_O2_TRIM_B1", "name": "Long term secondary O2 trim - Bank 1",
                                "unit": "%"},
            "SHORT_O2_TRIM_B2": {"command": "SHORT_O2_TRIM_B2", "name": "Short term secondary O2 trim - Bank 2",
                                 "unit": "%"},
            "LONG_O2_TRIM_B2": {"command": "LONG_O2_TRIM_B2", "name": "Long term secondary O2 trim - Bank 2",
                                "unit": "%"},
            "FUEL_RAIL_PRESSURE_ABS": {"command": "FUEL_RAIL_PRESSURE_ABS", "name": "Fuel Rail Pressure Absolute",
                                       "unit": "kPa"},
            "RELATIVE_ACCEL_POS": {"command": "RELATIVE_ACCEL_POS", "name": "Relative Acceleration Position",
                                   "unit": "%"},
            "HYBRID_BATTERY_REMAINING": {"command": "HYBRID_BATTERY_REMAINING", "name": "Hybrid Battery Remaining",
                                         "unit": "%"},
            "OIL_TEMP": {"command": "OIL_TEMP", "name": "Oil Temp", "unit": "°F"},
            "FUEL_INJECT_TIMING": {"command": "FUEL_INJECT_TIMING", "name": "Fuel Inject Timing", "unit": "°"},
            "FUEL_RATE": {"command": "FUEL_RATE", "name": "Fuel Rate", "unit": "liters/h"},
            "VIN": {"command": "VIN", "name": "VIN", "unit": ""},
            "GET_DTC": {"command": "GET_DTC", "name": "Get DTC", "unit": ""},
            "GET_CURRENT_DTC": {"command": "GET_CURRENT_DTC", "name": "Get Current DTC", "unit": ""},
            "ELM_VOLTAGE": {"command": "ELM_VOLTAGE", "name": "ELM Voltage", "unit": "Volts"}
        }

        pi_user = 'test'

        # Setting the database settings based on which computer we are running on
        if isPi or isCar:
            db_config = {
                'user': 'test',
                'password': 'password',
                'host': 'localhost',
                'database': 'obd'
            }
        else:
            # Database connection configuration
            db_config = {
                'user': 'root',
                'password': 'password',
                'host': 'localhost',
                'database': 'obd',
                'port': '3307'
            }

        # Connect to the database
        try:
            self.db_conn = mysql.connector.connect(**db_config)
            self.db_cursor = self.db_conn.cursor()
            printc("DATABASE: Database connection established.")
        except mysql.connector.Error as err:
            printc(f"DATABASE: Failed to connect to database: {err}")
            db_conn = None

        # Global flag to control the loop
        self.keep_running = True

        # Get the directory of the currently running script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the logs directory inside Data_Collection
        logs_dir = os.path.join(script_directory, 'logs')

        # Ensure the logs directory exists and if not, make it
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Creating a file name with date and time
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file_name = f"obd_data_{current_time}.txt"
        self.log_file_path = os.path.join(logs_dir, log_file_name)

        # Setting the port to select the emulator on pi, computer or the actual car
        if isPi:
            self.portSelection = '/dev/pts/0'  # For running on windows
        elif isCar:
            self.portSelection = '/dev/rfcomm0'
        else:
            self.portSelection = 'COM8'

    # Method for running the collection from the sensor or emulator
    def start_collection(self):
        # Establishing connection
        connection = self.wait_for_obd_connection()

        # Loop for logging the data
        if connection and connection.is_connected():
            printc(f"SENSOR: Connected to OBDII sensor. Logging data to {self.log_file_path}")

            # Opening the file to write to for logs
            with open(self.log_file_path, 'w') as file:

                # Setting the supported commands by grabbing it from the current car
                self.supported_commands = set(connection.supported_commands)  # Assuming connection is an OBD object
                self.filter_supported_commands()  # Calling the filtering method to set the filtered_commands variable

                # Loop to collect data
                while self.keep_running:
                    if not connection.is_connected():  # or not check_engine_on(): Use this with the real car to stop collection when it shuts off
                        printc("SENSOR: Lost connection to OBDII sensor or engine turned off. Exiting...")
                        break  # Exit the loop if connection is lost or engine is off

                    output = ["OBD Data Logging:"]

                    # Grab the current time for keeping in at 1 second per loop
                    start_time = time.time()

                    # Looping through the supported command
                    for command in self.supported_commands:
                        if command.name in self.available_commands:
                            # Call the method to query the sensor 
                            command_output = self.log_command(command, connection)
                            output.append(command_output)  # add it to the output
                            time.sleep(.001)  # Short delay between commands   

                    # Passing the data dictionary to the GUI if it calls for it
                    if self.update_gui_callback:
                        self.update_gui_callback(self.data_dict)

                    # Call the method to insert the collected data into the database
                    self.insert_data_into_database()

                    # Write the collected data to file
                    file.write('\n'.join(output) + '\n\n')
                    file.flush()

                    # Delay for a second minus the time it took to query
                    delay_time = 1 - (time.time() - start_time)
                    if delay_time > 0:
                        time.sleep(delay_time)  # Delay before the next cycle

            if connection and connection.is_connected():
                connection.close()
            printc("SENSOR: Connection closed.")

        else:
            printc("SENSOR: Failed to connect to OBDII sensor.")

    # Clean up function for ending collection        
    def stop_collection(self, signum=None, frame=None):
        # Set the flag to end the loop
        self.keep_running = False

        # Close the database connection
        if self.db_conn is not None and self.db_conn.is_connected():
            self.db_cursor.close()
            self.db_conn.close()
            printc("DATABASE: Database connection closed.")
        print("Exiting...")

        # Function to wait for OBD connection

    def wait_for_obd_connection(self):
        connection = None
        while self.keep_running and connection is None:  # Keep trying to connect
            try:
                printc("SENSOR: Attempting to connect to OBD-II sensor...")
                connection = obd.OBD(self.portSelection, baudrate=115200)
                if not connection.is_connected():
                    printc("SENSOR: Unable to connect, retrying...")
                    connection.close()
                    connection = None
                    time.sleep(5)  # Wait for 5 seconds before retrying
            except InterruptedError:
                printc("SENSOR: Connection attempt interrupted. Exiting...")
                break  # Exit the loop if interrupted
            except Exception as e:
                printc(f"SENSOR: Error establishing connection: {e}")
                time.sleep(5)  # Wait for 5 seconds before retrying
        return connection

    # Method for inserting the data_dict values into the database
    def insert_data_into_database(self):
        """
        Insert data into the database without explicitly handling the timestamp.
        :param data_dict: A dictionary with command names as keys and their values.
        """
        if self.db_conn is not None and self.db_conn.is_connected():
            # Extract only the value part from each entry for insertion
            values = [val_dict['value'] for val_dict in self.data_dict.values()]

            # Make the SQL Queries
            columns = ', '.join([f"`{key}`" for key in self.data_dict.keys()])
            placeholders = ', '.join(['%s'] * len(self.data_dict))
            query = f"INSERT INTO VehicleData ({columns}) VALUES ({placeholders})"
            # values = list(self.data_dict.values())

            try:
                self.db_cursor.execute(query, values)  # Execute the queries
                self.db_conn.commit()
                printc("DATABASE: Data inserted successfully.")
            except mysql.connector.Error as err:
                printc(f"DATABASE: Failed to insert data into database: {err}")

                # Function to log a single command

    def log_command(self, command, connection):
        response = connection.query(command)  # Query the sensor

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # make a timestamp for the logs

        if not response.is_null():
            # Handle responses that are lists
            if isinstance(response.value, list):
                # Join list elements into a string or handle them as needed
                value = ', '.join(str(v) for v in response.value)
                unit = ""  # List responses might not have a unified unit
            else:
                value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value
                unit = str(response.value.units) if hasattr(response.value, 'units') else ""

            unit = self.available_commands[command.name]['unit']

            # Editing the units to be better
            if command.name == 'SPEED':
                if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                    value = convert_speed_to_mph(response.value.magnitude)
            elif unit == "°F":
                if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                    value = convert_celsius_to_fahrenheit(response.value.magnitude)
            elif unit == "miles":
                if hasattr(response.value, 'magnitude'):  # Ensure value has magnitude for conversion
                    value = convert_km_to_m(response.value.magnitude)
            # Here's the key change: Ensure value is converted to a basic data type
            if hasattr(response.value, 'magnitude') and hasattr(response.value, 'units'):
                # Convert to float if it has magnitude; it's likely a numeric value
                processed_value = float(value)
            else:
                # Fallback: Convert directly to string
                processed_value = str(response.value)

            # Store the processed value instead of the raw response
            self.data_dict[command.name] = {'value': processed_value, 'unit': unit}

            return f"{timestamp} - {command.name}: {value} {unit}"
        else:
            return f"{timestamp} - {command.name}: Not Supported or No Data"

    # Method for filtering the commands to find the available ones that are available in this current car
    def filter_supported_commands(self):
        # Assuming command_names is a set containing the names of supported commands
        command_names = {cmd.name for cmd in self.supported_commands}

        # New structure for filtered_commands to also include command and descriptive name
        self.filtered_commands = {cmd_key: self.available_commands[cmd_key] for cmd_key in self.available_commands if
                                  self.available_commands[cmd_key]["command"] in command_names}

        return self.filtered_commands

    def find_unit_by_command(self, available_commands, name_to_find):
        for cmd_key, cmd_details in available_commands.items():
            if cmd_details["name"] == name_to_find:
                return cmd_details["command"]
        return None  # Return None if no matching name is found


# Other functions that do not need to be in the class

# Functions for unit conversion
def convert_speed_to_mph(speed_km_per_hr):
    return round(speed_km_per_hr * 0.621371)


# Convert Celsius to Fahrenheit
def convert_celsius_to_fahrenheit(temp_celsius):
    return (temp_celsius * 9 / 5) + 32


# Convert Kilometers to Miles
def convert_km_to_m(km_value):
    return km_value * 0.621371
