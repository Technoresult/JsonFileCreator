import streamlit as st
import json
import re

def text_to_json(text, sample_json):
    try:
        # Parse the sample JSON
        sample = json.loads(sample_json)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the sample. Please check and try again.")
    
    # Extract keys from the sample JSON
    keys = list(sample.keys())
    
    # Initialize result as a list
    result = []
    
    # Split the input text into lines
    lines = text.strip().split('\n')
    
    # Process each line of the input text
    for line in lines:
        # Extract city and prices using regular expression
        match = re.match(r'([A-Za-z ]+)\s+₹ ([\d,\.]+)\s+₹ ([\d,\.]+)\s+₹ ([\d,\.]+)', line.strip())
        if match:
            city = match.group(1).strip()
            price_10_gram = "₹ " + match.group(2).strip()
            price_100_gram = "₹ " + match.group(3).strip()
            price_1_kg = "₹ " + match.group(4).strip()
            
            # Create a new JSON object based on the sample structure
            obj = {
                "city": city,
                "10_gram": price_10_gram,
                "100_gram": price_100_gram,
                "1_kg": price_1_kg
            }
            
            # Add the JSON object to the result list
            result.append(obj)
    
    return result

def main():
    st.title("Text to JSON Converter")
    
    # Input for sample JSON
    sample_json = st.text_area("Enter sample JSON:", 
                               value='{"city": "Chennai", "10_gram": "₹ 1,005", "100_gram": "₹ 10,050", "1_kg": "₹ 1,00,500"}',
                               height=100)
    
    # Input for text to convert
    input_text = st.text_area("Enter text to convert:", 
                              value="City 10 gram 100 gram 1 Kg Chennai ₹ 1,005 ₹ 10,050 ₹ 1,00,500\nMumbai ₹ 960 ₹ 9,600 ₹ 96,000\nDelhi ₹ 960 ₹ 9,600 ₹ 96,000\nKolkata ₹ 960 ₹ 9,600 ₹ 96,000\nBangalore ₹ 947.50 ₹ 9,475 ₹ 94,750\nHyderabad ₹ 1,005 ₹ 10,050 ₹ 1,00,500\nKerala ₹ 1,005 ₹ 10,050 ₹ 1,00,500",
                              height=150)
    
    if st.button("Convert"):
        if sample_json and input_text:
            try:
                result = text_to_json(input_text, sample_json)
                st.subheader("Converted JSON:")
                st.json(result)
                
                # Option to download the JSON file
                json_string = json.dumps(result, indent=2)
                st.download_button(
                    label="Download JSON",
                    file_name="converted.json",
                    mime="application/json",
                    data=json_string,
                )
            except ValueError as ve:
                st.error(str(ve))
        else:
            st.warning("Please enter both sample JSON and text to convert.")

if __name__ == "__main__":
    main()
