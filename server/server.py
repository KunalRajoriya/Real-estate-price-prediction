from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import util
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_folder=os.path.join(base_dir, '../static'),
            template_folder=os.path.join(base_dir, '../templates'))
CORS(app)

# Load model artifacts
util.load_saved_artifacts()

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
    except Exception as e:
        response = jsonify({'error': str(e)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        estimated_price = float(util.get_estimated_price(location, total_sqft, bhk, bath))
        response = jsonify({'estimated_price': estimated_price})
    except Exception as e:
        response = jsonify({'error': str(e)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == "__main__":
    print("✅ Starting Flask Server for Home Price Prediction...")
    app.run(debug=True, port=5000)
