import streamlit as st
import json
import re

def text_to_json(text, sample_json):
    # Parse the sample JSON
    sample = json.loads(sample_json)
    
    # Extract keys from the sample JSON
    keys = list(sample.keys())
    
    # Split the input text into lines
    lines = text.strip().split('\n')
    
    # Create a list to store the resulting JSON objects
    result = []
    
    # Process each line of the input text
    for line in lines:
        # Split the line into values
        values = re.split(r'\s+', line.strip())
        
        # Create a new JSON object
        obj = {}
        for i, key in enumerate(keys):
            if i < len(values):
                obj[key] = values[i]
            else:
                obj[key] = ""
        
        result.append(obj)
    
    return result

def main():
    st.title("Text to JSON Converter")
    
    # Input for sample JSON
    sample_json = st.text_area("Enter sample JSON:", 
                               value='{"name": "John", "age": "30", "city": "New York"}',
                               height=100)
    
    # Input for text to convert
    input_text = st.text_area("Enter text to convert:", 
                              value="Alice 25 London\nBob 35 Paris\nCharlie 40 Berlin",
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
            except json.JSONDecodeError:
                st.error("Invalid JSON format in the sample. Please check and try again.")
        else:
            st.warning("Please enter both sample JSON and text to convert.")

if __name__ == "__main__":
    main()
