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
    """
    row = gdf[gdf['ServiceNo'] == service_no]
    if row.empty:
        print(f"No data found for ServiceNo: {service_no}")
        return None

    bus_route = row.iloc[0]['geometry']
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

    colors = [
        'red', 'green', 'darkblue', 'yellow', 'purple', 'brown', 'lightgreen', 'orange'
    ]
    mrt_names = [
        'NS Line', 'EW Line', 'DT Line', 'CC Line', 'NE Line', 'TE Line', 'CG Line', 'CE Line'
    ]

    start_coords = [1.3521, 103.8198]  # Default to Singapore coordinates
    m = folium.Map(location=start_coords, zoom_start=13)

    if bus_route and not bus_route.is_empty and bus_route.is_valid:
        folium.GeoJson(
            bus_route,
            name='Bus Route',
            style_function=lambda x: {'color': 'black', 'weight': 3}
        ).add_to(m)

    for mrt_geom, color, name in zip(mrt_geoms, colors, mrt_names):
        if mrt_geom and not mrt_geom.is_empty and mrt_geom.is_valid:
            folium.GeoJson(
                mrt_geom,
                name=name,
                style_function=lambda x, color=color: {'color': color, 'weight': 2}
            ).add_to(m)

    folium.LayerControl().add_to(m)
    return m._repr_html_()

# Load the GeoDataFrame with bus and MRT routes
bus_mrt_combined_gdf = gpd.read_file('data/bus_mrt_combined.geojson')

geom_columns = [
    'geometry', 'NS_MRT_geom', 'EW_MRT_geom', 'DT_MRT_geom', 'CC_MRT_geom',
    'NE_MRT_geom', 'TE_MRT_geom', 'CG_MRT_geom', 'CE_MRT_geom'
]

for col in geom_columns:
    if bus_mrt_combined_gdf[col].dtype == 'object':
        first_value = bus_mrt_combined_gdf[col].dropna().iloc[0]
        if isinstance(first_value, str):
            bus_mrt_combined_gdf[col] = bus_mrt_combined_gdf[col].apply(wkt.loads)

bus_mrt_combined_gdf['ServiceNo'] = bus_mrt_combined_gdf['ServiceNo'].astype(str)

@app.route('/', methods=['GET'])
def index():
    sections = [
        {"id": "section1", "image": "image1.png", "text": "This is a map of Singapore."},
        {"id": "section2", "image": "image2.png", "text": "Using data obtained from LTA and Wikipedia..."},
        {"id": "section3", "image": "image3.png", "text": "Text."},
        {"id": "section4", "image": "image4.png", "text": "Test."},
        {"id": "section5", "image": "image5.png", "text": "Text"},
        {"id": "section6", "image": "image6.png", "text": "Text."},
        # additional sections
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

    return render_template('scrollytelling.html', sections=sections, main_story_content=main_story_content)

@app.route('/get_bus_route', methods=['POST'])
def get_bus_route():
    data = request.get_json()
    service_no = data.get('service_no')
    bus_route_map = None
    error_message = None

    if not service_no:
        error_message = "Please enter a bus service number."
    else:
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
