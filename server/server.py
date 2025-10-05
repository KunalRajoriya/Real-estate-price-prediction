from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import util

# Flask app ko initialize karein
app = Flask(__name__)
CORS(app)

# Model aur doosri zaroori cheezein server start hote hi load karein
util.load_saved_artifacts()


# Yeh naya route homepage ke liye hai
@app.route('/')
def home():
    """Homepage ke liye endpoint."""
    # Option 1: Ek simple sa message dikhayein (ab comment kar diya gaya hai)
    # return "Welcome to the Housing Price Prediction System!"

    # Option 2: Ek HTML page (jaise app.html) dikhayein
    return render_template('app.html')


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """Available location names paane ke liye endpoint."""
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
    except Exception as e:
        response = jsonify({'error': str(e)})

    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """Input data ke aadhar par ghar ki keemat predict karne ke liye endpoint."""
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})

    except KeyError:
        response = jsonify({'error': 'Form mein data aadhura hai. Kripya total_sqft, location, bhk, aur bath pradaan karein.'})
    except ValueError:
        response = jsonify({'error': 'Kripya total_sqft, bhk, aur bath ke liye sahi number daalein.'})
    except Exception as e:
        response = jsonify({'error': str(e)})

    return response


@app.errorhandler(404)
def page_not_found(e):
    """Anjaan routes (404 errors) ko handle karein."""
    return jsonify({'error': 'Endpoint nahi mila. URL check karke dobara koshish karein.'}), 404


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run(debug=True)