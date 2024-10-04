import os
import pandas as pd
import zipfile

# Define the path to your 'data' folder
data_folder = "data"

# 1. Load bus routes data from CSV file
def load_bus_routes_data():
    bus_routes_path = os.path.join(data_folder, "bus_routes_data.csv")
    if os.path.exists(bus_routes_path):
        bus_routes_df = pd.read_csv(bus_routes_path)  # Use read_csv
        print("Bus Routes Data Loaded:")
        print(bus_routes_df.head())  # Show the first few rows
        return bus_routes_df
    else:
        print(f"Error: {bus_routes_path} not found.")
        return None

# 2. Load bus stops data from CSV file
def load_bus_stops_data():
    bus_stops_path = os.path.join(data_folder, "bus_stops_data.csv")
    if os.path.exists(bus_stops_path):
        bus_stops_df = pd.read_csv(bus_stops_path)  # Use read_csv
        print("Bus Stops Data Loaded:")
        print(bus_stops_df.head())  # Show the first few rows
        return bus_stops_df
    else:
        print(f"Error: {bus_stops_path} not found.")
        return None

# 3. Load Passenger Volume by Bus Stops data from ZIP file
def load_passenger_volume_bus_stops():
    zip_path = os.path.join(data_folder, "transport_node_bus_202408.zip")
    csv_file_name = "transport_node_bus_202408.csv"
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open(csv_file_name) as csv_file:
                passenger_volume_df = pd.read_csv(csv_file)
                print("Passenger Volume by Bus Stops Data Loaded:")
                print(passenger_volume_df.head())  # Show the first few rows
                return passenger_volume_df
    else:
        print(f"Error: {zip_path} not found.")
        return None

# 4. Load Origin-Destination Bus Stops data from ZIP file
def load_od_volume_bus_stops():
    zip_path = os.path.join(data_folder, "origin_destination_bus_202408.zip")
    csv_file_name = "origin_destination_bus_202408.csv"
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open(csv_file_name) as csv_file:
                od_volume_df = pd.read_csv(csv_file)
                print("Origin-Destination Bus Stops Data Loaded:")
                print(od_volume_df.head())  # Show the first few rows
                return od_volume_df
    else:
        print(f"Error: {zip_path} not found.")
        return None

# Main function to load all files and assign to DataFrame variables
def main():
    print("Loading data files from the 'data' folder...\n")
    
    # Load Bus Routes Data into bus_routes_df
    bus_routes_df = load_bus_routes_data()
    
    # Load Bus Stops Data into bus_stops_df
    bus_stops_df = load_bus_stops_data()
    
    # Load Passenger Volume by Bus Stops Data into passenger_volume_df
    passenger_volume_df = load_passenger_volume_bus_stops()
    
    # Load Origin-Destination Bus Stops Data into od_volume_df
    od_volume_df = load_od_volume_bus_stops()

    # You can now use these DataFrames for further processing
    if bus_routes_df is not None:
        print(f"Bus Routes DataFrame shape: {bus_routes_df.shape}")
    if bus_stops_df is not None:
        print(f"Bus Stops DataFrame shape: {bus_stops_df.shape}")
    if passenger_volume_df is not None:
        print(f"Passenger Volume DataFrame shape: {passenger_volume_df.shape}")
    if od_volume_df is not None:
        print(f"OD Bus Stops DataFrame shape: {od_volume_df.shape}")

if __name__ == "__main__":
    main()
