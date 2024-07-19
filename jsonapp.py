import streamlit as st
import json
import re

def table_to_json(table_data, metal_type):
    if metal_type == "Gold":
        # Use regex to split the data into city names and prices
        parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
        
        gold_prices = []
        
        for city, price_24k, price_22k, price_18k in parts:
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
        # Silver conversion
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

st.title("Precious Metal Price Data Converter")

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
        
        # Option to download the JSON file
        json_string = json.dumps(json_data, indent=2)
        st.download_button(
            label="Download JSON",
            file_name=f"{metal_type.lower()}_prices.json",
            mime="application/json",
            data=json_string,
        )
    else:
        st.warning("Please paste some data before converting.")

st.write("Note: Make sure your data is in the correct format. Each city should be on a new line or separated by spaces.")

# Example data
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
