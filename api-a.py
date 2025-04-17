from flask import Flask, jsonify
import requests
import redis
import json
import logging

app = Flask(__name__)
API_B_URL = "http://localhost:5001/weather/"
CACHE_EXPIRATION = 60  # segundos

# Conexão com Redis
try:
    cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    cache.ping()
    logging.info("Connected to Redis")
except redis.exceptions.ConnectionError as e:
    logging.error("Could not connect to Redis")
    cache = None

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    if not city.strip():
        return jsonify({"error": "City name must be provided"}), 400

    city_key = city.replace(" ", "").lower()

    # Tenta buscar no cache
    if cache:
        cached_data = cache.get(city_key)
        if cached_data:
            logging.info(f"Cache hit for city: {city_key}")
            data = json.loads(cached_data)
        else:
            logging.info(f"Cache miss for city: {city_key}")
            data = fetch_and_cache_weather(city_key)
    else:
        data = fetch_and_cache_weather(city_key)

    if not data:
        return jsonify({"error": "Could not get weather data"}), 500

    temp = data.get("temp")
    city_name = data.get("city")

    if temp is None or city_name is None:
        return jsonify({"error": "Incomplete data"}), 502

    if temp > 30:
        recommendation = "Está quente! Beba água e use protetor solar."
    elif temp > 15:
        recommendation = "Clima agradável! Aproveite o dia."
    else:
        recommendation = "Está frio! Leve um casaco."

    return jsonify({
        "city": city_name,
        "temp": temp,
        "recommendation": recommendation
    })

def fetch_and_cache_weather(city_key):
    try:
        response = requests.get(f"{API_B_URL}{city_key}", timeout=5)
        if response.status_code != 200:
            return None
        data = response.json()

        if cache:
            cache.setex(city_key, CACHE_EXPIRATION, json.dumps(data))

        return data
    except Exception as e:
        logging.error(f"Error fetching data from API B: {e}")
        return None

if __name__ == '__main__':
    app.run(port=5000, debug=True)
