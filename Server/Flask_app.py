from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
from Test_data import generate_car_info_json
import os

def calculate_mpg(MAF, Speed):
    """
    Calculates the miles per gallon (MPG) based on the Mass Air Flow (MAF) and Speed inputs.

    Args:
        MAF (float): Mass Air Flow in grams per second.
        Speed (float): Speed in kilometers per hour.

    Returns:
        float: Miles per gallon (MPG) value.
    """
    # Constants
    AFR = 14.7  # Air-Fuel Ratio for gasoline
    GAS_DENSITY = 0.74  # Density of gasoline in kg/L
    GRAMS_PER_POUND = 453.592  # Grams per pound
    LITERS_PER_GALLON = 3.78541  # Liters per gallon
    KM_PER_MILE = 1.60934  # Kilometers per mile
    
    # Convert MAF from grams per second to pounds per hour
    maf_lb_per_hr = MAF * 3600 / GRAMS_PER_POUND
    
    # Calculate fuel consumption in gallons per hour
    fuel_consumption_gph = (maf_lb_per_hr / AFR) / (GAS_DENSITY * LITERS_PER_GALLON)
    speed_mph = Speed / KM_PER_MILE
    
    mpg = round(speed_mph / fuel_consumption_gph, 2)

    return mpg

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
    
@app.route("/stage", methods=["POST"])
def stage():
    try:
        # data = request.get_json()
        # response = supabase.table('stage').insert(data).execute()
        json_data = generate_car_info_json()
        print(json_data)
        return jsonify({"Test": "GOOD"}), 200
    except Exception as e:
        return jsonify({"Error": "Interal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)