import socket
from datetime import datetime

import mysql.connector
import requests

# Database connection configuration
db_config = {
    'user': 'test',
    'password': 'password',
    'host': 'localhost',
    'port': '3307',
    'database': 'obd'
}


def test():
    try:
        response = requests.post(
            url="https://senior-design-final-project.onrender.com/"
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get token: {response.status_code}")
    except Exception as e:
        print(f"Error getting token: {e}")
    return None


def get_token():
    try:
        response = requests.post(
            url="https://senior-design-final-project.onrender.com/login",
            data={"username": "username", "password": "password"}
        )
        if response.status_code == 200:
            return response.json().get("token")
        else:
            print(f"Failed to get token: {response.status_code}")
    except Exception as e:
        print(f"Error getting token: {e}")
    return None


def fetch_data_from_database():
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


def send_data_to_server(data, token):
    try:
        response = requests.post(
            url="https://senior-design-final-project.onrender.com/postOBDData",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
        )
        if response.status_code == 200:
            print("Data sent successfully to the server.")
        else:
            print(f"Failed to send data to server: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to server: {e}")


def upload_data():
    t = test()
    print(f"Test: {t}")
    token = get_token()
    print(f"Token: {token}")
    data = fetch_data_from_database()
    print(f"Data: {data}")
    if data:
        send_data_to_server(data, token)
    else:
        print("No data to send.")


def main():
    upload_data()


if __name__ == "__main__":
    main()
