import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask("SuperKart Model")

# Load the serialized model
model = joblib.load("superkart_model_v1.0.joblib")

@app.route("/")
def home():
    return "Welcome to the SuperKart Model API!"

@app.route("/v1/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = [
            data.get("Product_Weight", 0.0),
            data.get("Product_Sugar_Content", "Low Sugar"),
            data.get("Product_Allocated_Area", 0.0),
            data.get("Product_MRP", 0.0),
            data.get("Store_Size", "Medium"),
            data.get("Store_Location_City_Type", "Tier 2"),
            data.get("Store_Type", "Supermarket Type2"),
            data.get("Product_Type", "Others"),
            data.get("Store_Age_Years", 0),
            data.get("Store_Establishment_Year", 2000)
        ]
        input_df = pd.DataFrame([features], columns=[
            "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
            "Product_MRP", "Store_Size", "Store_Location_City_Type",
            "Store_Type", "Product_Type"
        ])
        predicted_value = float(model.predict(input_df)[0])
        return jsonify({"prediction": predicted_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/v1/predictbatch", methods=["POST"])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        df = pd.read_csv(file)
        if 'Store_Age_Years' in df.columns:
            df['Store_Establishment_Year'] = 2026 - df['Store_Age_Years']
        if 'Product_Type' not in df.columns:
            prefix_mapping = {'FD': 'Fruits and Vegetables', 'DR': 'Soft Drinks', 'NC': 'Household'}
            product_prefix = df['Product_Id'].str[:2] if 'Product_Id' in df.columns else pd.Series(['FD']*len(df))
            df['Product_Type'] = product_prefix.map(prefix_mapping).fillna('Others')
        predicted_sales = model.predict(df).tolist()
        return jsonify({"predictions": predicted_sales})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
