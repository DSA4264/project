from flask import Flask, render_template, request, jsonify
import folium
import pandas as pd
from shapely import wkt
import pickle

app = Flask(__name__)

def plot_bus_service_and_mrt_routes(service_no, gdf, alternative_service_no=None):
    """
    Plots the bus routes and MRT lines for a given ServiceNo using Folium.

    Parameters:
    - service_no: str, the main bus service number to plot.
    - gdf: GeoDataFrame, contains the bus and MRT routes data.
    - alternative_service_no: str, optional, the alternative bus service number to plot, alternate service will be used in the main html plot.

    Returns:
    - An HTML representation of the Folium map.
    """
    # Initialize the map centered on Singapore
    singapore_coords = [1.3521, 103.8198]
    m = folium.Map(location=singapore_coords, zoom_start=12, control_scale=True)

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

    # Plot main bus route
    if service_no:
        row = gdf[gdf['ServiceNo'] == service_no]
        if not row.empty:
            bus_route = row.iloc[0]['geometry']
            if bus_route and not bus_route.is_empty:
                # Center the map on the bus route
                m.location = [bus_route.centroid.y, bus_route.centroid.x]
                m.zoom_start = 13
                route_name = f"Main Bus Route: {service_no}"
                main_bus_route_fg = folium.FeatureGroup(name=route_name, overlay=True, control=True)
                folium.GeoJson(
                    bus_route,
                    name=route_name,
                    style_function=lambda x: {'color': 'black', 'weight': 3}
                ).add_to(main_bus_route_fg)
                main_bus_route_fg.add_to(m)
        else:
            print(f"No data found for ServiceNo: {service_no}")

    # Plot alternative bus route
    if alternative_service_no:
        alt_row = gdf[gdf['ServiceNo'] == alternative_service_no]
        if not alt_row.empty:
            alt_bus_route = alt_row.iloc[0]['geometry']
            if alt_bus_route and not alt_bus_route.is_empty:
                alt_route_name = f"Alternate Bus Route: {alternative_service_no}"
                alternative_bus_route_fg = folium.FeatureGroup(name=alt_route_name, overlay=True, control=True)
                folium.GeoJson(
                    alt_bus_route,
                    name=alt_route_name,
                    style_function=lambda x: {'color': 'blue', 'weight': 3, 'dashArray': '5, 5'}
                ).add_to(alternative_bus_route_fg)
                alternative_bus_route_fg.add_to(m)
        else:
            print(f"No data found for Alternative ServiceNo: {alternative_service_no}")

    # Add Layer Control
    folium.LayerControl(collapsed=False).add_to(m)

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
    # This is read in from our csv file
    alt_bus_routes = []
    for i in range(1, 4):
        alternative_bus = row.get(f'Top_{i}_Alternative_Bus', None)
        overlap_percentage = row.get(f'Top_{i}_Overlap_Percentage', None)
        if pd.notnull(alternative_bus) and pd.notnull(overlap_percentage):
            alt_bus_routes.append(f"Bus {alternative_bus} with an overlap of {overlap_percentage:.2f}%")

    return mrt_overlap_messages, alt_bus_routes

# Used to pull the data to read category
def get_bus_category(row):
    # Updated function to handle NaN values
    if 'Category' in row.index and pd.notnull(row['Category']):
        return row['Category']
    else:
        return 'UNDEFINED'

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
        {"id": "section2", "image": "image2.png", "text": "Using data obtained from LTA and OneMapAPI, we mapped out MRT lines in Singapore. The buffered the MRT lines by 400m."},
        {"id": "section3", "image": "image3.png", "text": "We then mapped out all the bus routes in Singapore and then buffered it by 400m."},
    ]
    # Not in use now, but when we have time, we can do a full webpage write up of our findings using scrollytelling.
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
    # Render the default map with no bus line first. Only showing the buffered MRT Lines
    default_map = plot_bus_service_and_mrt_routes(service_no=None, gdf=bus_mrt_combined_gdf)

    return render_template(
        'scrollytelling.html',
        sections=sections,
        main_story_content=main_story_content,
        bus_route_map=default_map
    )

@app.route('/get_bus_route', methods=['POST'])
def get_bus_route():
    """
    Plots the bus routes and MRT lines for a given ServiceNo using Folium.

    Parameters:
    - No input
    
    Returns:
    - A jsonified response.
    - Also includes the alternate bus plot
    """

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
        bus_category = get_bus_category(row)
        mrt_overlap_messages, alt_bus_routes = get_overlap_messages(row)

        # Get the first alternative bus service number
        # This is the most overlapped service
        alternative_service_no = row.get('Top_1_Alternative_Bus', None)
        if pd.notnull(alternative_service_no):
            alternative_service_no = str(alternative_service_no)  # Ensure it's a string
        else:
            alternative_service_no = None

        bus_route_map = plot_bus_service_and_mrt_routes(service_no, bus_mrt_combined_gdf, alternative_service_no)

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
