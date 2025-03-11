from flask import Flask, render_template, request, jsonify
from shapely.geometry import Polygon

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

    # Example calculation (replace with actual logic)
    estimated_parking = polygon.area * 10  # Assume 10 parking spaces per unit area

    return jsonify({'estimated_parking': estimated_parking})

if __name__ == '__main__':
    app.run(debug=True)
