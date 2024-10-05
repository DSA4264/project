import os
import requests
import pandas as pd
import zipfile
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('API_KEY')

# Define the headers, including the API key from the environment variable
headers = {
    'AccountKey': api_key,
    'accept': 'application/json'
}

# Helper function to fetch paginated data
def fetch_paginated_data(url, headers):
    all_data = []
    skip = 0
    while True:
        response = requests.get(url, headers=headers, params={'$skip': skip})
        if response.status_code == 200:
            data = response.json()
            if not data['value']:
                break
            all_data.extend(data['value'])
            skip += 500
        else:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            break
    return all_data

# 1. Bus Routes API
def fetch_bus_routes():
    print("Fetching Bus Routes...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusRoutes"
    bus_routes_data = fetch_paginated_data(url, headers)
    if bus_routes_data:
        bus_routes_df = pd.DataFrame(bus_routes_data)
        # bus_routes_df.to_csv('data/bus_routes_data.csv', index=False)
        bus_routes_df.to_csv('bus_routes_data.csv', index=False)
        print("Bus Routes data saved to bus_routes_data.csv.")
    else:
        print("No Bus Routes data retrieved.")

# 2. Bus Stops API
def fetch_bus_stops():
    print("Fetching Bus Stops...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusStops"
    bus_stops_data = fetch_paginated_data(url, headers)
    if bus_stops_data:
        bus_stops_df = pd.DataFrame(bus_stops_data)
        # bus_stops_df.to_csv('data/bus_stops_data.csv', index=False)
        bus_stops_df.to_csv('bus_stops_data.csv', index=False)
        print("Bus Stops data saved to bus_stops_data.csv.")
    else:
        print("No Bus Stops data retrieved.")

# Helper function to download and save ZIP file
def download_zip_file(download_url, file_name):
    print(f"Downloading file from {download_url}...")
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded and saved {file_name}.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

# 3. Passenger Volume by Bus Stops API
def fetch_passenger_volume_by_bus_stops(date='202408'):
    print("Fetching Passenger Volume by Bus Stops...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/PV/Bus"
    params = {'Date': date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'value' in data and data['value']:
            download_link = data['value'][0]['Link']
            #download_zip_file(download_link, 'data/transport_node_bus_202408.zip')
            download_zip_file(download_link, 'transport_node_bus_202408.zip')
        else:
            print("No Passenger Volume by Bus Stops data available.")
    else:
        print(f"Failed to retrieve Passenger Volume by Bus Stops. Status code: {response.status_code}")

# 4. Passenger Volume by Origin Destination Bus Stops API
def fetch_od_volume_by_bus_stops(date='202408'):
    print("Fetching Passenger Volume by Origin Destination Bus Stops...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/PV/ODBus"
    params = {'Date': date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'value' in data and data['value']:
            download_link = data['value'][0]['Link']
            # download_zip_file(download_link, 'data/origin_destination_bus_202408.zip')
            download_zip_file(download_link, 'origin_destination_bus_202408.zip')
        else:
            print("No Origin-Destination Bus Stops data available.")
    else:
        print(f"Failed to retrieve OD Bus Stops data. Status code: {response.status_code}")

# 5. Passenger Volume by Origin Destination Train Stations API
def fetch_od_volume_by_train_stations(date='202408'):
    print("Fetching Passenger Volume by Origin Destination Train Stations...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/PV/ODTrain"
    params = {'Date': date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'value' in data and data['value']:
            download_link = data['value'][0]['Link']
            # download_zip_file(download_link, 'data/od_train_volume_202408.zip')
            download_zip_file(download_link, 'od_train_volume_202408.zip')
        else:
            print("No Origin-Destination Train Stations data available.")
    else:
        print(f"Failed to retrieve OD Train Stations data. Status code: {response.status_code}")

# 6. Train Station - Geospatial Whole Island API
def fetch_train_stn_geospatial_whole_island(date='202408'):
    print("Fetching Train Station - Geospatial Whole Island...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    params = {'Date': date,
              'ID': 'TrainStation'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # download_link = data.get('Link')
        if 'value' in data and data['value']:
            download_link = data['value'][0]['Link']
            # download_zip_file(download_link, 'data/train_station_geospatial_whole_island_202408.zip')
            download_zip_file(download_link, 'train_station_geospatial_whole_island_202408.zip')
        else:
            print("No Train Station - Geospatial Whole Island data available.")
    else:
        print(f"Failed to retrieve Train Station - Geospatial Whole Island data. Status code: {response.status_code}")

# 7. Train Station - Geospatial Whole Island API
def fetch_train_stn_exit_geospatial_whole_island(date='202408'):
    print("Fetching Train Station Exit - Geospatial Whole Island...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    params = {'Date': date,
              'ID': 'TrainStationExit'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # download_link = data.get('Link')
        if 'value' in data and data['value']:
            download_link = data['value'][0]['Link']
            # download_zip_file(download_link, 'data/train_station_exit_geospatial_whole_island_202408.zip')
            download_zip_file(download_link, 'train_station_exit_geospatial_whole_island_202408.zip')
        else:
            print("No Train Station Exit - Geospatial Whole Island data available.")
    else:
        print(f"Failed to retrieve Train Station Exit - Geospatial Whole Island data. Status code: {response.status_code}")

# 8. Bus Stop Location - Geospatial Whole Island API
def fetch_bus_stop_geospatial_whole_island(date='202408'):
    print("Fetching Bus Stop Location - Geospatial Whole Island...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    params = {'Date': date,
              'ID': 'BusStopLocation'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # download_link = data.get('Link')
        if 'value' in data and data['value']:
            download_link = data['value'][0]['Link']
            # download_zip_file(download_link, 'data/bus_stop_location_geospatial_whole_island_202408.zip')
            download_zip_file(download_link, 'bus_stop_location_geospatial_whole_island_202408.zip')
        else:
            print("No Bus Stop Location - Geospatial Whole Island data available.")
    else:
        print(f"Failed to retrieve Bus Stop Location - Geospatial Whole Island data. Status code: {response.status_code}")

# Fetch all data
def fetch_all_data():
    fetch_bus_routes()
    fetch_bus_stops()
    fetch_passenger_volume_by_bus_stops()
    fetch_od_volume_by_bus_stops()
    fetch_od_volume_by_train_stations()
    fetch_train_stn_geospatial_whole_island()
    fetch_train_stn_exit_geospatial_whole_island()
    fetch_bus_stop_geospatial_whole_island()

# Execute the data fetching
fetch_all_data()
