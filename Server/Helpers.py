from datetime import datetime, timedelta
from collections import defaultdict
import json

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

def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    
    Args:
    - celsius (float): Temperature in degrees Celsius.
    
    Returns:
    - float: Temperature in degrees Fahrenheit.
    """
    fahrenheit = round(celsius * 9/5 + 32, 2)
    return fahrenheit

def kph_to_mph(kph):
    """
    Convert kilometers per hour to miles per hour and round to two decimal places.
    
    Args:
    - kph (float): Speed in kilometers per hour.
    
    Returns:
    - float: Speed in miles per hour, rounded to two decimal places.
    """
    mph = kph * 0.621371
    return round(mph, 2)

def divide_into_trips(data, time_threshold_minutes=30):
    """
    Divide driving data into trips based on a time threshold.
    
    Args:
    - data (list of dicts): The driving data, sorted chronologically.
    - time_threshold_minutes (int): The threshold in minutes to define a new trip.
    
    Returns:
    - list of lists: A list where each element is a list of data points representing a trip.
    """
    try:
        trips = []
        current_trip = []
        
        for i, point in enumerate(data):
            if i == 0:
                current_trip.append(point)
                continue
            
            previous_point = data[i-1]
            previous_timestamp = datetime.strptime(previous_point['timestamp'], '%Y-%m-%d %H:%M:%S')
            current_timestamp = datetime.strptime(point['timestamp'], '%Y-%m-%d %H:%M:%S')
            
            if (current_timestamp - previous_timestamp) > timedelta(minutes=time_threshold_minutes):
                trips.append(current_trip)
                current_trip = []
            
            current_trip.append(point)
        
        if current_trip:
            trips.append(current_trip)
        
        return trips
    except Exception as e:
        print(e)
        return

def group_by_day(data):
    grouped_data = defaultdict(list)
    for item in data:
        day = datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%Y')
        grouped_data[day].append(item)
    return grouped_data

def convert_date(date):
    date_obj = datetime.strptime(date, '%m-%d-%Y')
    return date_obj.strftime('%Y-%m-%d')