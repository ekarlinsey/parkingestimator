from flask import Flask, render_template, request, jsonify
from shapely.geometry import Polygon
import requests
from urllib.parse import quote
from osm2geojson import json2geojson

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the frontend

@app.route('/estimate_parking', methods=['POST'])
def estimate_parking():
    data = request.json
    polygon_coords = data['polygon']  # Get the polygon coordinates
    polygon = Polygon(polygon_coords)  # Create a Shapely polygon

    # Convert the polygon coordinates to Overpass API's "poly" format
    poly_string = " ".join([f"{lat} {lon}" for lon, lat in polygon_coords])
    print("Polygon string:" + poly_string)

    # get the roads in the polygon from Overpass
    overpass_query = f"""
    [out:json] [timeout:25];
    (
        way["highway"="residential"](poly:"{poly_string}");
        way["highway"="primary"](poly:"{poly_string}");
        way["highway"="secondary"](poly:"{poly_string}");
        way["highway"="tertiary"](poly:"{poly_string}");
        way["highway"="unclassified"](poly:"{poly_string}");
        way["highway"="service"](poly:"{poly_string}");
    );
    out geom;
    """
    print("QUERY:\n" + overpass_query)
    encoded_query = quote(overpass_query)
    #response = requests.post("https://overpass-api.de/api/interpreter", data=encoded_query)
    url = f"https://overpass-api.de/api/interpreter?data={encoded_query}"
    response = requests.get(url)

    print("QUERY RESPONSE")
    print(response)
    print(jsonify(response.json()))

    if response.status_code == 200:
        # Return the JSON response from Overpass API to the frontend
        geojson = json2geojson(response.json())
        return jsonify(geojson)
    else:
        # Handle errors
        return jsonify({"error": f"Failed to fetch data from Overpass API. Status code: {response.status_code}"}), response.status_code


    # Example calculation (replace with actual logic)
    estimated_parking = polygon.area * 10  # Assume 10 parking spaces per unit area

    return jsonify({'estimated_parking': estimated_parking})

if __name__ == '__main__':
    app.run(debug=True)
