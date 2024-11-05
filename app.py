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
    singapore_coords = [1.3521, 103.8198]
    m = folium.Map(location=singapore_coords, zoom_start=12)

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

    if service_no:
        row = gdf[gdf['ServiceNo'] == service_no]
        if not row.empty:
            bus_route = row.iloc[0]['geometry']
            if bus_route and not bus_route.is_empty:
                start_coords = [bus_route.coords[0][1], bus_route.coords[0][0]]
                m.location = start_coords
                m.zoom_start = 13
                folium.GeoJson(
                    bus_route,
                    name='Bus Route',
                    style_function=lambda x: {'color': 'black', 'weight': 3}
                ).add_to(m)
        else:
            print(f"No data found for ServiceNo: {service_no}")

    folium.LayerControl().add_to(m)
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
    overlap_messages = []
    for line, percentage in top_mrt_lines:
        if percentage > 40:
            overlap_text = f"{line}: {percentage:.2f}% overlap - Very overlapped."
        elif percentage < 10:
            overlap_text = f"{line}: {percentage:.2f}% overlap - Not overlapped."
        else:
            overlap_text = f"{line}: {percentage:.2f}% overlap - Quite overlapped."
        overlap_messages.append(overlap_text)

    # Add top alternative bus routes and their overlap percentages
    for i in range(1, 4):
        alternative_bus = row.get(f'Top_{i}_Alternative_Bus', None)
        overlap_percentage = row.get(f'Top_{i}_Overlap_Percentage', None)
        if pd.notnull(alternative_bus) and pd.notnull(overlap_percentage):
            alt_message = f"We also determined that an alternative route is Bus {alternative_bus} with an overlap of {overlap_percentage:.2f}%."
            overlap_messages.append(alt_message)

    return overlap_messages

def get_bus_category(row):
    # Updated function to handle NaN values
    if 'Category' in row.index and pd.notnull(row['Category']):
        return row['Category']
    else:
        return 'Unknown'
# Load GeoDataFrame and model data
file_path = 'data/bus_mrt_combined_gdf.pkl'
with open(file_path, 'rb') as f:
    bus_mrt_combined_gdf = pickle.load(f)

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

bus_mrt_combined_gdf['geometry'] = bus_mrt_combined_gdf['geometry'].apply(multiline_to_single_line)


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

bus_mrt_combined_gdf.to_csv('data/bus_mrt_combined_gdf.csv', index=False)

@app.route('/', methods=['GET'])
def index():
    sections = [
        {"id": "section1", "image": "image1.png", "text": "This is a map of Singapore."},
        {"id": "section2", "image": "image2.png", "text": "Using data obtained from LTA and Wikipedia..."},
        {"id": "section3", "image": "image3.png", "text": "Text."},
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
    row = bus_mrt_combined_gdf[bus_mrt_combined_gdf['ServiceNo'] == service_no].iloc[0] if not bus_mrt_combined_gdf[bus_mrt_combined_gdf['ServiceNo'] == service_no].empty else None

    if row is None:
        response = {
            'error_message': f"No data found for Bus Service No: {service_no}",
            'bus_route_map': '',
            'service_no': service_no
        }
    else:
        bus_route_map = plot_bus_service_and_mrt_routes(service_no, bus_mrt_combined_gdf)
        overlap_messages = get_overlap_messages(row)
        bus_category = get_bus_category(row)

        response = {
            'error_message': None,
            'bus_route_map': bus_route_map,
            'service_no': service_no,
            'Category': bus_category,
            'overlap_messages': overlap_messages
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
