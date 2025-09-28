from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS ke liye naya import
from . import util

# Flask app ko initialize karein
app = Flask(__name__)
# Poori app ke liye CORS ko enable karein (Cross-Origin Resource Sharing)
CORS(app)

# Model aur doosri zaroori cheezein server start hote hi load karein
# Yeh line 'if __name__ == "__main__"' block se bahar honi chahiye taaki Render par chale
util.load_saved_artifacts()


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
        # POST request ke form se data lein
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Util module se function ka istemal karke keemat predict karein
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        # Anumaanit keemat ko JSON response mein return karein
        response = jsonify({'estimated_price': estimated_price})

    except KeyError:
        # Jab form mein data missing ho, uss case ko handle karein
        response = jsonify({'error': 'Form mein data aadhura hai. Kripya total_sqft, location, bhk, aur bath pradaan karein.'})
    except ValueError:
        # Jab sqft, bhk, ya bath sahi number na ho, uss case ko handle karein
        response = jsonify({'error': 'Kripya total_sqft, bhk, aur bath ke liye sahi number daalein.'})
    except Exception as e:
        # Doosre potential errors ko handle karein
        response = jsonify({'error': str(e)})

    return response


@app.errorhandler(404)
def page_not_found(e):
    """Anjaan routes (404 errors) ko handle karein."""
    return jsonify({'error': 'Endpoint nahi mila. URL check karke dobara koshish karein.'}), 404


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    # 'app.run' sirf local development ke liye istemal hota hai
    app.run(debug=True)