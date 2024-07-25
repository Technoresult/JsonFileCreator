import streamlit as st
import json
import re
import requests
from datetime import datetime

# Function to generate filename with date
def generate_filename(metal_type):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{metal_type[0].upper()}_{today}.json"

# Function to convert table data to JSON
def table_to_json(table_data, metal_type):
    if metal_type == "Gold":
        parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
        gold_prices = []
        for city, price_22k, price_24k, price_18k in parts:
            try:
                city_dict = {
                    "City": city,
                    "24K Today": price_24k.strip(),
                    "22K Today": price_22k.strip(),
                    "18K Today": price_18k.strip()
                }
                gold_prices.append(city_dict)
            except ValueError:
                st.warning(f"Skipping invalid data for city: {city}, prices: {price_24k}, {price_22k}, {price_18k}")
        return {"gold_prices": gold_prices}
    else:
        parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
        silver_rates = []
        for city, price_10g, price_100g, price_1kg in parts:
            try:
                city_dict = {
                    "city": city,
                    "10_gram": price_10g.strip(),
                    "100_gram": price_100g.strip(),
                    "1_kg": price_1kg.strip()
                }
                silver_rates.append(city_dict)
            except ValueError:
                st.warning(f"Skipping invalid data for city: {city}, prices: {price_10g}, {price_100g}, {price_1kg}")
        return {"silver_rates": silver_rates}

# Function to upload JSON to Heroku
def upload_to_heroku(file_name, content, heroku_url):
    url = f"{heroku_url}/upload"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "fileName": file_name,
        "content": content
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200 or response.status_code == 201:
        try:
            response_json = response.json()
            return response_json
        except ValueError:
            return {"error": "Response is not JSON"}
    else:
        return {"error": f"Failed to upload file. Status code: {response.status_code}. Response: {response.text}"}

st.title("Precious Metal Price Data Converter")

# Initialize session state variables
if 'heroku_url' not in st.session_state:
    st.session_state.heroku_url = ""
if 'json_string' not in st.session_state:
    st.session_state.json_string = ""

metal_type = st.selectbox("Select metal type:", ["Gold", "Silver"])

st.write(f"Paste your {metal_type.lower()} price data below. The format should be:")
if metal_type == "Gold":
    st.code("City ₹ 24K_price ₹ 22K_price ₹ 18K_price")
else:
    st.code("City ₹ 10gram_price ₹ 100gram_price ₹ 1kg_price")

table_data = st.text_area("Paste your data here:", height=200)

if st.button("Convert to JSON"):
    if table_data:
        json_data = table_to_json(table_data, metal_type)
        st.write("Converted JSON data:")
        st.json(json_data, expanded=True)
        st.session_state.json_string = json.dumps(json_data, indent=2, ensure_ascii=False).encode('utf-8').decode('utf-8')
        filename = generate_filename(metal_type)
        st.download_button(
            label="Download JSON",
            file_name=f"{metal_type.lower()}_prices.json",
            mime="application/json",
            data=st.session_state.json_string,
        )
    else:
        st.warning("Please paste some data before converting.")

# Heroku upload section
st.write("Upload to Heroku")

with st.form(key='heroku_upload_form'):
    heroku_url = st.text_input("Heroku App URL (e.g., https://your-heroku-app.herokuapp.com)", value=st.session_state.heroku_url, key="heroku_url_input")
    submit_button = st.form_submit_button(label="Upload to Heroku")

if submit_button:
    if heroku_url and st.session_state.json_string:
        st.session_state.heroku_url = heroku_url
        filename = generate_filename(metal_type)
        response = upload_to_heroku(filename, st.session_state.json_string, heroku_url)
        
        if "error" in response:
            st.error(response["error"])
        else:
            st.success("File uploaded successfully!")

st.write("Note: Make sure your data is in the correct format. Each city should be on a new line or separated by spaces.")

st.write("Example data:")
if metal_type == "Gold":
    example_data = """
    Chennai ₹ 7,452 ₹ 6,831 ₹ 5,596
    Mumbai ₹ 7,403 ₹ 6,786 ₹ 5,553
    Delhi ₹ 7,418 ₹ 6,800 ₹ 5,564
    Kolkata ₹ 7,403 ₹ 6,786 ₹ 5,553
    """
else:
    example_data = """
    Chennai ₹ 977.50 ₹ 9,775 ₹ 97,750 
    Mumbai ₹ 932.50 ₹ 9,325 ₹ 93,250
    Delhi ₹ 932.50 ₹ 9,325 ₹ 93,250
    Kolkata ₹ 932.50 ₹ 9,325 ₹ 93,250
    """
st.code(example_data)
