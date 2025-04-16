from flask import Flask, jsonify

app = Flask(__name__)

weather_data = {
    "saopaulo": {"city": "São Paulo", "temp": 25, "unit": "Celsius"},
    "riodejaneiro": {"city": "Rio de Janeiro", "temp": 33, "unit": "Celsius"},
    "curitiba": {"city": "Curitiba", "temp": 14, "unit": "Celsius"},
    "salvador": {"city": "Salvador", "temp": 28, "unit": "Celsius"}
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_key = city.replace(" ", "").lower()
    data = weather_data.get(city_key)

    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
