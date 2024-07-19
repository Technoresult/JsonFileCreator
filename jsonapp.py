import streamlit as st
import json
import re

def table_to_json(table_data, metal_type):
    # Use regex to split the data into city names and prices
    parts = re.findall(r'(\w+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)\s+(₹\s*[\d,.]+)', table_data)
    
    headers = ["24K", "22K", "18K"] if metal_type == "Gold" else ["10gram", "100gram", "1kg"]
    cities = []
    
    for city, price_1, price_2, price_3 in parts:
        try:
            city_dict = {
                "name": city,
                "prices": {
                    headers[0]: float(price_1.replace('₹', '').replace(',', '').strip()),
                    headers[1]: float(price_2.replace('₹', '').replace(',', '').strip()),
                    headers[2]: float(price_3.replace('₹', '').replace(',', '').strip())
                }
            }
            cities.append(city_dict)
        except ValueError:
            st.warning(f"Skipping invalid data for city: {city}, prices: {price_1}, {price_2}, {price_3}")
    
    return {"cities": cities}

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
    Chennai ₹ 6,875 ₹ 7,500 ₹ 5,632 
    Mumbai ₹ 6,815 ₹ 7,435 ₹ 5,576 
    Delhi ₹ 6,830 ₹ 7,450 ₹ 5,588 
    Kolkata ₹ 6,815 ₹ 7,435 ₹ 5,576 
    """
else:
    example_data = """
    Chennai ₹ 977.50 ₹ 9,775 ₹ 97,750 
    Mumbai ₹ 932.50 ₹ 9,325 ₹ 93,250
    Delhi ₹ 932.50 ₹ 9,325 ₹ 93,250
    Kolkata ₹ 932.50 ₹ 9,325 ₹ 93,250
    """
st.code(example_data)
