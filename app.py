import os
import json
from flask import Flask, render_template, request, jsonify
import folium
import geopandas as gpd
from shapely import wkt
from shapely.geometry import LineString, MultiLineString, Point
from typing import Union
import pickle

app = Flask(__name__)

def multiline_to_single_line(geometry: Union[LineString, MultiLineString]) -> LineString:
    if isinstance(geometry, LineString):
        return geometry
    elif isinstance(geometry, MultiLineString):
        coords = []
        for line in geometry.geoms:
            coords.extend(line.coords)
        return LineString(coords)
    else:
        # Handle other geometry types if necessary
        return LineString()


def plot_bus_service_and_mrt_routes(service_no, gdf):
    """
    Plots the MRT lines and the bus route for a given ServiceNo (if available) using Folium.

    Parameters:
    - service_no: str, the service number to search for
    - gdf: GeoDataFrame, contains the bus and MRT routes data
    
    Returns:
    - A Folium map centered on Singapore, with MRT lines always displayed
      and the bus route displayed if a valid service number is provided.
    """
    # Center the map on Singapore (or adjust coordinates as needed)
    singapore_coords = [1.3521, 103.8198]
    m = folium.Map(location=singapore_coords, zoom_start=12)

    # Plot MRT lines with corresponding colors
    colors = [
        'red',         # NS Line
        'green',       # EW Line
        'darkblue',    # DT Line
        'yellow',      # CC Line
        'purple',      # NE Line
        'brown'        # TE Line
    ]
    mrt_geoms = [
        gdf.iloc[0]['NS_MRT_geom'],
        gdf.iloc[0]['EW_MRT_geom'],
        gdf.iloc[0]['DT_MRT_geom'],
        gdf.iloc[0]['CC_MRT_geom'],
        gdf.iloc[0]['NE_MRT_geom'],
        gdf.iloc[0]['TE_MRT_geom']
    ]
    
    for mrt_geom, color, name in zip(mrt_geoms, colors, [
        'NS Line', 'EW Line', 'DT Line', 'CC Line', 'NE Line', 'TE Line'
    ]):
        folium.GeoJson(
            mrt_geom,
            name=name,
            style_function=lambda x, color=color: {'color': color, 'weight': 2}
        ).add_to(m)
    
    # If a valid service number is provided, attempt to plot the bus route
    if service_no:
        row = gdf[gdf['ServiceNo'] == service_no]
        
        if not row.empty:
            bus_route = row.iloc[0]['geometry']
            
            # Center map on the bus route's starting point
            start_coords = [bus_route.coords[0][1], bus_route.coords[0][0]]
            m.location = start_coords
            m.zoom_start = 13  # Zoom in to focus on the route
            
            # Plot the bus route in black
            folium.GeoJson(
                bus_route,
                name='Bus Route',
                style_function=lambda x: {'color': 'black', 'weight': 3}
            ).add_to(m)
        else:
            print(f"No data found for ServiceNo: {service_no}")

    # Add a layer control to toggle visibility of each line
    folium.LayerControl().add_to(m)
    
    return m._repr_html_()

# Load the GeoDataFrame with bus and MRT routes
file_path = 'data/bus_mrt_combined_gdf.pkl'
with open(file_path, 'rb') as f:
    bus_mrt_combined_gdf = pickle.load(f)

# Ensure geometry columns are properly loaded
geom_columns = [
    'geometry', 'NS_MRT_geom', 'EW_MRT_geom', 'DT_MRT_geom', 'CC_MRT_geom',
    'NE_MRT_geom', 'TE_MRT_geom'
]

for col in geom_columns:
    if bus_mrt_combined_gdf[col].dtype == 'object':
        first_value = bus_mrt_combined_gdf[col].dropna().iloc[0]
        if isinstance(first_value, str):
            bus_mrt_combined_gdf[col] = bus_mrt_combined_gdf[col].apply(wkt.loads)

bus_mrt_combined_gdf['ServiceNo'] = bus_mrt_combined_gdf['ServiceNo'].astype(str)

# Apply the multiline_to_single_line function to the geometry column
bus_mrt_combined_gdf['geometry'] = bus_mrt_combined_gdf['geometry'].apply(multiline_to_single_line)


@app.route('/', methods=['GET'])
def index():
    sections = [
        {"id": "section1", "image": "image1.png", "text": "This is a map of Singapore."},
        {"id": "section2", "image": "image2.png", "text": "Using data obtained from LTA and Wikipedia..."},
        {"id": "section3", "image": "image3.png", "text": "Text."},  # additional sections
    ]

    main_story_content = {
        "heading": "Explanation of results",
        "text": "Based on your bus route selection, we figured out that xxxx",
        "sections": [
            {
                "subheading": "SH1",
                "description": "Explanation 1."
            }
        ]
    }

    # Generate the default map with MRT lines only
    default_map = plot_bus_service_and_mrt_routes(service_no=None, gdf=bus_mrt_combined_gdf)

    return render_template(
        'scrollytelling.html',
        sections=sections,
        main_story_content=main_story_content,
        bus_route_map=default_map  # Pass the default map to the template
    )

@app.route('/get_bus_route', methods=['POST'])
def get_bus_route():
    data = request.get_json()
    service_no = data.get('service_no')
    bus_route_map = plot_bus_service_and_mrt_routes(service_no, bus_mrt_combined_gdf)
    
    if bus_route_map is None:
        error_message = f"No data found for Bus Service No: {service_no}"
    else:
        error_message = None

    response = {
        'error_message': error_message,
        'bus_route_map': bus_route_map,
        'service_no': service_no
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
