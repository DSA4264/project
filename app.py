import os
import json
from flask import Flask, render_template, request, jsonify
import folium
import geopandas as gpd
from shapely import wkt

app = Flask(__name__)

def plot_bus_service_and_mrt_routes(service_no, gdf):
    """
    Plots the 'geometry' route and all MRT geometries for a given ServiceNo using Folium.

    Parameters:
    - service_no: str, the service number to search for
    - gdf: GeoDataFrame, contains the bus and MRT routes data

    Returns:
    - A Folium map HTML representation centered on the bus route or MRT geometry.
    """
    # Filter the row with the given service number
    row = gdf[gdf['ServiceNo'] == service_no]

    if row.empty:
        print(f"No data found for ServiceNo: {service_no}")
        return None

    # Extract the bus route geometry
    bus_route = row.iloc[0]['geometry']

    # Extract the MRT line geometries
    mrt_geoms = [
        row.iloc[0]['NS_MRT_geom'],
        row.iloc[0]['EW_MRT_geom'],
        row.iloc[0]['DT_MRT_geom'],
        row.iloc[0]['CC_MRT_geom'],
        row.iloc[0]['NE_MRT_geom'],
        row.iloc[0]['TE_MRT_geom'],
        row.iloc[0]['CG_MRT_geom'],
        row.iloc[0]['CE_MRT_geom']
    ]

    # Corresponding MRT line colors
    colors = [
        'red',         # NS Line
        'green',       # EW Line
        'darkblue',    # DT Line
        'yellow',      # CC Line
        'purple',      # NE Line
        'brown',       # TE Line
        'lightgreen',  # CG Line
        'orange'       # CE Line
    ]

    mrt_names = [
        'NS Line', 'EW Line', 'DT Line', 'CC Line',
        'NE Line', 'TE Line', 'CG Line', 'CE Line'
    ]

    # Center the map on the first point of the bus route or MRT geometry
    if bus_route and not bus_route.is_empty and bus_route.is_valid:
        # Get the coordinates of the first point
        if bus_route.geom_type == 'MultiLineString':
            coords = list(bus_route.geoms[0].coords)
        else:
            coords = list(bus_route.coords)
        start_coords = [coords[0][1], coords[0][0]]  # lat, lon
    else:
        print(f"Invalid bus route geometry for ServiceNo: {service_no}")
        start_coords = [1.3521, 103.8198]  # Default to Singapore coordinates

    # Create a Folium map centered on the bus route
    m = folium.Map(location=start_coords, zoom_start=13)

    # Plot the bus route in black
    if bus_route and not bus_route.is_empty and bus_route.is_valid:
        folium.GeoJson(
            bus_route,
            name='Bus Route',
            style_function=lambda x: {'color': 'black', 'weight': 3}
        ).add_to(m)
    else:
        print(f"Bus route geometry is invalid or empty for ServiceNo: {service_no}")

    # Plot each MRT line geometry with the corresponding color
    for mrt_geom, color, name in zip(mrt_geoms, colors, mrt_names):
        if mrt_geom and not mrt_geom.is_empty and mrt_geom.is_valid:
            folium.GeoJson(
                mrt_geom,
                name=name,
                style_function=lambda x, color=color: {'color': color, 'weight': 2}
            ).add_to(m)
        else:
            print(f"MRT geometry {name} is invalid or empty.")

    # Add a layer control to switch between routes
    folium.LayerControl().add_to(m)

    # Return the map HTML representation
    return m._repr_html_()

# Load the GeoDataFrame with bus and MRT routes
bus_mrt_combined_gdf = gpd.read_file('data/bus_mrt_combined.geojson')

# Convert WKT strings to Shapely geometry objects if necessary
geom_columns = [
    'geometry',
    'NS_MRT_geom',
    'EW_MRT_geom',
    'DT_MRT_geom',
    'CC_MRT_geom',
    'NE_MRT_geom',
    'TE_MRT_geom',
    'CG_MRT_geom',
    'CE_MRT_geom'
]

for col in geom_columns:
    if bus_mrt_combined_gdf[col].dtype == 'object':
        # Check if the first non-null value is a string
        first_value = bus_mrt_combined_gdf[col].dropna().iloc[0]
        if isinstance(first_value, str):
            bus_mrt_combined_gdf[col] = bus_mrt_combined_gdf[col].apply(wkt.loads)

# Ensure that 'ServiceNo' is a string
bus_mrt_combined_gdf['ServiceNo'] = bus_mrt_combined_gdf['ServiceNo'].astype(str)

@app.route('/', methods=['GET'])
def index():
    # Sections data for scrollytelling
    sections = [
        {"id": "section1", 
         "image": "image1.png", 
         "text": "This is a map of Singapore."},
        {"id": "section2", 
         "image": "image2.png", 
         "text": "Using data obtianed from LTA and Wikipedia, we plotted all the current and future MRT lines in Singapore. This includes the oldest MRT line in Singapore, the North-South Line (NSL), and the incomplete Thomson-East Coast Line (TEL)."},
        {"id": "section3", 
         "image": "image3.png", 
         "text": "We then ran our polygon encodong algorithm and mapped out every single bus route in Singapore. As you can tell, our bus routes are very complex and cover a large area of Singapore."},
        {"id": "section4",
         "image": "image4.png",
         "text": "On Nov 17 2024, LTA announced that bus service '167' will cease operations, as 'ridership for some bus services (including 167) along segments of the Thomson-East Coast Line (TEL) has fallen by around 30 per cent to 40 per cent'."},
        {"id": "section5",
         "image": "image5.png",
         "text": "This was met by a huge backlash from the public, with many people complaining that they will have to take a longer route to work. This is because the bus service '167' is the one of the few bus service that connects the residents living in the north to the CBD directly."},
        {"id": "section6",
         "image": "image6.png",
         "text": "This is a map of the bus route '167' and the MRT lines that it connects to. As you can see, the bus route '167' connects to the North-South Line (NSL), the Downtown Line (DTL), and the future Thomson-East Coast Line (TEL)."},
    ]
    return render_template('scrollytelling.html', sections=sections)

@app.route('/get_bus_route', methods=['POST'])
def get_bus_route():
    data = request.get_json()
    service_no = data.get('service_no')
    bus_route_map = None
    error_message = None

    if not service_no:
        error_message = "Please enter a bus service number."
    else:
        # Call the function to get the map HTML
        bus_route_map = plot_bus_service_and_mrt_routes(service_no, bus_mrt_combined_gdf)
        if bus_route_map is None:
            error_message = f"No data found for Bus Service No: {service_no}"

    response = {
        'error_message': error_message,
        'bus_route_map': bus_route_map,
        'service_no': service_no
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

