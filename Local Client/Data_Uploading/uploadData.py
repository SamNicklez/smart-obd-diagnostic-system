import mysql.connector
import requests
from datetime import datetime
import socket

# Database connection configuration
db_config = {
    'user': 'sloecke',
    'password': 'password',
    'host': 'localhost',
    'database': 'obd'
}

# Flask server configuration
server_url = 'http://172.17.100.225:5000/upload'

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check if the Raspberry Pi is connected to the internet.
    
    Attempts to establish a socket connection with Google's DNS server.
    If successful, it implies an active internet connection.
    
    :param host: The host IP to connect to for checking the internet connection.
    :param port: The port number to use for the connection.
    :param timeout: Connection timeout in seconds.
    :return: True if the internet connection is available, False otherwise.
    """
    try:
        # Use the socket to attempt to connect to the host
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"No internet connection: {ex}")
        return False

def fetch_data_from_database():
    """
    Fetch data from the MySQL database.
    :return: A list of dictionaries with the data, where datetime objects are converted to strings.
    """
    data = []
    try:
        db_conn = mysql.connector.connect(**db_config)
        db_cursor = db_conn.cursor(dictionary=True)
        query = "SELECT * FROM VehicleData"  # Adjust the query as needed
        db_cursor.execute(query)

        for row in db_cursor:
            # Convert datetime objects to strings
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
            data.append(row)
        
        db_cursor.close()
        db_conn.close()
    except mysql.connector.Error as err:
        print(f"Failed to fetch data from database: {err}")
    
    return data


def send_data_to_server(data):
    """
    Send data to the Flask server via POST request.
    :param data: The data to send, as a list of dictionaries.
    """
    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Data sent successfully to the server.")
        else:
            print(f"Failed to send data to server: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to server: {e}")

def main():
    if check_internet_connection():
        data = fetch_data_from_database()
        if data:
            send_data_to_server(data)
        else:
            print("No data to send.")

if __name__ == "__main__":
    main()
