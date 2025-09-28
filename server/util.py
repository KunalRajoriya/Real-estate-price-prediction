import pickle
import json
import numpy as np
import warnings

# Suppress UserWarning to keep the output clean during prediction.
warnings.filterwarnings("ignore", category=UserWarning)

# --- Global variables to hold the loaded model and data columns ---
__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    """
    Estimates the price of a home based on its location, size, and number of rooms.

    Args:
        location (str): The location of the property.
        sqft (float): The total square footage of the property.
        bhk (int): The number of bedrooms (BHK).
        bath (int): The number of bathrooms.

    Returns:
        float: The estimated price in Lakhs, rounded to 2 decimal places.
    """
    try:
        # Find the index of the location column. Case-insensitive search.
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # If the location is not in our columns, it's treated as an unknown category.
        loc_index = -1

    # Create a feature vector of zeros with the correct length.
    # This vector must match the input shape expected by the model.
    x = np.zeros(len(__data_columns))

    # Set the values for sqft, bath, and bhk at the correct indices.
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    # If the location was found, set its corresponding column to 1 (one-hot encoding).
    if loc_index >= 0:
        x[loc_index] = 1

    # Use the loaded model to predict the price and return the result.
    # The result is rounded to two decimal places for readability.
    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    """
    Loads the trained model and data columns from saved files (pickle and JSON).
    This function populates the global variables for use by other functions.
    """
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Load the data column information from the JSON file.
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        # The first 3 columns are 'sqft', 'bath', 'bhk'. The rest are locations.
        __locations = __data_columns[3:]

    # Load the trained machine learning model from the pickle file.
    # Check if the model is already loaded to avoid redundant file I/O.
    if __model is None:
        with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
            __model = pickle.load(f)

    print("Loading saved artifacts...done")


def get_location_names():
    """
    Returns a list of all location names that the model was trained on.

    Returns:
        list: A list of location strings.
    """
    return __locations


def get_data_columns():
    """
    Returns the list of all data columns, including features and locations.

    Returns:
        list: A list of all column name strings.
    """
    return __data_columns


# --- Main execution block ---
if __name__ == "__main__":
    # Load artifacts when the script is run directly.
    load_saved_artifacts()

    # --- Test Cases ---
    print("\nAvailable locations:")
    # print(get_location_names()) # Uncomment to see all locations

    print("\n--- Price Estimations ---")
    # Test with a valid, known location
    print(f"Price for 1000 sqft, 3 BHK, 3 Bath in '1st Phase JP Nagar': ", get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))

    # Test with another valid, known location
    print(f"Price for 1000 sqft, 2 BHK, 2 Bath in '1st Phase JP Nagar': ", get_estimated_price("1st Phase JP Nagar", 1000, 2, 2))

    # Test with a location that is not in the dataset (will have a lower accuracy)
    print(f"Price for 1000 sqft, 2 BHK, 2 Bath in 'Kalhalli' (unknown): ", get_estimated_price("Kalhalli", 1000, 2, 2))

    # Test with another location that is not in the dataset
    print(f"Price for 1000 sqft, 2 BHK, 2 Bath in 'Ejipura' (known): ", get_estimated_price("Ejipura", 1000, 2, 2))
