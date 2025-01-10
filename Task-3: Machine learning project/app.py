from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the model, categories, and feature names
with open("./model/flight_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("./model/categories.pkl", "rb") as f:
    categories = pickle.load(f)

with open("./model/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)


def preprocess_input(data):
    # Create an empty DataFrame with all possible features (initialized to 0)
    input_df = pd.DataFrame(0, index=[0], columns=feature_names)

    # Set non-categorical features
    input_df["duration"] = float(data["duration"])
    input_df["days_left"] = int(data["days_left"])

    # Convert class
    input_df["class"] = 1 if data["class"] == "Business" else 0

    # Convert stops
    stops_map = {"zero": 0, "one": 1, "two_or_more": 2}
    input_df["stops"] = stops_map[data["stops"]]

    # Set dummy variables to 1 for the selected categories
    input_df[f"airline_{data['airline']}"] = 1
    input_df[f"source_{data['source_city']}"] = 1
    input_df[f"dest_{data['destination_city']}"] = 1
    input_df[f"arrival_{data['arrival_time']}"] = 1
    input_df[f"departure_{data['departure_time']}"] = 1

    return input_df


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        input_data = {
            "airline": request.form["airline"],
            "source_city": request.form["source_city"],
            "destination_city": request.form["destination_city"],
            "departure_time": request.form["departure_time"],
            "arrival_time": request.form["arrival_time"],
            "stops": request.form["stops"],
            "class": request.form["class"],
            "duration": request.form["duration"],
            "days_left": request.form["days_left"],
        }

        # Preprocess input to make prediction
        processed_input = preprocess_input(input_data)
        prediction = model.predict(processed_input)[0]

    return render_template("index.html", categories=categories, prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
