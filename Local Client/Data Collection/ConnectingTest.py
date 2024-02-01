import obd

# Need to find the address of the OBD II bluetooth and bind it to a serial port.
# Binding command: sudo rfcomm bind rfcomm0 00:1D:A5:05:A4:E3
# change the address as needed

# Establishing connection
connection = obd.OBD('/dev/rfcomm0')

if connection.is_connected():
    print("Connected to OBDII sensor.")

    # Example: Query the engine RPM
    rpm = connection.query(obd.commands.RPM)
    if not rpm.is_null():
        print(f"Engine RPM: {rpm.value}")

    # Vehicle Speed
    speed = connection.query(obd.commands.SPEED)
    if not speed.is_null():
        print(f"Speed: {speed.value}")

    connection.close()
else:
    print("Failed to connect to OBDII sensor.")