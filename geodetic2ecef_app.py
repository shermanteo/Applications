from flask import Flask, render_template, request
import numpy as np
import webbrowser

app = Flask(__name__)

# Constants
a = 6378137  # Semi-major axis (meters)
f = 1 / 298.257223563  # Flattening
e2 = f * (2 - f)  # Eccentricity squared

def geodetic_2_ecef(lat, lon, alt):
    """Converts geodetic coordinates (latitude, longitude, altitude) to ECEF."""
    lat_radians = np.radians(lat)  # Convert degrees to radians
    lon_radians = np.radians(lon)  # Convert degrees to radians

    # Compute N
    N = a / np.sqrt(1 - e2 * np.sin(lat_radians) ** 2)
    
    # Compute ECEF coordinates
    X = (N + alt) * np.cos(lat_radians) * np.cos(lon_radians)
    Y = (N + alt) * np.cos(lat_radians) * np.sin(lon_radians)
    Z = (N * (1 - e2) + alt) * np.sin(lat_radians)
    
    return round(X, 3), round(Y, 3), round(Z, 3)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Get user input from the form
            lat = float(request.form["latitude"])
            lon = float(request.form["longitude"])
            alt = float(request.form["altitude"])

            # Convert to ECEF
            X, Y, Z = geodetic_2_ecef(lat, lon, alt)

            return render_template("index.html", X=X, Y=Y, Z=Z, lat=lat, lon=lon, alt=alt)
        
        except ValueError:
            error = "Invalid input! Please enter valid numbers."
            return render_template("index.html", error=error)

    return render_template("index.html")

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")  # Automatically open browser
    app.run(debug=True)
