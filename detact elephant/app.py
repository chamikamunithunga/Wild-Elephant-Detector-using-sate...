from flask import Flask, request, jsonify, render_template
import folium
from geopy.geocoders import Nominatim
import random  # Simulating elephant locations (replace with real data)

app = Flask(__name__)

# Geolocator for city to coordinates
geolocator = Nominatim(user_agent="elephant_tracker")

# Simulated elephant data (replace with real-time data integration)
def get_elephant_locations(city_coords):
    elephant_data = []
    for _ in range(5):  # Simulate 5 elephant positions near the city
        lat = city_coords[0] + random.uniform(-0.05, 0.05)
        lon = city_coords[1] + random.uniform(-0.05, 0.05)
        elephant_data.append((lat, lon))
    return elephant_data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    city = request.form['city']
    location = geolocator.geocode(city + ", Sri Lanka")

    if location:
        city_coords = (location.latitude, location.longitude)
        elephants = get_elephant_locations(city_coords)

        # Create map
        m = folium.Map(location=city_coords, zoom_start=12)
        folium.Marker(city_coords, tooltip="City Center").add_to(m)
        for idx, (lat, lon) in enumerate(elephants):
            folium.Marker((lat, lon), tooltip=f"Elephant {idx + 1}").add_to(m)

        # Save map
        map_file = "templates/map.html"
        m.save(map_file)
        return render_template('map.html')
    else:
        return "City not found. Please enter a valid Sri Lankan city."

if __name__ == '__main__':
    app.run(debug=True)
