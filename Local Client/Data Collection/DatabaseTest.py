import mysql.connector



def insert_commands_with_units(commands):
    try:
        # Assuming db_conn is your database connection
        cursor = conn.cursor()
        
        # Adjusted to include units in the insert statement
        insert_query = "INSERT INTO Commands (CommandName, Description, Units) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, commands)
        
        conn.commit()
        print(f"{cursor.rowcount} commands were inserted.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection is closed.")


# Replace these with your connection details
config = {
    'user': 'sloecke',
    'password': 'password',
    'host': 'localhost',
    'port': 3306,  # Default MariaDB/MySQL port
}

commandsList = {
    ("PIDS_A", "Supported PIDs [01-20]", "BitArray"),
    ("STATUS", "Status since DTCs cleared", "Special"),
    ("FREEZE_DTC", "DTC that triggered the freeze frame", "Special"),
    ("FUEL_STATUS", "Fuel System Status", "String, String"),
    ("ENGINE_LOAD", "Calculated Engine Load", "%"),
    ("COOLANT_TEMP", "Engine Coolant Temperature", "Degrees F"),
    ("SHORT_FUEL_TRIM_1", "Short Term Fuel Trim - Bank 1", "%"),
    ("LONG_FUEL_TRIM_1", "Long Term Fuel Trim - Bank 1", "%"),
    ("SHORT_FUEL_TRIM_2", "Short Term Fuel Trim - Bank 2", "%"),
    ("LONG_FUEL_TRIM_2", "Long Term Fuel Trim - Bank 2", "%"),
    ("FUEL_PRESSURE", "Fuel Pressure", "kPa"),
    ("INTAKE_PRESSURE", "Intake Manifold Pressure", "kPa"),
    ("RPM", "Engine RPM", "RPM"),
    ("SPEED", "Vehicle Speed", "MPH"),
    ("TIMING_ADVANCE", "Timing Advance", "Degrees"),
    ("INTAKE_TEMP", "Intake Air Temp", "Degrees F"),
    ("MAF", "Air Flow Rate (MAF)", "g/s"),
    ("THROTTLE_POS", "Throttle Position", "%"),
    ("AIR_STATUS", "Secondary Air Status", "String"),
    ("O2_SENSORS", "O2 Sensors Present", "Special"),
    ("O2_B1S1", "O2: Bank 1 - Sensor 1 Voltage", "V"),
    ("O2_B1S2", "O2: Bank 1 - Sensor 2 Voltage", "V"),
    ("O2_B1S3", "O2: Bank 1 - Sensor 3 Voltage", "V"),
    ("O2_B1S4", "O2: Bank 1 - Sensor 4 Voltage", "V"),
    ("O2_B2S1", "O2: Bank 2 - Sensor 1 Voltage", "V"),
    ("O2_B2S2", "O2: Bank 2 - Sensor 2 Voltage", "V"),
    ("O2_B2S3", "O2: Bank 2 - Sensor 3 Voltage", "V"),
    ("O2_B2S4", "O2: Bank 2 - Sensor 4 Voltage", "V"),
    ("OBD_COMPLIANCE", "OBD Standards Compliance", "String"),
    ("O2_SENSORS_ALT", "O2 Sensors Present (alternate)", "Special"),
    ("AUX_INPUT_STATUS", "Auxiliary input status (power take off)", "Boolean"),
    ("RUN_TIME", "Engine Run Time", "Seconds"),
    ("PIDS_B", "Supported PIDs [21-40]", "BitArray"),
    ("DISTANCE_W_MIL", "Distance Traveled with MIL on", "m"),
    ("FUEL_RAIL_PRESSURE_VAC", "Fuel Rail Pressure (relative to vacuum)", "kPa"),
    ("FUEL_RAIL_PRESSURE_DIRECT", "Fuel Rail Pressure (direct inject)", "kPa"),
    ("O2_S1_WR_VOLTAGE", "02 Sensor 1 WR Lambda Voltage", "V"),
    ("O2_S2_WR_VOLTAGE", "02 Sensor 2 WR Lambda Voltage", "V"),
    ("O2_S3_WR_VOLTAGE", "02 Sensor 3 WR Lambda Voltage", "V"),
    ("O2_S4_WR_VOLTAGE", "02 Sensor 4 WR Lambda Voltage", "V"),
    ("O2_S5_WR_VOLTAGE", "02 Sensor 5 WR Lambda Voltage", "V"),
    ("O2_S6_WR_VOLTAGE", "02 Sensor 6 WR Lambda Voltage", "V"),
    ("O2_S7_WR_VOLTAGE", "02 Sensor 7 WR Lambda Voltage", "V"),
    ("O2_S8_WR_VOLTAGE", "02 Sensor 8 WR Lambda Voltage", "V"),
    ("COMMANDED_EGR", "Commanded EGR", "%"),
    ("EGR_ERROR", "EGR Error", "%"),
    ("EVAPORATIVE_PURGE", "Commanded Evaporative Purge", "%"),
    ("FUEL_LEVEL", "Fuel Level Input", "%"),
    ("WARMUPS_SINCE_DTC_CLEAR", "Number of warm-ups since codes cleared", "Times"),
    ("DISTANCE_SINCE_DTC_CLEAR", "Distance traveled since codes cleared", "m"),
    ("EVAP_VAPOR_PRESSURE", "Evaporative system vapor pressure", "Pa"),
    ("BAROMETRIC_PRESSURE", "Barometric Pressure", "kPa"),
    ("O2_S1_WR_CURRENT", "02 Sensor 1 WR Lambda Current", "mA"),
    ("O2_S2_WR_CURRENT", "02 Sensor 2 WR Lambda Current", "mA"),
    ("O2_S3_WR_CURRENT", "02 Sensor 3 WR Lambda Current", "mA"),
    ("O2_S4_WR_CURRENT", "02 Sensor 4 WR Lambda Current", "mA"),
    ("O2_S5_WR_CURRENT", "02 Sensor 5 WR Lambda Current", "mA"),
    ("O2_S6_WR_CURRENT", "02 Sensor 6 WR Lambda Current", "mA"),
    ("O2_S7_WR_CURRENT", "02 Sensor 7 WR Lambda Current", "mA"),
    ("O2_S8_WR_CURRENT", "02 Sensor 8 WR Lambda Current", "mA"),
    ("CATALYST_TEMP_B1S1", "Catalyst Temperature: Bank 1 - Sensor 1", "Degrees F"),
    ("CATALYST_TEMP_B2S1", "Catalyst Temperature: Bank 2 - Sensor 1", "Degrees F"),
    ("CATALYST_TEMP_B1S2", "Catalyst Temperature: Bank 1 - Sensor 2", "Degrees F"),
    ("CATALYST_TEMP_B2S2", "Catalyst Temperature: Bank 2 - Sensor 2", "Degrees F"),
    ("PIDS_C", "Supported PIDs [41-60]", "BitArray"),
    ("STATUS_DRIVE_CYCLE", "Monitor status this drive cycle", "Special"),
    ("CONTROL_MODULE_VOLTAGE", "Control module voltage", "V"),
    ("ABSOLUTE_LOAD", "Absolute load value", "%"),
    ("COMMANDED_EQUIV_RATIO", "Commanded equivalence ratio", "Ratio"),
    ("RELATIVE_THROTTLE_POS", "Relative throttle position", "%"),
    ("AMBIANT_AIR_TEMP", "Ambient air temperature", "Degrees F"),
    ("THROTTLE_POS_B", "Absolute throttle position B", "%"),
    ("THROTTLE_POS_C", "Absolute throttle position C", "%"),
    ("ACCELERATOR_POS_D", "Accelerator pedal position D", "%"),
    ("ACCELERATOR_POS_E", "Accelerator pedal position E", "%"),
    ("ACCELERATOR_POS_F", "Accelerator pedal position F", "%"),
    ("THROTTLE_ACTUATOR", "Commanded throttle actuator", "%"),
    ("RUN_TIME_MIL", "Time run with MIL on", "min"),
    ("TIME_SINCE_DTC_CLEARED", "Time since trouble codes cleared", "min"),
    ("MAX_MAF", "Maximum value for mass air flow sensor", "g/s"),
    ("FUEL_TYPE", "Fuel Type", "String"),
    ("ETHANOL_PERCENT", "Ethanol Fuel Percent", "%"),
    ("EVAP_VAPOR_PRESSURE_ABS", "Absolute Evap system Vapor Pressure", "kPa"),
    ("EVAP_VAPOR_PRESSURE_ALT", "Evap system vapor pressure", "Pa"),
    ("SHORT_O2_TRIM_B1", "Short term secondary O2 trim - Bank 1", "%"),
    ("LONG_O2_TRIM_B1", "Long term secondary O2 trim - Bank 1", "%"),
    ("SHORT_O2_TRIM_B2", "Short term secondary O2 trim - Bank 2", "%"),
    ("LONG_O2_TRIM_B2", "Long term secondary O2 trim - Bank 2", "%"),
    ("FUEL_RAIL_PRESSURE_ABS", "Fuel rail pressure (absolute)", "kPa"),
    ("RELATIVE_ACCEL_POS", "Relative accelerator pedal position", "%"),
    ("HYBRID_BATTERY_REMAINING", "Hybrid battery pack remaining life", "%"),
    ("OIL_TEMP", "Engine oil temperature", "Degrees F"),
    ("FUEL_INJECT_TIMING", "Fuel injection timing", "Degrees"),
    ("FUEL_RATE", "Engine fuel rate", "Liters/h")
}

try:
    # Establish a connection to MariaDB
    conn = mysql.connector.connect(**config)
    
    # Create a cursor object
    cursor = conn.cursor()
    
    insert_commands_with_units(commandsList)
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MariaDB connection is closed")