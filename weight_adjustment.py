import pandas as pd
import osmnx as ox
from tqdm import tqdm

# Load the CSV data
grouped_data = pd.read_csv('grouped_data2.csv')
print("got here")
# Load the pre-saved graph data
graph = ox.load_graphml('nyc_walk.graphml')
print("got here")
# Simplified safety score function
def safety_score_function(lat, lon, month_segment, grouped_data):
    # Match data by exact latitude, longitude, and month_segment
    matching_data = grouped_data[
        (grouped_data['Rounded_Latitude'] == lat) &
        (grouped_data['Rounded_Longitude'] == lon) &
        (grouped_data['Month_Segment'] == month_segment)
    ]
    
    if matching_data.empty:
        return 1  # Default safety score if no exact match is found

    # Use the count directly as the safety score
    safety_score = matching_data['Count'].values[0]
    
    # Convert count to a safety score (lower count -> higher safety)
    safety_score = max(1 / (safety_score + 1), 0.1)  # Avoid division by zero
    
    return safety_score

# Focus on the "Sep-Oct" month segment
month_segment = 'Sep-Oct'

# Create a dictionary to store node safety scores for the "Sep-Oct" month segment
node_safety_scores = {}

# Calculate safety scores for each node for the "Sep-Oct" month segment
print("Calculating node safety scores...")
for node, data in tqdm(graph.nodes(data=True), desc="Nodes"):
    # Calculate the safety score based on the location and current month segment
    lat = round(data['y'], 4)
    lon = round(data['x'], 4)
    safety_score = safety_score_function(lat, lon, month_segment, grouped_data)
    node_safety_scores[node] = safety_score

# Apply safety scores to edge weights for the "Sep-Oct" month segment
print("Adjusting edge weights based on safety scores...")
for u, v, data in tqdm(graph.edges(data=True), desc="Edges"):
    # Ensure the 'length' attribute is a float
    length = float(data.get('length', 0))  # Default to 0 if 'length' is not found

    # Get the safety score for the node 'u' and ensure it is a float
    safety_score = float(node_safety_scores.get(u, 1))  # Default to 1 if not found

    # Adjust the edge weight by multiplying length by safety score
    data['safety'] = length * safety_score
    
# Save the graph to a GraphML file
ox.save_graphml(graph, "nyc_walk_with_sept_oct_safety.graphml")

print("Process completed successfully!")
