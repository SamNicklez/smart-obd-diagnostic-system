import random
from datetime import datetime

import mysql.connector
import requests
from PrintInColor import printc

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


def fetch_and_delete_data_from_database():
    data = []
    try:
        db_conn = mysql.connector.connect(**db_config)
        db_cursor = db_conn.cursor(dictionary=True)
        db_conn.start_transaction()

        select_query = "SELECT * FROM VehicleData"
        db_cursor.execute(select_query)
        for row in db_cursor:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
            data.append(row)

        delete_query = "DELETE FROM VehicleData"
        db_cursor.execute(delete_query)

        db_conn.commit()

        db_cursor.close()
        db_conn.close()
    except mysql.connector.Error as err:
        print(f"Failed to fetch data from database: {err}")

    return data


def send_data_to_server(data, token):
    try:
        response = requests.post(
            # url="https://senior-design-final-project.onrender.com/stage",
            url="http://127.0.0.1:5000/stage",
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


def send_dtc_data_to_server(data, token):
    try:
        response = requests.post(
            # url="https://senior-design-final-project.onrender.com/stage",
            url="http://127.0.0.1:5000/postDTCData",
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
    dtc_data = []
    list_of_end_points = [("41.683430", "-91.562100"), ("41.703860", "-91.619360"),
                          ("41.646198", "-91.551003"), ("41.665890", "-91.471680"),
                          ("41.725360", "-91.519960"), ("41.698840", "-91.565990"),
                          ("41.697731", "-91.525510"), ("41.721920", "-91.525510"),
                          ("41.663880", "-91.530370"), ("41.659290", "-91.505840"),
                          ("41.651409", "-91.500900"), ("41.646969", "-91.532738")]
    random_end_point = random.choice(list_of_end_points)
    for i, row in enumerate(data):
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
            "latitude": "41.658200" if i != len(data) - 1 else random_end_point[0],
            "longitude": "-91.533460" if i != len(data) - 1 else random_end_point[1],
        }
        return_data.append(formatted_row)
        if row['GET_DTC'] and (row['GET_DTC'] not in [dtc_data[i]['code'] for i in range(len(dtc_data))]):
            formatted_row = {
                "date": row['timestamp'],
                "code": row['GET_DTC']
            }
            dtc_data.append(formatted_row)
    return return_data, dtc_data


def upload_data():
    token = get_token()
    print(f"Token: {token}")
    data = fetch_and_delete_data_from_database()
    by_sec_data, dtc_data = format_data(data)
    printc(f"By Sec Data: {by_sec_data}")
    if dtc_data:
        printc(f"DTC Data: {dtc_data}")
        send_dtc_data_to_server(dtc_data, token)
    if data:
        send_data_to_server(data, token)
    else:
        print("No data to send.")


def main():
    upload_data()


if __name__ == "__main__":
    main()
