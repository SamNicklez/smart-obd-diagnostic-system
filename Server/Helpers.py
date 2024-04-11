from datetime import datetime, timedelta


def calculate_mpg(MAF, Speed):
    if MAF == 0 or Speed == 0:
        return 100
    """
    Calculates the miles per gallon (MPG) based on the Mass Air Flow (MAF) and Speed inputs.

    Args:
        MAF (float): Mass Air Flow in grams per second.
        Speed (float): Speed in miles per hour.

    Returns:
        float: Miles per gallon (MPG) value.
    """
    # Constants
    AFR = 14.7  # Air-Fuel Ratio for gasoline
    GAS_DENSITY = 0.74  # Density of gasoline in kg/L
    GRAMS_PER_POUND = 453.592  # Grams per pound
    LITERS_PER_GALLON = 3.78541  # Liters per gallon

    # Convert MAF from grams per second to pounds per hour
    maf_lb_per_hr = float(MAF) * 3600 / GRAMS_PER_POUND

    # Calculate fuel consumption in gallons per hour
    fuel_consumption_gph = (maf_lb_per_hr / AFR) / (GAS_DENSITY * LITERS_PER_GALLON)

    mpg = round(Speed / fuel_consumption_gph, 2)

    return mpg


def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    
    Args:
    - celsius (float): Temperature in degrees Celsius.
    
    Returns:
    - float: Temperature in degrees Fahrenheit.
    """
    fahrenheit = round(float(celsius) * 9 / 5 + 32, 2)
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

            previous_point = data[i - 1]
            previous_timestamp = datetime.fromisoformat(previous_point['timestamp'])
            current_timestamp = datetime.fromisoformat(point['timestamp'])

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
    grouped_data = {}
    for item in data:
        day = datetime.fromisoformat(item['timestamp']).strftime('%m-%d-%Y')
        if day in grouped_data.keys():
            grouped_data[day].append(item)
        else:
            grouped_data[day] = [item]
    return grouped_data


def convert_date(date):
    date_obj = datetime.strptime(date, '%m-%d-%Y')
    return date_obj.strftime('%Y-%m-%d')


def transform_graph_data(data, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    transformed_data = [
        {"name": "Average MPG", "data": []},
        {"name": "Runtime", "data": []},
        {"name": "Average Coolant Temp", "data": []},
        {"name": "Average Oil Temp", "data": []},
        {"name": "Average Speed", "data": []},
        {"name": "Dates", "data": []}
    ]

    date_data_map = {item["timestamp"]: item for item in data}

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        date_append_str = current_date.strftime('%m-%d-%Y')
        transformed_data[5]["data"].append(date_append_str)

        item = date_data_map.get(date_str)
        if item:
            transformed_data[0]["data"].append(item.get("avg_mpg"))
            transformed_data[1]["data"].append(item.get("runtime"))
            transformed_data[2]["data"].append(item.get("avg_coolant_temp"))
            transformed_data[3]["data"].append(item.get("avg_oil_temp"))
            transformed_data[4]["data"].append(item.get("avg_speed"))
        else:
            for i in range(5):
                transformed_data[i]["data"].append(None)

        current_date += timedelta(days=1)

    return transformed_data
