from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
from Test_data import generate_car_info_json
from __init__ import token_auth
import Helpers
import os
import json
import jwt

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Test Flask API!"

@app.route("/verify", methods=["GET"])
@token_auth.login_required
def verify():
    try:
        return jsonify({"Good": "User verified successfully"}), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        response = supabase.table('Users').select("*").eq('username', data['username']).eq('password', data['password']).execute()
        if(response.data == []):
            return jsonify({"Error": "Invalid username or password"}), 401
        else:
            encoded_token = jwt.encode({"id": 1}, "secret", algorithm="HS256")
            return jsonify({"token": encoded_token}), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/grabcardetails", methods=["GET"])
@token_auth.login_required
def grab_car_details():
    try:
        response = supabase.table('Cars').select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/postcardetails", methods=["POST"])
@token_auth.login_required
def post_car_details():
    try:
        data = request.get_json()
        response = supabase.table('Cars').insert(data).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500

@app.route("/grabOBDData", methods=["GET"])
@token_auth.login_required
def grab_obd_data():
    try:
        response = supabase.table('OBDData').select("*").execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/postOBDData", methods=["POST"])
@token_auth.login_required
def post_obd_data():
    try:
        data = request.get_json()
        response = supabase.table('OBD').insert(data).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/grabNotifications", methods=["GET"])
@token_auth.login_required
def grab_notifications():
    try:
        response, _ = supabase.table('OBD').select("*").eq('dismissed', False).execute()
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Interal Server Error"}), 500

@app.route('/dismissNotification', methods=["POST"])
@token_auth.login_required
def dismiss_notification():
    try:
        data = request.get_json()
        response = supabase.table('OBD').update({"dismissed": True}).eq('obd_id', data['obd_id']).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/stage", methods=["POST"])
@token_auth.login_required
def stage():
    try:
        car_info = request.get_json()
        grouped_data = Helpers.group_by_day(car_info)
        # process data into generalized day data
        for day, records in grouped_data.items():
            temp = supabase.table('DrivingData').select('*').eq('timestamp', day).execute()
            try:
                response = temp.data[0]['driving_id']
            except:
                response = 0
            # If new entry
            if(response == 0):
                average_speed = Helpers.kph_to_mph(sum(record['speed'] for record in records) / len(records))
                total_runtime = max(record['runtime'] for record in records)
                average_coolant_temp = Helpers.celsius_to_fahrenheit(sum(record['coolant_temp'] for record in records) / len(records))
                average_oil_temp = Helpers.celsius_to_fahrenheit(sum(record['oil_temp'] for record in records) / len(records))
                avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) / len(records), 2)
                supabase.table('DrivingData').insert({"num_entries": len(records), "timestamp": day, "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            # If entry already exists
            else:
                data, _ = supabase.table('DrivingData').select("*").eq('timestamp', day).execute()
                average_speed = Helpers.kph_to_mph((sum(record['speed'] for record in records) + data['avg_speed'])/ (len(records) + data['num_entries']))
                total_runtime = max(record['runtime'] for record in records) + data['rumtime']
                average_coolant_temp = Helpers.celsius_to_fahrenheit((sum(record['coolant_temp'] for record in records) + data['avg_coolant_temp']) / (len(records) + data['num_entries']))
                average_oil_temp = Helpers.celsius_to_fahrenheit((sum(record['oil_temp'] for record in records) + data['avg_oil_temp']) / (len(records) + data['num_entries']))
                avg_mpg = round((sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) + data['avg_mpg']) / (len(records) + data['num_entries']), 2)
                supabase.table('DrivingData').update({"num_entries": (len(records) + data['num_entries']), "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).eq('driving_id', data['driving_id']).execute()
            car_info = Helpers.divide_into_trips(car_info)
            for trip in car_info:
                runtime = trip[-1]['runtime']
                start_time = trip[0]['timestamp']
                end_time = trip[-1]['timestamp']
                start_lat = trip[0]['lattitude']
                start_lon = trip[0]['longitude']
                end_lat = trip[-1]['lattitude']
                end_lon = trip[-1]['longitude']
                avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in trip) / len(trip), 2)
                avg_engine_load = round(sum(record['engine_load'] for record in trip) / len(trip), 2)
                response = supabase.table('DrivingData').select('driving_id').eq('timestamp', Helpers.convert_date(day)).execute()
                try:
                    driving_id = response.data[0]['driving_id']
                except:
                    driving_id = 0
                if driving_id == 0 or driving_id == None:
                    return jsonify({"Error": "Driving ID not found within the Trips"}), 500
                supabase.table('Trips').insert({"driving_id": driving_id, "runtime": runtime, "start_time": start_time, "end_time": end_time, "start_lat": start_lat, "start_lon": start_lon, "end_lat": end_lat, "end_lon": end_lon, "avg_mpg": avg_mpg, "avg_engine_load": avg_engine_load}).execute()

        return jsonify({"Test": "GOOD"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/test", methods=["GET"])
def test():
    try:
        car_info = json.loads(generate_car_info_json())
        grouped_data = Helpers.group_by_day(car_info)
        # process data into generalized day data
        for day, records in grouped_data.items():
            temp = supabase.table('DrivingData').select('*').eq('timestamp', day).execute()
            try:
                response = temp.data[0]['driving_id']
            except:
                response = 0
            # If new entry
            if(response == 0):
                average_speed = Helpers.kph_to_mph(sum(record['speed'] for record in records) / len(records))
                total_runtime = max(record['runtime'] for record in records)
                average_coolant_temp = Helpers.celsius_to_fahrenheit(sum(record['coolant_temp'] for record in records) / len(records))
                average_oil_temp = Helpers.celsius_to_fahrenheit(sum(record['oil_temp'] for record in records) / len(records))
                avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) / len(records), 2)
                supabase.table('DrivingData').insert({"num_entries": len(records), "timestamp": day, "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            # If entry already exists
            else:
                data, _ = supabase.table('DrivingData').select("*").eq('timestamp', day).execute()
                average_speed = Helpers.kph_to_mph((sum(record['speed'] for record in records) + data['avg_speed'])/ (len(records) + data['num_entries']))
                total_runtime = max(record['runtime'] for record in records) + data['rumtime']
                average_coolant_temp = Helpers.celsius_to_fahrenheit((sum(record['coolant_temp'] for record in records) + data['avg_coolant_temp']) / (len(records) + data['num_entries']))
                average_oil_temp = Helpers.celsius_to_fahrenheit((sum(record['oil_temp'] for record in records) + data['avg_oil_temp']) / (len(records) + data['num_entries']))
                avg_mpg = round((sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) + data['avg_mpg']) / (len(records) + data['num_entries']), 2)
                supabase.table('DrivingData').update({"num_entries": (len(records) + data['num_entries']), "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).eq('driving_id', data['driving_id']).execute()
            car_info = Helpers.divide_into_trips(car_info)
            for trip in car_info:
                runtime = trip[-1]['runtime']
                start_time = trip[0]['timestamp']
                end_time = trip[-1]['timestamp']
                start_lat = trip[0]['lattitude']
                start_lon = trip[0]['longitude']
                end_lat = trip[-1]['lattitude']
                end_lon = trip[-1]['longitude']
                avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in trip) / len(trip), 2)
                avg_engine_load = round(sum(record['engine_load'] for record in trip) / len(trip), 2)
                response = supabase.table('DrivingData').select('driving_id').eq('timestamp', Helpers.convert_date(day)).execute()
                try:
                    driving_id = response.data[0]['driving_id']
                except:
                    driving_id = 0
                if driving_id == 0 or driving_id == None:
                    return jsonify({"Error": "Driving ID not found within the Trips"}), 500
                supabase.table('Trips').insert({"driving_id": driving_id, "runtime": runtime, "start_time": start_time, "end_time": end_time, "start_lat": start_lat, "start_lon": start_lon, "end_lat": end_lat, "end_lon": end_lon, "avg_mpg": avg_mpg, "avg_engine_load": avg_engine_load}).execute()

        return jsonify(car_info), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)