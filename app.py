from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import dotenv_values
import os
import osmnx as ox
import networkx as nx
import folium
import numpy as np
from folium.plugins import MeasureControl
from twilio.rest import Client
import speech_recognition as sr

app = Flask(__name__)

app.secret_key = 'ayushe'
config = dotenv_values()
graph = ox.load_graphml("nyc_walk_with_sept_oct_safety.graphml")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/map', methods=['GET'])
def map_view():
    # path_finding()
    return render_template('map.html', api_key=config['GOOGLE_PLACES_API_KEY']) 

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    start_lat, start_lon = data['start']
    end_lat, end_lon = data['end']

    print("got here")
    # Find the nearest nodes to the start and end points
    start_node = ox.distance.nearest_nodes(graph, X=start_lon, Y=start_lat)
    end_node = ox.distance.nearest_nodes(graph, X=end_lon, Y=end_lat)

    # Find the shortest path using the A* algorithm
    route = nx.astar_path(graph, start_node, end_node, heuristic=None, weight='length')

    # Extract the latitude and longitude for each node in the route
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]
    print("route coords")
    print(route_coords)
    return jsonify({'route_coords': route_coords})


def path_finding():
    # Get the start and end coordinates from the query parameters
    try:
        start_lat = float(request.args.get('start_lat'))
        start_lon = float(request.args.get('start_lon'))
        end_lat = float(request.args.get('end_lat'))
        end_lon = float(request.args.get('end_lon'))

        start_coords = (start_lat, start_lon)
        end_coords = (end_lat, end_lon)
    
    except:
        start_coords = (40.7128, -74.0060)  # Default to example coordinates in NYC
        end_coords = (40.730610, -73.935242)
        return 

    # Create a map centered around the start point
    m = folium.Map(location=start_coords, zoom_start=12)

    
    # Add markers for start and end points
    folium.Marker(start_coords, popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, popup="End", icon=folium.Icon(color='red')).add_to(m)

    start_node = ox.distance.nearest_nodes(graph, X=start_coords[1], Y=start_coords[0])
    end_node = ox.distance.nearest_nodes(graph, X=end_coords[1], Y=end_coords[0])

    # Calculate the shortest path
    route = nx.shortest_path(graph, start_node, end_node, weight='length')
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

    # Add the route as a PolyLine on the map
    folium.PolyLine(route_coords, color="blue", weight=15.5, opacity=1).add_to(m)

    # Add a measure control to the map
    measure_control = MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres')
    m.add_child(measure_control)

    # Save the map as an HTML file in the static directory
    map_path = os.path.join('static', 'map1.html')
    m.save(map_path)

@app.route('/emergency_calls', methods=['GET', 'POST'])
def emergency_calls():
    return render_template('emergency_calls.html')

@app.route('/set_safe_word', methods=['POST'])
def set_safe_word():
    session['safe_word'] = request.form['safe_word']
    session['phone_number'] = request.form['phone_number']
    listen_for_safe_word()
    return redirect(url_for('index'))

def listen_for_safe_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Listening for the safe word...")
        audio = recognizer.listen(source)
    
    try:
        transcript = recognizer.recognize_google(audio)
        if session.get('safe_word') and session['safe_word'].lower() in transcript.lower():
            trigger_emergency_call()
            print("trigger word detected--emergency call initiated")
        else:
            print("Safe word not detected.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")

def trigger_emergency_call():
    phone_number = session.get('phone_number')
    if phone_number:
        print(f"Emergency call triggered to {phone_number}!")
        #actual call logic using Twilio API
        client = Client(config['TWILIO_ACCOUNT_SID'], config['TWILIO_AUTH_TOKEN'])
        call = client.calls.create(
            url = "http://demo.twilio.com/docs/voice.xml",
            to = phone_number,
            from_ = config['TWILIO_PHONE_NUMBER']
        )
    else:
        print("Phone number not found!")

if __name__ == '__main__':
    app.run(debug=True)