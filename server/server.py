from flask import Flask, request, jsonify
import util  # CORRECTED: Was 'import ut' which is incorrect.

# Initialize Flask app
app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """Endpoint to get available location names."""
    try:
        # Call the get_location_names function from the util module
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
    except Exception as e:
        # Handle potential errors and return an error message
        response = jsonify({'error': str(e)})

    # Add a CORS header to allow requests from other domains (like a frontend website)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# CORRECTED: The duplicate @app.route line was removed.
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """Endpoint to predict home price based on input data."""
    try:
        # Get data from the POST request's form
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Predict the price using the function from the util module
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        # Return the estimated price as a JSON response
        response = jsonify({'estimated_price': estimated_price})

    except KeyError:
        # Handle cases where form data is missing
        response = jsonify({'error': 'Missing data in form. Please provide total_sqft, location, bhk, and bath.'})
    except Exception as e:
        # Handle other potential errors
        response = jsonify({'error': str(e)})

    # Add CORS header
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.errorhandler(404)
def page_not_found(e):
    """Handle undefined routes (404 errors)."""
    return jsonify({'error': 'Endpoint not found. Check the URL and try again.'}), 404


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    try:
        # Load the saved model and other artifacts before starting the server
        util.load_saved_artifacts()
        # Run the Flask application
        app.run(debug=True)  # debug=True provides detailed error messages during development
    except Exception as e:
        print(f"Error starting server: {e}")
