import streamlit as st
import json
import re

def table_to_json(table_data):
    # Use regex to split the data into city names and prices
    parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
    
    headers = ["10gram", "100gram", "1kg"]
    cities = []
    
    for city, price_10g, price_100g, price_1kg in parts:
        try:
            city_dict = {
                "name": city,
                "prices": {
                    headers[0]: float(price_10g.replace('₹', '').replace(',', '').strip()),
                    headers[1]: float(price_100g.replace('₹', '').replace(',', '').strip()),
                    headers[2]: float(price_1kg.replace('₹', '').replace(',', '').strip())
                }
            }
            cities.append(city_dict)
        except ValueError:
            st.warning(f"Skipping invalid data for city: {city}, prices: {price_10g}, {price_100g}, {price_1kg}")
    
    return {"cities": cities}

st.title("Silver Price Data Converter")

st.write("Paste your silver price data below. The format should be:")
st.code("City ₹ 10gram_price ₹ 100gram_price ₹ 1kg_price")

table_data = st.text_area("Paste your data here:", height=200)

if st.button("Convert to JSON"):
    if table_data:
        json_data = table_to_json(table_data)
        
        st.write("Converted JSON data:")
        st.json(json_data)
        
        # Option to download the JSON file
        json_string = json.dumps(json_data, indent=2)
        st.download_button(
            label="Download JSON",
            file_name="silver_prices.json",
            mime="application/json",
            data=json_string,
        )
    else:
        st.warning("Please paste some data before converting.")

st.write("Note: Make sure your data is in the correct format. Each city should be on a new line or separated by spaces.")
