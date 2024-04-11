import json
import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client

import Helpers
from Test_data import generate_car_info_json
from __init__ import token_auth

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
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        response = supabase.table('Users').select("*").eq('username', data['username']).eq('password',
                                                                                           data['password']).execute()
        if response.data == []:
            return jsonify({"Error": "Invalid username or password"}), 401
        else:
            encoded_token = jwt.encode({"id": 1}, "secret", algorithm="HS256")
            return jsonify({"token": encoded_token}), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/grabcardetails", methods=["GET"])
@token_auth.login_required
def grab_car_details():
    try:
        response = supabase.table('Cars').select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/postcardetails", methods=["POST"])
@token_auth.login_required
def post_car_details():
    try:
        data = request.get_json()
        response = supabase.table('Cars').insert(data).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/grabOBDData", methods=["GET"])
@token_auth.login_required
def grab_obd_data():
    try:
        response = supabase.table('OBDData').select("*").execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Internal Server Error: " + str(e)}), 500


@app.route("/postOBDData", methods=["POST"])
@token_auth.login_required
def post_obd_data():
    try:
        data = request.get_json()
        response = supabase.table('OBD').insert(data).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/grabNotifications", methods=["GET"])
@token_auth.login_required
def grab_notifications():
    try:
        response, _ = supabase.table('OBD').select("*").eq('dismissed', False).execute()
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route('/dismissNotification', methods=["POST"])
@token_auth.login_required
def dismiss_notification():
    try:
        data = request.get_json()
        response = supabase.table('OBD').update({"dismissed": True}).eq('obd_id', data['obd_id']).execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/stage", methods=["POST"])
@token_auth.login_required
def stage():
    try:
        car_info = request.get_json()
        grouped_data = Helpers.group_by_day(car_info)
        # process data into generalized day data
        for day in grouped_data.keys():
            records = grouped_data[day]
            temp = supabase.table('DrivingData').select('*').eq('timestamp', day).execute()
            response = temp.data[0]['driving_id'] if temp.data != [] else 0
            # If new entry
            if response == 0:
                if len(records) == 1:
                    average_speed = records[0]['speed']
                    total_runtime = records[0]['runtime']
                    average_coolant_temp = records[0]['coolant_temp']
                    average_oil_temp = records[0]['oil_temp']
                    avg_mpg = round(Helpers.calculate_mpg(records[0]['airflow_rate'], records[0]['speed']), 2)
                    supabase.table('DrivingData').insert(
                        {"num_entries": len(records), "timestamp": day, "avg_speed": average_speed,
                         "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp,
                         "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()

                    # TODO: Add DTC
                else:
                    filtered_speed = [record['speed'] for record in records if record['speed'] != "None"]
                    if len(filtered_speed) == 0:
                        average_speed = 0
                    else:
                        average_speed = sum(filtered_speed) / len(filtered_speed)

                    filtered_runtime = [record['runtime'] for record in records if record['runtime'] != "None"]
                    if len(filtered_runtime) == 0:
                        total_runtime = 0
                    else:
                        total_runtime = 0
                        temp_max = -1
                        for x in filtered_runtime:
                            if x >= temp_max:
                                temp_max = x
                                if x == filtered_runtime[-1]:
                                    total_runtime += temp_max
                            elif x < temp_max:
                                total_runtime += temp_max
                                temp_max = -1

                    filtered_coolant_temp = [record['coolant_temp'] for record in records if
                                             record['coolant_temp'] != "None"]
                    if len(filtered_coolant_temp) == 0:
                        average_coolant_temp = 0
                    else:
                        average_coolant_temp = sum(filtered_coolant_temp) / len(filtered_coolant_temp)

                    filtered_oil_temp = [record['oil_temp'] for record in records if record['oil_temp'] != "None"]
                    if len(filtered_oil_temp) == 0:
                        average_oil_temp = 0
                    else:
                        average_oil_temp = sum(filtered_oil_temp) / len(filtered_oil_temp)

                    avg_mpg = round(
                        sum([Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in
                             records]) / len(
                            records), 2)

                    supabase.table('DrivingData').insert(
                        {"num_entries": len(records), "timestamp": day, "avg_speed": average_speed,
                         "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp,
                         "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            # If entry already exists
            else:
                data, _ = supabase.table('DrivingData').select("*").eq('timestamp', day).execute()

                data = data[1][0]
                print(data)

                filtered_speed = [record['speed'] for record in records if record['speed'] != "None"]
                if len(filtered_speed) == 0:
                    average_speed = data['avg_speed']
                else:
                    average_speed = (sum(filtered_speed) + (data['avg_speed'] * data['num_entries'])) / (
                            len(filtered_speed) + data['num_entries'])

                filtered_runtime = [record['runtime'] for record in records if record['runtime'] != "None"]
                if len(filtered_runtime) == 0:
                    total_runtime = data['runtime']
                elif filtered_runtime[0] > 1:
                    total_runtime = data['runtime'] - (filtered_runtime[0] - 1)
                    temp_total_runtime = 0
                    temp_max = -1
                    for x in filtered_runtime:
                        if x >= temp_max:
                            temp_max = x
                            if x == filtered_runtime[-1]:
                                temp_total_runtime += temp_max
                        elif x < temp_max:
                            temp_total_runtime += temp_max
                            temp_max = -1
                    total_runtime = temp_total_runtime + total_runtime
                else:
                    temp_total_runtime = 0
                    temp_max = -1
                    for x in filtered_runtime:
                        if x >= temp_max:
                            temp_max = x
                            if x == filtered_runtime[-1]:
                                temp_total_runtime += temp_max
                        elif x < temp_max:
                            temp_total_runtime += temp_max
                            temp_max = -1
                    total_runtime = temp_total_runtime + data['runtime']

                filtered_coolant_temp = [record['coolant_temp'] for record in records if
                                         record['coolant_temp'] != "None"]
                if len(filtered_coolant_temp) == 0:
                    average_coolant_temp = data['avg_coolant_temp']
                else:
                    average_coolant_temp = (sum(filtered_coolant_temp) + (
                            data['avg_coolant_temp'] * data['num_entries'])) / (
                                                   len(filtered_coolant_temp) + data['num_entries'])

                filtered_oil_temp = [record['oil_temp'] for record in records if record['oil_temp'] != "None"]
                if len(filtered_oil_temp) == 0:
                    average_oil_temp = data['avg_oil_temp']
                else:
                    average_oil_temp = (sum(filtered_oil_temp) + (data['avg_oil_temp'] * data['num_entries'])) / (
                            len(filtered_oil_temp) + data['num_entries'])

                avg_mpg = round(
                    (sum([Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records]) + (
                            data['avg_mpg'] * data['num_entries'])) / (len(records) + data['num_entries']), 2)

                supabase.table('DrivingData').update(
                    {"num_entries": len(records) + data['num_entries'], "avg_speed": average_speed,
                     "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp,
                     "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).eq('driving_id',
                                                                               data['driving_id']).execute()

            car_info = Helpers.divide_into_trips(car_info)

            for trip in car_info:
                runtime = trip[-1]['runtime']
                start_time = trip[0]['timestamp']
                end_time = trip[-1]['timestamp']
                start_lat = trip[0]['latitude']
                start_lon = trip[0]['longitude']
                end_lat = trip[-1]['latitude']
                end_lon = trip[-1]['longitude']
                avg_mpg = round(
                    sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in trip) / len(trip),
                    2)
                avg_engine_load = round(sum(record['engine_load'] for record in trip) / len(trip), 2)
                response = supabase.table('DrivingData').select('driving_id').eq('timestamp', day).execute()
                driving_id = response.data[0]['driving_id'] if response.data[0]['driving_id'] else 0
                if driving_id == 0 or driving_id == None:
                    print("Driving ID not found within the Trips")
                    return jsonify({"Error": "Driving ID not found within the Trips"}), 500
                supabase.table('Trips').insert(
                    {"driving_id": driving_id, "runtime": runtime, "start_time": start_time, "end_time": end_time,
                     "start_lat": start_lat, "start_lon": start_lon, "end_lat": end_lat, "end_lon": end_lon,
                     "avg_mpg": avg_mpg, "avg_engine_load": avg_engine_load}).execute()

        return jsonify({"Test": "GOOD"}), 200
    except Exception as e:
        print("ERROR: " + str(e))
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


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
            if (response == 0):
                average_speed = sum(record['speed'] for record in records) / len(records)
                total_runtime = max(record['runtime'] for record in records)
                average_coolant_temp = sum(record['coolant_temp'] for record in records) / len(records)
                average_oil_temp = sum(record['oil_temp'] for record in records) / len(records)
                avg_mpg = round(
                    sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) / len(
                        records), 2)
                supabase.table('DrivingData').insert(
                    {"num_entries": len(records), "timestamp": day, "avg_speed": average_speed,
                     "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp,
                     "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).execute()
            # If entry already exists
            else:
                data, _ = supabase.table('DrivingData').select("*").eq('timestamp', day).execute()
                average_speed = (sum(record['speed'] for record in records) + (
                        data['avg_speed'] * data['num_entries'])) / (
                                        len(records) + data['num_entries'])
                total_runtime = max(record['runtime'] for record in records) + data['rumtime']
                average_coolant_temp = (sum(record['coolant_temp'] for record in records) + (
                        data['avg_coolant_temp'] * data['num_entries'])) / (
                                               len(records) + data['num_entries'])
                average_oil_temp = (sum(record['oil_temp'] for record in records) + (
                        data['avg_oil_temp'] * data['num_entries'])) / (
                                           len(records) + data['num_entries'])
                avg_mpg = round((sum(
                    Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in records) + (data[
                                                                                                                 'avg_mpg'] *
                                                                                                             data[
                                                                                                                 'num_entries'])) / (
                                        len(records) + data['num_entries']), 2)
                supabase.table('DrivingData').update(
                    {"num_entries": (len(records) + data['num_entries']), "avg_speed": average_speed,
                     "runtime": total_runtime, "avg_coolant_temp": average_coolant_temp,
                     "avg_oil_temp": average_oil_temp, "avg_mpg": avg_mpg}).eq('driving_id',
                                                                               data['driving_id']).execute()
            car_info = Helpers.divide_into_trips(car_info)
            for trip in car_info:
                runtime = trip[-1]['runtime']
                start_time = trip[0]['timestamp']
                end_time = trip[-1]['timestamp']
                start_lat = trip[0]['latitude']
                start_lon = trip[0]['longitude']
                end_lat = trip[-1]['latitude']
                end_lon = trip[-1]['longitude']
                avg_mpg = round(
                    sum(Helpers.calculate_mpg(record['airflow_rate'], record['speed']) for record in trip) / len(trip),
                    2)
                avg_engine_load = round(sum(record['engine_load'] for record in trip) / len(trip), 2)
                response = supabase.table('DrivingData').select('driving_id').eq('timestamp', day).execute()
                try:
                    driving_id = response.data[0]['driving_id']
                except:
                    driving_id = 0
                if driving_id == 0 or driving_id == None:
                    return jsonify({"Error": "Driving ID not found within the Trips"}), 500
                supabase.table('Trips').insert(
                    {"driving_id": driving_id, "runtime": runtime, "start_time": start_time, "end_time": end_time,
                     "start_lat": start_lat, "start_lon": start_lon, "end_lat": end_lat, "end_lon": end_lon,
                     "avg_mpg": avg_mpg, "avg_engine_load": avg_engine_load}).execute()

        return jsonify(car_info), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Internal Server Error"}), 500


@app.route("/grabData", methods=["GET"])
@token_auth.login_required
def grab_data():
    try:
        response, _ = supabase.table('DrivingData').select("*").execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/grabTrips", methods=["GET"])
@token_auth.login_required
def grab_trips():
    try:
        response, _ = supabase.table('Trips').select("*").execute()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/grabCurrentData", methods=["GET"])
@token_auth.login_required
def grab_current_data():
    try:
        response, _ = supabase.table('DrivingData').select("*").order('timestamp', desc=True).limit(1).execute()
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route("/grabCurrentTrip", methods=["GET"])
@token_auth.login_required
def grab_current_trip():
    try:
        trip_id = request.args.get('trip_id', None)
        print(trip_id)
        response, _ = supabase.table('Trips').select("*").eq('trip_id', trip_id).execute()

        print(response)
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Interal Server Error: " + str(e)}), 500


@app.route('/grabGraphData', methods=["POST"])
@token_auth.login_required
def grab_graph_data():
    try:
        data = request.get_json()
        start_date = data['start_date']
        start_date_obj = datetime.strptime(start_date, "%m/%d/%Y") + timedelta(days=1)
        end_date_obj = datetime.today()
        db_start_date = start_date_obj.strftime("%Y-%m-%d")
        db_end_date = end_date_obj.strftime("%Y-%m-%d")
        response, _ = supabase.table('DrivingData').select("*").gte('timestamp', db_start_date).lte('timestamp',
                                                                                                    db_end_date).execute()
        response = response[1]
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Internal Server Error: " + str(e)}), 500


@app.route('/grabSpecificGraphData', methods=["POST"])
@token_auth.login_required
def grab_specific_graph_data():
    try:
        data = request.get_json()
        start_date = data['start_date']
        end_date = data['end_date']
        start_date_obj = datetime.strptime(start_date, "%m/%d/%Y")
        end_date_obj = datetime.strptime(end_date, "%m/%d/%Y")
        db_start_date = start_date_obj.strftime("%Y-%m-%d")
        db_end_date = end_date_obj.strftime("%Y-%m-%d")
        response, _ = supabase.table('DrivingData').select("*").gte('timestamp', db_start_date).lte('timestamp',
                                                                                                    db_end_date).execute()
        response = response[1]
        response = Helpers.transform_graph_data(response, db_start_date, db_end_date)
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"Error": "Internal Server Error: " + str(e)}), 500


if __name__ == '__main__':
    # app.run(debug=True, port=5000, host='0.0.0.0')
    app.run(debug=True)
