from flask import Flask, render_template, request, jsonify
import osmnx as ox
import networkx as nx
import folium
import numpy as np
from folium.plugins import MeasureControl
import os
import pandas as pd
import pickle

start_coords = (40.7128, -74.0060)

# Create a map centered around the central point
m = folium.Map(location=start_coords, zoom_start=11, tiles='cartodbpositron')
locations_df = pd.read_csv('unique_locations_sorted.csv')

for _, row in locations_df.iterrows():
    folium.Circle(
        location=(row['Latitude'], row['Longitude']),
        radius=20,  # Radius in meters
        color='yellow',
        fill=True
    ).add_to(m)

# Add a measure control to the map
measure_control = MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres')
m.add_child(measure_control)

# # Serialize the map object using pickle
# with open('static/base_map.pkl', 'wb') as f:
#     pickle.dump(m, f)

map_path = os.path.join('static', 'base_map.html')
m.save(map_path)