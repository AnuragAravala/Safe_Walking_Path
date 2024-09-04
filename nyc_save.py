import osmnx as ox

# Define the area
place_name = "New York City, New York, USA"

# Fetch the street network data for the entire NYC area
graph = ox.graph_from_place(place_name, network_type='walk')

# Save the graph to a GraphML file
ox.save_graphml(graph, "nyc_walk.graphml")
