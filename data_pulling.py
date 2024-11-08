import os
import requests
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Define the headers, including the API key from the environment variable
headers = {"AccountKey": api_key, "accept": "application/json"}

# Set the data folder for saving files
data_folder = "data"

# Ensure the data folder exists
os.makedirs(data_folder, exist_ok=True)


# Helper function to fetch paginated data
def fetch_paginated_data(url, headers):
    all_data = []
    skip = 0
    while True:
        response = requests.get(url, headers=headers, params={"$skip": skip})
        if response.status_code == 200:
            data = response.json()
            if not data["value"]:
                break
            all_data.extend(data["value"])
            skip += 500
        else:
            print(
                f"Failed to retrieve data from {url}. Status code: {response.status_code}"
            )
            break
    return all_data


# 1. Bus Routes API
def fetch_bus_routes():
    print("Fetching Bus Routes...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusRoutes"
    bus_routes_data = fetch_paginated_data(url, headers)
    if bus_routes_data:
        bus_routes_df = pd.DataFrame(bus_routes_data)
        bus_routes_path = os.path.join(data_folder, "bus_routes_data.csv")
        bus_routes_df.to_csv(bus_routes_path, index=False)
        print(f"Bus Routes data saved to {bus_routes_path}.")
    else:
        print("No Bus Routes data retrieved.")


# 2. Bus Stops API
def fetch_bus_stops():
    print("Fetching Bus Stops...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusStops"
    bus_stops_data = fetch_paginated_data(url, headers)
    if bus_stops_data:
        bus_stops_df = pd.DataFrame(bus_stops_data)
        bus_stops_path = os.path.join(data_folder, "bus_stops_data.csv")
        bus_stops_df.to_csv(bus_stops_path, index=False)
        print(f"Bus Stops data saved to {bus_stops_path}.")
    else:
        print("No Bus Stops data retrieved.")


# Helper function to download and save ZIP file
def download_zip_file(download_url, file_name):
    print(f"Downloading file from {download_url}...")
    response = requests.get(download_url)
    if response.status_code == 200:
        zip_path = os.path.join(data_folder, file_name)
        with open(zip_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded and saved {zip_path}.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


# 3. Passenger Volume by Bus Stops API
def fetch_passenger_volume_by_bus_stops(date="202408"):
    print("Fetching Passenger Volume by Bus Stops...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/PV/Bus"
    params = {"Date": date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "value" in data and data["value"]:
            download_link = data["value"][0]["Link"]
            download_zip_file(download_link, "transport_node_bus_202408.zip")
        else:
            print("No Passenger Volume by Bus Stops data available.")
    else:
        print(
            f"Failed to retrieve Passenger Volume by Bus Stops. Status code: {response.status_code}"
        )


# 4. Passenger Volume by Origin Destination Bus Stops API
def fetch_od_volume_by_bus_stops(date):
    print("Fetching Passenger Volume by Origin Destination Bus Stops...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/PV/ODBus"
    params = {"Date": date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "value" in data and data["value"]:
            filename = "origin_destination_bus_" + date + ".zip"
            download_link = data["value"][0]["Link"]
            download_zip_file(download_link, filename)
        else:
            print("No Origin-Destination Bus Stops data available.")
    else:
        print(
            f"Failed to retrieve OD Bus Stops data for {date}. Status code: {response.status_code}"
        )

# 5. Passenger Volume by Origin Destination Train Stations API
def fetch_od_volume_by_train_stations(date="202408"):
    print("Fetching Passenger Volume by Origin Destination Train Stations...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/PV/ODTrain"
    params = {"Date": date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "value" in data and data["value"]:
            download_link = data["value"][0]["Link"]
            download_zip_file(download_link, "od_train_volume_202408.zip")
        else:
            print("No Origin-Destination Train Stations data available.")
    else:
        print(
            f"Failed to retrieve OD Train Stations data. Status code: {response.status_code}"
        )


# 6. Train Station - Geospatial Whole Island API
def fetch_train_stn_geospatial_whole_island(date="202408"):
    print("Fetching Train Station - Geospatial Whole Island...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    params = {"Date": date, "ID": "TrainStation"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "value" in data and data["value"]:
            download_link = data["value"][0]["Link"]
            download_zip_file(
                download_link, "train_station_geospatial_whole_island_202408.zip"
            )
        else:
            print("No Train Station - Geospatial Whole Island data available.")
    else:
        print(
            f"Failed to retrieve Train Station - Geospatial Whole Island data. Status code: {response.status_code}"
        )


# 7. Train Station - Geospatial Whole Island Exit API
def fetch_train_stn_exit_geospatial_whole_island(date="202408"):
    print("Fetching Train Station Exit - Geospatial Whole Island...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    params = {"Date": date, "ID": "TrainStationExit"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "value" in data and data["value"]:
            download_link = data["value"][0]["Link"]
            download_zip_file(
                download_link, "train_station_exit_geospatial_whole_island_202408.zip"
            )
        else:
            print("No Train Station Exit - Geospatial Whole Island data available.")
    else:
        print(
            f"Failed to retrieve Train Station Exit - Geospatial Whole Island data. Status code: {response.status_code}"
        )


# 8. Bus Stop Location - Geospatial Whole Island API
def fetch_bus_stop_geospatial_whole_island(date="202408"):
    print("Fetching Bus Stop Location - Geospatial Whole Island...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    params = {"Date": date, "ID": "BusStopLocation"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "value" in data and data["value"]:
            download_link = data["value"][0]["Link"]
            download_zip_file(
                download_link, "bus_stop_location_geospatial_whole_island_202408.zip"
            )
        else:
            print("No Bus Stop Location - Geospatial Whole Island data available.")
    else:
        print(
            f"Failed to retrieve Bus Stop Location - Geospatial Whole Island data. Status code: {response.status_code}"
        )


# 9. MRT Line to Name
def fetch_mrt_line():
    # Function to map MRT lines and create indicator variables
    def mrt_line_mapping(df):
        # Flatten the column names if they are MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ["_".join(col).strip() for col in df.columns.values]

        # Assuming the MRT line code is in the first column, adjust as necessary
        line_column = "Alpha-numeric code(s)_In operation"

        # Extract the MRT line codes (first 2 characters of the identified column)
        df["MRT_Lines"] = df[line_column].str.extract("([A-Z]{2})")

        # Split multiple lines in case a station belongs to multiple MRT lines
        df["MRT_Lines_List"] = df[line_column].str.findall(r"[A-Z]{2}")

        # Create indicator variables for each MRT line
        mrt_lines = [
            "NS",
            "EW",
            "DT",
            "CC",
            "NE",
            "TE",
            "CG",
            "CE",
        ]  # Add more as necessary

        for line in mrt_lines:
            df[line] = df["MRT_Lines_List"].apply(lambda x: 1 if line in x else 0)

        # Filter out rows that contain MRT lines you want to remove (CP, CR, CA, JR)
        unwanted_lines = ["CP", "CR", "CA", "JR"]
        df = df[~df["MRT_Lines"].isin(unwanted_lines)]

        # List of station names to remove
        unwanted_station_names = [
            "Thomson–East Coast Line Extension (TELe)",
            "Thomson–East Coast Line (TEL)",
            "North East Line Extension (NELe)",
            "North East Line (NEL)",
            "Jurong Region Line (JRL)",
            "East–West Line (EWL)",
            "Cross Island Line (CRL)",
            "Punggol Extension (CPe)",
            "Circle Line Extension (CCLe)",
            "Circle Line (CCL)",
            "Changi Airport Branch Line (CAL)",
        ]

        # Remove rows with unwanted station names
        df = df[~df["Station name_English • Malay"].isin(unwanted_station_names)]

        # Keep the station name and the extracted MRT lines with indicator variables
        result_df = df[["Station name_English • Malay", "MRT_Lines"] + mrt_lines]

        # Remove rows with any NA values
        result_df = result_df.dropna()

        return result_df

    # URL of the Wikipedia page containing the table
    url = "https://en.wikipedia.org/wiki/List_of_Singapore_MRT_stations"

    # Send a GET request to fetch the content of the page
    response = requests.get(url)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first table with the class "wikitable sortable"
    table = soup.find("table", {"class": "wikitable sortable"})

    # Read the table into a pandas DataFrame
    df = pd.read_html(str(table))[0]

    # Apply the mrt_line_mapping function to extract MRT lines and create indicator variables
    df_with_lines = mrt_line_mapping(df)

    # Check if the DataFrame is not empty before saving it
    if not df_with_lines.empty:
        mrt_df = pd.DataFrame(df_with_lines)
        mrt_df_path = os.path.join(
            data_folder, "singapore_mrt_stations_with_lines_filtered.csv"
        )
        mrt_df.to_csv(mrt_df_path, index=False)
        print(
            f"Filtered table with MRT line indicators has been saved to '{mrt_df_path}'"
        )
    else:
        print("No data available after filtering.")

def fetch_bus_services():
    print("Fetching Bus Services...")
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusServices"
    headers = {"AccountKey": api_key, "accept": "application/json"}
    all_buses = []

    # Loop to handle paginated data
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Append data to the list
        all_buses.extend(data['value'])
        
        # Check for next page
        url = data.get('@odata.nextLink', None)

    # Convert list to DataFrame and save to CSV
    if all_buses:
        all_buses_from_lta = pd.DataFrame(all_buses)
        bus_services_path = os.path.join(data_folder, "BusServicesInfo.csv")
        all_buses_from_lta.to_csv(bus_services_path, index=False)
        print(f"Bus Services data saved to {bus_services_path}.")
    else:
        print("No Bus Services data retrieved.")

# 1. Fetch Planning Area Names Data and Save to CSV
def fetch_planning_area_names():
    print("Fetching Planning Area Names...")
    url = "https://www.onemap.gov.sg/api/public/popapi/getPlanningareaNames?year=2019"
    headers = {"Authorization": ACCESS_TOKEN}
    
    # Request data from the API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        df_planning_area = pd.DataFrame(data)  # Convert data to DataFrame
        
        # Save to CSV
        planning_area_path = os.path.join(data_folder, "PlanningAreaNames.csv")
        df_planning_area.to_csv(planning_area_path, index=False)
        print(f"Planning area names data saved to {planning_area_path}.")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")

# Define the file path for the Excel file
file_path = r'data/population_data.xlsx'

# 1. Fetch Population by Planning Area Data and Save to CSV
def fetch_population_data():
    print("Fetching population data by planning area...")
    
    # Attempt to load the Excel file
    try:
        df_population_planning_area = pd.read_excel(file_path, header=2)
        print("Population data successfully fetched.")
        
        # Save to CSV
        data_folder = "data"
        os.makedirs(data_folder, exist_ok=True)
        population_data_path = os.path.join(data_folder, "population_planning_area_data.csv")
        df_population_planning_area.to_csv(population_data_path, index=False)
        print(f"Population data saved to {population_data_path}.")
    except FileNotFoundError:
        print(f"File not found at {file_path}. Please check the path and try again.")
        return None

def fetch_planning_area_data():
    print("Fetching planning area GeoJSON data...")
    url = "https://www.onemap.gov.sg/api/public/popapi/getAllPlanningarea?year=2019"
    headers = {"Authorization": ACCESS_TOKEN}

    # Send request to API
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Planning area data successfully fetched.")
        return response.json()
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None
    
# 2. Save Planning Area Data to CSV
def save_planning_area_data(data):
    planning_area_data = []

    # Process JSON data and store planning area name and GeoJSON
    for area in data['SearchResults']:
        planning_area_name = area['pln_area_n'].lower()  
        geojson_data = area['geojson']  # Extract GeoJSON as a string
        planning_area_data.append({'pln_area_n': planning_area_name, 'geojson': geojson_data})
    
    # Convert list to DataFrame and save to CSV
    planning_area_location = pd.DataFrame(planning_area_data)
    planning_area_path = os.path.join(data_folder, "planning_area_geojson_data.csv")
    planning_area_location.to_csv(planning_area_path, index=False)
    print(f"Planning area data saved to {planning_area_path}.")

# Fetch and save the planning area data
planning_area_data = fetch_planning_area_data()
if planning_area_data:
    save_planning_area_data(planning_area_data)

# 1. Fetch Planning Area Data with GeoJSON
def fetch_planning_area_geojson():
    print("Fetching planning area GeoJSON data...")
    url = "https://www.onemap.gov.sg/api/public/popapi/getAllPlanningarea?year=2019"
    headers = {"Authorization": ACCESS_TOKEN}
    
    # Request data from the API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        planning_area_data = []

        # Extract each planning area name and GeoJSON
        for area in data['SearchResults']:
            planning_area_name = area['pln_area_n'].lower()  
            geojson_data = area['geojson']  # Extract GeoJSON as a string
            
            # Append to the list
            planning_area_data.append({
                'pln_area_n': planning_area_name,
                'geojson': geojson_data
            })
        
        # Convert list to DataFrame and save to CSV
        planning_area_location = pd.DataFrame(planning_area_data)
        planning_area_path = os.path.join(data_folder, "planning_area_geojson_data.csv")
        planning_area_location.to_csv(planning_area_path, index=False)
        print(f"Planning area data saved to {planning_area_path}.")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None
    
# Fetch all data
def fetch_all_data():
    fetch_bus_routes()
    fetch_bus_stops()
    fetch_passenger_volume_by_bus_stops()
    fetch_od_volume_by_bus_stops("202407")
    fetch_od_volume_by_bus_stops("202408")
    fetch_od_volume_by_bus_stops("202409")
    fetch_od_volume_by_train_stations()
    fetch_train_stn_geospatial_whole_island()
    fetch_train_stn_exit_geospatial_whole_island()
    fetch_bus_stop_geospatial_whole_island()
    fetch_mrt_line()
    fetch_bus_services()
    fetch_planning_area_names()
    fetch_population_data()
    fetch_planning_area_geojson()

# Execute the data fetching
fetch_all_data()
