from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os


def init():
    """
    Initializes the server by retrieving data from the 'stage' table in Supabase.
    """
    response = supabase.table('stage').select("*").execute()
    if(response.count != 0):
        print(response)


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
    density_of_gasoline_kg_per_l = 0.74  # Density of gasoline in kg/L
    grams_per_pound = 453.592  # Grams per pound
    liters_per_gallon = 3.78541  # Liters per gallon
    km_per_mile = 1.60934  # Kilometers per mile
    
    # Convert MAF from grams per second to pounds per hour
    maf_lb_per_hr = MAF * 3600 / grams_per_pound
    
    # Calculate fuel consumption in gallons per hour
    fuel_consumption_gph = (maf_lb_per_hr / AFR) / (density_of_gasoline_kg_per_l * liters_per_gallon)
    speed_mph = Speed / km_per_mile
    
    mpg = round(speed_mph / fuel_consumption_gph, 2)

    return mpg

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)
init()

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
    


if __name__ == '__main__':
    app.run(debug=True)