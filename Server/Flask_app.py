from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
from Test_data import generate_car_info_json
from datetime import datetime
from collections import defaultdict
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
        response = supabase.table('users').select("*").eq('username', data['username']).eq('password', data['password']).execute()
        if(response.count == 0):
            return jsonify({"Error": "Invalid username or password"}), 401
        else:
            return jsonify("Login"), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500
    
@app.route("/stage", methods=["GET"])
def stage():
    try:
        # data = request.get_json()
        # response = supabase.table('stage').insert(data).execute()
        car_info = json.loads(generate_car_info_json())
        grouped_data = Helpers.group_by_day(car_info)

        for day, records in grouped_data.items():
            response = supabase.table('DrivingData').select('*').eq('date', day).execute()
            average_speed = Helpers.kph_to_mph(sum(record['speed'] for record in records) / len(records))
            total_runtime = sum(record['runtime'] for record in records)
            average_coolant_temp = Helpers.celsius_to_fahrenheit(sum(record['coolant_temp'] for record in records) / len(records))
            average_oil_temp = Helpers.celsius_to_fahrenheit(sum(record['oil_temp'] for record in records) / len(records))
            avg_mpg = round(sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) / len(records), 2)
            if(response.count == 0):
                supabase.table('DrivingData').insert({"num_entries": len(records), "timestamp": day, "avg_speed": average_speed, "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp, "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            else:
                break
            

        return jsonify({"Test": "GOOD"}), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)