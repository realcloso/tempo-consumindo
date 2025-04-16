from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_B_URL = "http://localhost:5001/weather/"

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    # Requisição à API B
    try:
        response = requests.get(f"{API_B_URL}{city}")
        if response.status_code == 404:
            return jsonify({"error": "City not found in weather service"}), 404
        elif response.status_code != 200:
            return jsonify({"error": "Weather service error"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error connecting to weather service", "details": str(e)}), 500

    weather = response.json()
    temp = weather.get("temp")

    if temp is None:
        return jsonify({"error": "Temperature data not found"}), 500

    if temp > 30:
        recommendation = "It's very hot. Stay hydrated and use sunscreen!"
    elif temp > 15:
        recommendation = "The weather is nice. Enjoy your day!"
    else:
        recommendation = "It's cold. Don't forget to wear a jacket!"

    return jsonify({
        "city": weather["city"],
        "temperature": f"{temp} °C",
        "recommendation": recommendation
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
