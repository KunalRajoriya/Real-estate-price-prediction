import pickle
import json
import numpy as np
import warnings
import os  # Yeh naya import hai file paths ke liye

# UserWarning ko ignore karein taaki output saaf rahe
warnings.filterwarnings("ignore", category=UserWarning)

# --- Global variables ---
__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    """Ghar ki keemat ka anumaan lagata hai."""
    try:
        # Location column ka index dhoondein (case-insensitive)
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # Agar location nahi milti, toh use unknown category maana jaata hai
        loc_index = -1

    # Model ke liye sahi length ka feature vector banayein
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    # Agar location mili hai, toh uske column ko 1 set karein (one-hot encoding)
    if loc_index >= 0:
        x[loc_index] = 1

    # Load kiye gaye model se keemat predict karein
    return round(__model.predict([x])[0], 2)


def get_location_names():
    """Model mein istemal ki gayi sabhi locations ki list return karta hai."""
    return __locations


def load_saved_artifacts():
    """
    Trained model aur data columns ko files se load karta hai.
    Yeh function server start hone par ek baar chalta hai.
    """
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    try:
        # Is script (util.py) ke directory ka absolute path pata karein
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Artifacts ka absolute path banayein
        columns_path = os.path.join(script_dir, "artifacts", "columns.json")
        model_path = os.path.join(script_dir, "artifacts", "banglore_home_prices_model.pickle")

        # Absolute path ka istemal karke JSON file load karein
        with open(columns_path, "r") as f:
            data = json.load(f)
            __data_columns = data["data_columns"]
            __locations = __data_columns[3:]  # Pehle 3 columns features hain

        # Absolute path ka istemal karke model file load karein
        if __model is None:
            with open(model_path, "rb") as f:
                __model = pickle.load(f)
        
        print("Loading saved artifacts...done")

    except FileNotFoundError as e:
        print(f"Error loading artifacts: File not found. Make sure 'artifacts' folder is in the 'server' directory.")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred while loading artifacts: {e}")


# --- Test Cases ---
if __name__ == "__main__":
    load_saved_artifacts()
    if __locations:
        print("\n--- Price Estimations ---")
        print(f"Price for '1st Phase JP Nagar', 1000 sqft, 3 BHK, 3 Bath: ", get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))
        print(f"Price for 'Ejipura', 1000 sqft, 2 BHK, 2 Bath: ", get_estimated_price("Ejipura", 1000, 2, 2))