import obd

# Need to find the address of the OBD II bluetooth and bind it to a serial port.
# Binding command: sudo rfcomm bind rfcomm0 00:1D:A5:05:A4:E3
# change the address as needed

# Establishing connection
connection = obd.OBD('/dev/rfcomm0')

if connection.is_connected():
    print("Connected to OBDII sensor.")

    # Engine RPM
    rpm = connection.query(obd.commands.RPM)
    if not rpm.is_null():
        print(f"Engine RPM: {rpm.value.magnitude}")  # .magnitude for numeric value

    # Vehicle Speed
    speed = connection.query(obd.commands.SPEED)
    if not speed.is_null():
        print(f"Speed: {speed.value.magnitude} km/h")

    # Coolant Temperature
    coolant_temp = connection.query(obd.commands.COOLANT_TEMP)
    if not coolant_temp.is_null():
        print(f"Coolant Temperature: {coolant_temp.value.magnitude} °C")

    # Throttle Position
    throttle_pos = connection.query(obd.commands.THROTTLE_POS)
    if not throttle_pos.is_null():
        print(f"Throttle Position: {throttle_pos.value.magnitude}%")

    # Fuel Level
    fuel_level = connection.query(obd.commands.FUEL_LEVEL)
    if not fuel_level.is_null():
        print(f"Fuel Level: {fuel_level.value.magnitude}%")

    # Battery Voltage
    battery_voltage = connection.query(obd.commands.ELM_VOLTAGE)
    if not battery_voltage.is_null():
        print(f"Battery Voltage: {battery_voltage.value.magnitude} V")

    # Intake Air Temperature
    intake_temp = connection.query(obd.commands.INTAKE_TEMP)
    if not intake_temp.is_null():
        print(f"Intake Air Temperature: {intake_temp.value.magnitude} °C")

    # Close connection
    connection.close()
else:
    print("Failed to connect to OBDII sensor.")
