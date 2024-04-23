import io

import pynmea2
import serial


class GPS:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    def get_gps_data(self):
        while True:
            line = self.sio.readline()
            msg = pynmea2.parse(line)

            if type(msg) == pynmea2.types.talker.RMC:
                if msg.lat and msg.lon:
                    return msg.lat, msg.lon
                else:
                    return None, None


def main():
    gps = GPS()
    while True:
        lat, lon = gps.get_gps_data()
        if lat and lon:
            print("Lat: " + lat + "\nLon: " + lon)
        else:
            print("Lat: None\nLon: None")


if __name__ == "__main__":
    main()
