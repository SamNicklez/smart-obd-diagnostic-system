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


def get_token():
    try:
        response = requests.post(
            # url="https://senior-design-final-project.onrender.com/login",
            url="http://127.0.0.1:5000/login",
            json={"username": "username", "password": "password"},
            headers={"Content-Type": "application/json"}
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
    print(data)
    print(token)
    try:
        response = requests.post(
            # url="https://senior-design-final-project.onrender.com/stage",
            url="http://localhost/stage",
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


def format_data(data):
    return_data = []
    for row in data:
        formatted_row = {
            "timestamp": row['timestamp'],
            "airflow_rate": row['MAF'],
            "speed": row['SPEED'],
            "relative_throttle_pos": row['RELATIVE_THROTTLE_POS'],
            "distance_w_mil": row['DISTANCE_W_MIL'],
            "runtime": row['RUN_TIME'],
            "commanded_egr": row['COMMANDED_EGR'],
            "time_since_dtc_cleared": row['TIME_SINCE_DTC_CLEARED'],
            "runtime_mil": row['RUN_TIME_MIL'],
            "intake_pressure": row['INTAKE_PRESSURE'],
            "coolant_temp": row['COOLANT_TEMP'],
            "oil_temp": row['OIL_TEMP'],
            "barometric_pressure": row['BAROMETRIC_PRESSURE'],
            "rpm": row['RPM'],
            "pids_b": row['PIDS_B'],
            "intake_temp": row['INTAKE_TEMP'],
            "voltage": row['CONTROL_MODULE_VOLTAGE'],
            "absolute_load": row['ABSOLUTE_LOAD'],
            "engine_load": row['ENGINE_LOAD'],
            "dtc": row['GET_DTC'] if row['GET_DTC'] else "None",
            "current_dtc": row['GET_CURRENT_DTC'] if row['GET_CURRENT_DTC'] else "None",
            "latitude": "76.34",
            "longitude": "52.65"
        }
        return_data.append(formatted_row)
    return return_data


def upload_data():
    token = get_token()
    print(f"Token: {token}")
    data = fetch_data_from_database()
    data = format_data(data)
    print(f"Data: {data}")
    if data:
        send_data_to_server(data, token)
    else:
        print("No data to send.")


def main():
    upload_data()


if __name__ == "__main__":
    main()
