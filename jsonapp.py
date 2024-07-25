import streamlit as st
import json
import re
import requests
from datetime import datetime

def generate_filename(metal_type):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{metal_type.lower()}_{today}.json"

def table_to_json(table_data, metal_type):
    if metal_type == "Gold":
        parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
        gold_prices = []
        for city, price_22k, price_24k, price_18k in parts:
            city_dict = {
                "City": city,
                "24K Today": price_24k.strip(),
                "22K Today": price_22k.strip(),
                "18K Today": price_18k.strip()
            }
            gold_prices.append(city_dict)
        return {"gold_prices": gold_prices}
    else:
        parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
        silver_rates = []
        for city, price_10g, price_100g, price_1kg in parts:
            city_dict = {
                "city": city,
                "10_gram": price_10g.strip(),
                "100_gram": price_100g.strip(),
                "1_kg": price_1kg.strip()
            }
            silver_rates.append(city_dict)
        return {"silver_rates": silver_rates}

def upload_to_heroku(file_name, content, heroku_url):
    url = f"{heroku_url}/upload"
    headers = {"Content-Type": "application/json"}
    data = {"fileName": file_name, "content": content}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

st.title("Precious Metal Price Data Converter and Uploader")

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
        st.json(json_data)
        st.session_state.json_string = json.dumps(json_data, indent=2, ensure_ascii=False)
        filename = generate_filename(metal_type)
        st.download_button(
            label="Download JSON",
            file_name=filename,
            mime="application/json",
            data=st.session_state.json_string,
        )
    else:
        st.warning("Please paste some data before converting.")

st.write("Upload to Heroku")

with st.form(key='heroku_upload_form'):
    heroku_url = st.text_input("Heroku App URL (e.g., https://your-app.herokuapp.com)", 
                               value=st.session_state.heroku_url, 
                               key="heroku_url_input")
    submit_button = st.form_submit_button(label="Upload to Heroku")

if submit_button:
    if heroku_url and st.session_state.json_string:
        st.session_state.heroku_url = heroku_url
        filename = generate_filename(metal_type)
        st.write(f"Attempting to upload {filename} to {heroku_url}")
        response = upload_to_heroku(filename, st.session_state.json_string, heroku_url)
        
        if "error" in response:
            st.error(f"Upload failed: {response['error']}")
        else:
            st.success(f"File uploaded successfully: {response}")
    else:
        st.warning("Please ensure you have entered a Heroku URL and generated JSON data.")

st.write("Note: Make sure your data is in the correct format. Each city should be on a new line.")

st.write("Example data:")
example_data = """
Chennai ₹ 7,452 ₹ 6,831 ₹ 5,596
Mumbai ₹ 7,403 ₹ 6,786 ₹ 5,553
Delhi ₹ 7,418 ₹ 6,800 ₹ 5,564
Kolkata ₹ 7,403 ₹ 6,786 ₹ 5,553
""" if metal_type == "Gold" else """
Chennai ₹ 977.50 ₹ 9,775 ₹ 97,750 
Mumbai ₹ 932.50 ₹ 9,325 ₹ 93,250
Delhi ₹ 932.50 ₹ 9,325 ₹ 93,250
Kolkata ₹ 932.50 ₹ 9,325 ₹ 93,250
"""
st.code(example_data)
