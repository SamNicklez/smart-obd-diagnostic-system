
import requests

def get_vehicle_info_by_vin(vin):
    """
    Fetches vehicle information by VIN from the NHTSA API.
    
    :param vin: Vehicle Identification Number (string)
    :return: Dictionary with vehicle information
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('Results', [])[0]
        make = results.get('Make')
        model = results.get('Model')
        year = results.get('ModelYear')
        
        return {
            'Make': make,
            'Model': model,
            'Year': year
        }
    else:
        return {"Error": "Failed to fetch data"}

if __name__ == "__main__":
    vin = input("Enter the VIN of the vehicle: ")
    vehicle_info = get_vehicle_info_by_vin(vin)
    print(vehicle_info)
