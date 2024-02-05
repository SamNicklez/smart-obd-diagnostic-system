import obd
import time
import os
import signal

# Global flag to control the loop
keep_running = True

# Ensure the logs directory exists
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "obd_data.txt")

# Signal handler function to gracefully exit
def signal_handler(sig, frame):
    global keep_running
    keep_running = False
    print("\nGraceful shutdown initiated...")

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Establishing connection
connection = obd.OBD('/dev/rfcomm0')

def convert_speed_to_mph(speed_km_per_hr):
    return speed_km_per_hr * 0.621371

def convert_celsius_to_fahrenheit(temp_celsius):
    return (temp_celsius * 9/5) + 32

if connection.is_connected():
    print(f"Connected to OBDII sensor. Logging data and DTCs to {log_file_path}")

    with open(log_file_path, 'w') as file:
        while keep_running:
            if not connection.is_connected():
                print("Lost connection to OBDII sensor.")
                break

            output = []

            # Query for DTC codes
            dtc_response = connection.query(obd.commands.GET_DTC)
            if dtc_response.value:  # Check if there are any DTC codes
                dtc_codes = ', '.join([code for code, description in dtc_response.value])
                output.append(f"DTC Codes: {dtc_codes}")
            else:
                output.append("DTC Codes: None")

            # Engine RPM (no conversion needed)
            rpm = connection.query(obd.commands.RPM)
            if not rpm.is_null():
                output.append(f"Engine RPM: {rpm.value.magnitude}")

            # Vehicle Speed (convert km/h to mph)
            speed = connection.query(obd.commands.SPEED)
            if not speed.is_null():
                speed_mph = convert_speed_to_mph(speed.value.magnitude)
                output.append(f"Speed: {speed_mph} mph")

            # Coolant Temperature (convert Celsius to Fahrenheit)
            coolant_temp = connection.query(obd.commands.COOLANT_TEMP)
            if not coolant_temp.is_null():
                coolant_temp_f = convert_celsius_to_fahrenheit(coolant_temp.value.magnitude)
                output.append(f"Coolant Temperature: {coolant_temp_f} °F")

            # Additional conversions for other metrics as necessary...
                
                # Throttle Position
            throttle_pos = connection.query(obd.commands.THROTTLE_POS)
            if not throttle_pos.is_null():
                output.append(f"Throttle Position: {throttle_pos.value.magnitude}%")

            # Fuel Level
            fuel_level = connection.query(obd.commands.FUEL_LEVEL)
            if not fuel_level.is_null():
                output.append(f"Fuel Level: {fuel_level.value.magnitude}%")

            # Battery Voltage
            battery_voltage = connection.query(obd.commands.ELM_VOLTAGE)
            if not battery_voltage.is_null():
                output.append(f"Battery Voltage: {battery_voltage.value.magnitude} V")

            # Intake Air Temperature
            intake_temp = connection.query(obd.commands.INTAKE_TEMP)
            if not intake_temp.is_null():
                intake_temp_f = convert_celsius_to_fahrenheit(intake_temp.value.magnitude)
                output.append(f"Intake Air Temperature: {intake_temp_f} °C")

            # Write the collected data to file
            file.write('\n'.join(output) + '\n\n')
            file.flush()

            time.sleep(1)  # Adjust as necessary

    if connection.is_connected():
        connection.close()
    print("Connection closed.")

else:
    print("Failed to connect to OBDII sensor.")
