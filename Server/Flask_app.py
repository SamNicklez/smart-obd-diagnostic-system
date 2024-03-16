from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
from Test_data import generate_car_info_json
import Helpers
import os
import json

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Test Flask API!"

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        response = supabase.table('Users').select("*").eq('username', data['username']).eq('password', data['password']).execute()
        if(response.count == 0):
            return jsonify({"Error": "Invalid username or password"}), 401
        else:
            return jsonify("Login"), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/grabcardetails", methods=["GET"])
def grab_car_details():
    try:
        response = supabase.table('Cars').select("*").execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/postcardetails", methods=["POST"])
def post_car_details():
    try:
        data = request.get_json()
        response = supabase.table('Cars').insert(data).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500

# CHANGE TO POST ROUTE EVENTUALLY
@app.route("/stage", methods=["POST"])
def stage():
    try:
        car_info = request.get_json()
        grouped_data = Helpers.group_by_day(car_info)
        # process data into generalized day data
        for day, records in grouped_data.items():
            response = supabase.table('DrivingData').select('*').eq('timestamp', day).execute()
            # If new entry
            if(response.count == 0):
                average_speed = Helpers.kph_to_mph(sum(record['speed'] for record in records) / len(records))
                total_runtime = sum(record['runtime'] for record in records)
                average_coolant_temp = Helpers.celsius_to_fahrenheit(sum(record['coolant_temp'] for record in records) / len(records))
                average_oil_temp = Helpers.celsius_to_fahrenheit(sum(record['oil_temp'] for record in records) / len(records))
                avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) / len(records), 2)
                supabase.table('DrivingData').insert({"num_entries": len(records), "timestamp": day, "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            # If entry already exists
            else:
                data, _ = supabase.table('DrivingData').select("*").eq('timestamp', day).execute()
                average_speed = Helpers.kph_to_mph((sum(record['speed'] for record in records) + data['avg_speed'])/ (len(records) + data['num_entries']))
                total_runtime = sum(record['runtime'] for record in records) + data['rumtime']
                average_coolant_temp = Helpers.celsius_to_fahrenheit((sum(record['coolant_temp'] for record in records) + data['avg_coolant_temp']) / (len(records) + data['num_entries']))
                average_oil_temp = Helpers.celsius_to_fahrenheit((sum(record['oil_temp'] for record in records) + data['avg_oil_temp']) / (len(records) + data['num_entries']))
                avg_mpg = round((sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) + data['avg_mpg']) / (len(records) + data['num_entries']), 2)
                supabase.table('DrivingData').update({"num_entries": (len(records) + data['num_entries']), "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).eq('driving_id', data['driving_id']).execute()
            # here process trips

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
            response = supabase.table('DrivingData').select('*').eq('timestamp', day).execute()
            # If new entry
            if(response.count == 0):
                average_speed = Helpers.kph_to_mph(sum(record['speed'] for record in records) / len(records))
                total_runtime = sum(record['runtime'] for record in records)
                average_coolant_temp = Helpers.celsius_to_fahrenheit(sum(record['coolant_temp'] for record in records) / len(records))
                average_oil_temp = Helpers.celsius_to_fahrenheit(sum(record['oil_temp'] for record in records) / len(records))
                avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) / len(records), 2)
                supabase.table('DrivingData').insert({"num_entries": len(records), "timestamp": day, "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            # If entry already exists
            else:
                data, _ = supabase.table('DrivingData').select("*").eq('timestamp', day).execute()
                average_speed = Helpers.kph_to_mph((sum(record['speed'] for record in records) + data['avg_speed'])/ (len(records) + data['num_entries']))
                total_runtime = sum(record['runtime'] for record in records) + data['rumtime']
                average_coolant_temp = Helpers.celsius_to_fahrenheit((sum(record['coolant_temp'] for record in records) + data['avg_coolant_temp']) / (len(records) + data['num_entries']))
                average_oil_temp = Helpers.celsius_to_fahrenheit((sum(record['oil_temp'] for record in records) + data['avg_oil_temp']) / (len(records) + data['num_entries']))
                avg_mpg = round((sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) + data['avg_mpg']) / (len(records) + data['num_entries']), 2)
                supabase.table('DrivingData').update({"num_entries": (len(records) + data['num_entries']), "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).eq('driving_id', data['driving_id']).execute()
            car_info = Helpers.divide_into_trips(car_info)

        return jsonify(car_info), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)