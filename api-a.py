from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)
API_B_URL = "http://localhost:5001/weather/"

logging.basicConfig(level=logging.INFO)

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    if not city.strip():
        return jsonify({"error": "City name must be provided"}), 400

    # Monta a URL para a chamada da API B
    url = f"{API_B_URL}{city}"
    logging.info(f"Fetching weather for city: {city} from {url}")

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return jsonify({"error": "Weather service timed out"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Unable to connect to the weather service"}), 503
    except requests.exceptions.RequestException as e:
        logging.error(f"Unexpected request error: {e}")
        return jsonify({"error": "Unexpected error while requesting weather data"}), 500

    if response.status_code == 404:
        return jsonify({"error": "City not found in weather service"}), 404
    elif response.status_code != 200:
        return jsonify({
            "error": "Weather service returned an unexpected error",
            "status_code": response.status_code
        }), 502

    try:
        weather = response.json()
    except ValueError:
        logging.error("Invalid JSON response from weather service")
        return jsonify({"error": "Invalid response format from weather service"}), 502
    temp = weather.get("temp")
    city_name = weather.get("city")

    if temp is None or city_name is None:
        return jsonify({"error": "Incomplete weather data received"}), 502

    if temp > 30:
        recommendation = "It's very hot. Stay hydrated and use sunscreen!"
    elif temp > 15:
        recommendation = "The weather is nice. Enjoy your day!"
    else:
        recommendation = "It's cold. Don't forget to wear a jacket!"

    return jsonify({
        "city": city_name,
        "temperature": f"{temp} °C",
        "recommendation": recommendation
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
