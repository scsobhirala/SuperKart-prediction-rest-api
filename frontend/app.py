import streamlit as st
import pandas as pd
import requests

#Base URL of the Flask backend
BASE_URL = "http://localhost:7860"

#Set the title of streamlit app
st.title("SuperKart Sales Prediction")

#Section for online prediction 

st.header("Online Prediction")

# Collect the user input for SuperKart features
product_weight = st.number_input("Product Weight", min_value=0.0, max_value=100.0, value=0.0) 
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Medium Sugar", "High Sugar"])  
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.0) 
product_mrp = st.number_input("Product MRP", min_value=0.0, max_value=1000.0, value=0.0) 
store_size = st.selectbox("Store Size", ["Small", "Medium", "Large"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2"]) 
product_id_char = st.selectbox("Product ID Character", ["FD", "DR", "NC"])
store_age_years = st.number_input("Store Age in Years", min_value=0, max_value=100, value=0)  
product_type_category = st.selectbox("Product Type Category", ["Fruits and Vegetables", "Soft Drinks", "Household", "Others"])

# Convert the user input to Dataframe 

data = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location
    "Store_Type": store_type,
    "Product_Id_char": product
    "Store_Age_Years": store_age_years,
    "Product_Type_Category": product_type
}

# Make the prediction when "Predict" button is clicked

if st.button("Predict"):
    try:
        response = requests.post(f"{BASE_URL}/v1/predict", json=data)
        response.raise_for_status()
        prediction = response.json()["prediction"]
        st.success(f"Predicted Sales: {prediction}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        st.error(f"Status Code: {response.status_code}")
        st.error(f"Response Text: {response.text}")
 
 # Section for batch prediction 

 st.header("Batch Prediction")

 # Upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])

 # Make Batch Prediction when the "Predict Batch" button is clicked 

 if st.button("Predict Batch"):
    if uploaded_file is not None:
        try:
            files = {"file": uploaded_file}
            response = requests.post(f"{BASE_URL}/v1/predictbatch", files=files)
            response.raise_for_status()
            predictions = response.json()["predictions"]
            st.success("Batch prediction completed successfully!")
            st.write("Predictions:")
            st.write(predictions)
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
            st.error(f"Status Code: {response.status_code}")
            st.error(f"Response Text: {response.text}")
    else:
        st.warning("Please upload a CSV file for batch prediction.")

















