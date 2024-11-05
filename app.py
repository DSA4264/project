import os
import json
from flask import Flask, render_template, request, jsonify
import folium
import geopandas as gpd
import pandas as pd
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
        return LineString()

def plot_bus_service_and_mrt_routes(service_no, gdf):
    """
    Plots the 'geometry' route and all MRT geometries for a given ServiceNo using Folium.

    Parameters:
    - service_no: str, the service number to search for
    - gdf: GeoDataFrame, contains the bus and MRT routes data

    Returns:
    - An HTML representation of the Folium map centered on the bus route or MRT geometry.
    """
    if service_no:
        # Filter the row with the given service number
        row = gdf[gdf['ServiceNo'] == service_no]

        if row.empty:
            print(f"No data found for ServiceNo: {service_no}")
            return None

        # Extract the bus route geometry (buffered)
        bus_route = row.iloc[0]['geometry']

        # Extract the MRT line geometries
        mrt_geoms = [
            row.iloc[0]['NS_MRT_geom'],
            row.iloc[0]['EW_MRT_geom'],
            row.iloc[0]['DT_MRT_geom'],
            row.iloc[0]['CC_MRT_geom'],
            row.iloc[0]['NE_MRT_geom'],
            row.iloc[0]['TE_MRT_geom']
        ]

        # Corresponding MRT line colors
        colors = [
            'red',         # NS Line
            'green',       # EW Line
            'darkblue',    # DT Line
            'yellow',      # CC Line
            'purple',      # NE Line
            'brown'        # TE Line
        ]

        # Center the map on the centroid of the bus route
        start_coords = [bus_route.centroid.y, bus_route.centroid.x]  # lat, lon

        # Create a Folium map centered on the bus route
        m = folium.Map(location=start_coords, zoom_start=13)

        # Plot the bus route in black
        folium.GeoJson(
            bus_route,
            name='Bus Route',
            style_function=lambda x: {'color': 'black', 'weight': 2, 'fillOpacity': 0.3}
        ).add_to(m)

        # Plot each MRT line geometry with the corresponding color
        for mrt_geom, color, name in zip(mrt_geoms, colors, [
            'NS Line', 'EW Line', 'DT Line', 'CC Line', 'NE Line', 'TE Line'
        ]):
            if mrt_geom and not mrt_geom.is_empty:
                folium.GeoJson(
                    mrt_geom,
                    name=name,
                    style_function=lambda x, color=color: {'color': color, 'weight': 2}
                ).add_to(m)
            else:
                print(f"No geometry found for {name}")

    else:
        # If no service number is provided, center the map on Singapore
        singapore_coords = [1.3521, 103.8198]
        m = folium.Map(location=singapore_coords, zoom_start=12)

        # Plot MRT lines
        line_colors = {
            'NS Line': 'red',
            'EW Line': 'green',
            'DT Line': 'darkblue',
            'CC Line': 'yellow',
            'NE Line': 'purple',
            'TE Line': 'brown'
        }

        for line_name, color in line_colors.items():
            geom_col = f"{line_name.split()[0]}_MRT_geom"
            mrt_geom = gdf.iloc[0][geom_col]
            if mrt_geom and not mrt_geom.is_empty:
                folium.GeoJson(
                    mrt_geom,
                    name=line_name,
                    style_function=lambda x, color=color: {'color': color, 'weight': 2}
                ).add_to(m)
            else:
                print(f"No geometry found for {line_name}")

    # Add a layer control to switch between routes
    folium.LayerControl().add_to(m)

    # Return the HTML representation of the map
    return m._repr_html_()
    
def get_overlap_messages(row):
    # Extract MRT overlap percentages
    mrt_overlap_percentages = {}
    for line in ['NS', 'EW', 'DT', 'CC', 'NE', 'TE']:
        overlap_col = f"{line}_MRT_geom_overlap"
        percentage = row.get(overlap_col, 0) if pd.notnull(row.get(overlap_col)) else 0
        mrt_overlap_percentages[f"{line} Line"] = percentage

    # Get top 2 MRT line overlaps
    top_mrt_lines = sorted(
        mrt_overlap_percentages.items(),
        key=lambda x: x[1],
        reverse=True
    )[:2]

    # Build MRT overlap messages
    mrt_overlap_messages = []
    for line, percentage in top_mrt_lines:
        if percentage > 40:
            overlap_text = f"{line}: {percentage:.2f}% overlap - Very overlapped."
        elif percentage < 10:
            overlap_text = f"{line}: {percentage:.2f}% overlap - Not overlapped."
        else:
            overlap_text = f"{line}: {percentage:.2f}% overlap - Quite overlapped."
        mrt_overlap_messages.append(overlap_text)

    # Collect alternative bus routes
    alt_bus_routes = []
    for i in range(1, 4):
        alternative_bus = row.get(f'Top_{i}_Alternative_Bus', None)
        overlap_percentage = row.get(f'Top_{i}_Overlap_Percentage', None)
        if pd.notnull(alternative_bus) and pd.notnull(overlap_percentage):
            alt_bus_routes.append(f"Bus {alternative_bus} with an overlap of {overlap_percentage:.2f}%")

    return mrt_overlap_messages, alt_bus_routes

def get_bus_category(row):
    # Updated function to handle NaN values
    if 'Category' in row.index and pd.notnull(row['Category']):
        return row['Category']
    else:
        return 'Unknown'

# Load GeoDataFrame and model data
file_path = 'data/buffered_bus_mrt_combined_gdf.pkl'
with open(file_path, 'rb') as f:
    bus_mrt_combined_gdf = pickle.load(f)

# Rename 'buffered_bus_route_geom' to 'geometry' for consistency
bus_mrt_combined_gdf.rename(columns={'buffered_bus_route_geom': 'geometry'}, inplace=True)

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

# Load additional overlap data and merge
bus_overlap_df = pd.read_csv('data/all_bus_overlaps.csv')
model_df = pd.read_csv('data/model_df.csv')
model_df['ServiceNo'] = model_df['ServiceNo'].astype(str)
final_df = model_df.merge(
    bus_overlap_df,
    on='ServiceNo',
    how='left'
)

bus_mrt_combined_gdf = bus_mrt_combined_gdf.merge(
    final_df,
    on='ServiceNo',
    how='left',
    suffixes=('', '_overlap')
)

# Save the combined DataFrame for debugging (optional)
# bus_mrt_combined_gdf.to_csv('data/bus_mrt_combined_gdf.csv', index=False)

@app.route('/', methods=['GET'])
def index():
    sections = [
        {"id": "section1", "image": "image1.png", "text": "This is a map of Singapore."},
        {"id": "section2", "image": "image2.png", "text": "Using data obtained from LTA and OneMapAPI, we mapped out MRT lines in Singapore."},
        {"id": "section3", "image": "image3.png", "text": "We then mapped out all the bus routes in Singapore and then buffered."},
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

    default_map = plot_bus_service_and_mrt_routes(service_no=None, gdf=bus_mrt_combined_gdf)

    return render_template(
        'scrollytelling.html',
        sections=sections,
        main_story_content=main_story_content,
        bus_route_map=default_map
    )

@app.route('/get_bus_route', methods=['POST'])
def get_bus_route():
    data = request.get_json()
    service_no = data.get('service_no').strip()
    row_df = bus_mrt_combined_gdf[bus_mrt_combined_gdf['ServiceNo'] == service_no]

    if row_df.empty:
        response = {
            'error_message': f"No data found for Bus Service No: {service_no}",
            'bus_route_map': '',
            'service_no': service_no
        }
    else:
        row = row_df.iloc[0]
        bus_route_map = plot_bus_service_and_mrt_routes(service_no, bus_mrt_combined_gdf)
        mrt_overlap_messages, alt_bus_routes = get_overlap_messages(row)
        bus_category = get_bus_category(row)

        response = {
            'error_message': None,
            'bus_route_map': bus_route_map,
            'service_no': service_no,
            'Category': bus_category,
            'mrt_overlap_messages': mrt_overlap_messages,
            'alt_bus_routes': alt_bus_routes
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
