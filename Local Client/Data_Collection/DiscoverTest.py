import bluetooth

def discover_obdii_devices():
    print("Scanning for OBDII devices...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    obdii_devices = [device for device in nearby_devices if device[1] == "OBDII"]

    if obdii_devices:
        print("Found OBDII devices:")
        for addr, name in obdii_devices:
            print(f"  Address: {addr}, Name: {name}")
    else:
        print("No OBDII devices found.")

if __name__ == "__main__":
    discover_obdii_devices()
