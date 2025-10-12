import pickle
import json
import numpy as np
import warnings
import os  # Path handling ke liye

# Warnings ignore kar do
warnings.filterwarnings("ignore", category=UserWarning)

# --- Global variables ---
__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    """Ghar ki keemat ka estimation."""
    if __model is None or __data_columns is None:
        raise Exception("Model artifacts not loaded. Call load_saved_artifacts() first.")

    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def get_location_names():
    """Return all locations available in model."""
    return __locations


def load_saved_artifacts():
    """
    Model aur data columns load karta hai.
    Server start hone par call hona chahiye.
    """
    global __data_columns
    global __locations
    global __model

    print("Loading saved artifacts...start")
    try:
        # Absolue path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        columns_path = os.path.join(script_dir, "artifacts", "columns.json")
        model_path = os.path.join(script_dir, "artifacts", "banglore_home_prices_model.pickle")

        # Load columns
        with open(columns_path, "r") as f:
            data = json.load(f)
            __data_columns = data["data_columns"]
            __locations = [col.lower() for col in __data_columns[3:]]  # case-insensitive

        # Load model
        if __model is None:
            with open(model_path, "rb") as f:
                __model = pickle.load(f)

        print("Loading saved artifacts...done")

    except FileNotFoundError as e:
        print("Error: Artifacts folder or files not found.")
        print(e)
    except Exception as e:
        print(f"Unexpected error while loading artifacts: {e}")


# --- Test ---
if __name__ == "__main__":
    load_saved_artifacts()
    if __locations:
        print("\n--- Price Estimations ---")
        print(f"Price for '1st Phase JP Nagar', 1000 sqft, 3 BHK, 3 Bath: ",
              get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))
        print(f"Price for 'Ejipura', 1000 sqft, 2 BHK, 2 Bath: ",
              get_estimated_price("Ejipura", 1000, 2, 2))
