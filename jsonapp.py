import streamlit as st
import json
import re

def text_to_json(text, sample_json):
    # Parse the sample JSON
    sample = json.loads(sample_json)
    
    # Split the input text into lines
    lines = text.strip().split('\n')
    
    # Create a list to store the resulting JSON objects
    result = []
    
    for line in lines:
        # Use regex to split by both currency symbol and space to extract data
        data = re.split(r' [₹ ]', line.strip())
        
        # Create a new JSON object
        obj = {}
        obj["city"] = data[0]  # First element is the city
        
        # Assign values to corresponding keys
        obj["10_gram"] = f"₹ {data[1]}"
        obj["100_gram"] = f"₹ {data[2]}"
        obj["1_kg"] = f"₹ {data[3]}"
        
        result.append(obj)
    
    return result

def main():
    st.title("Text to JSON Converter")
    
    # Sample JSON format
    sample_json = '''
    {
      "city": "Chennai",
      "10_gram": "₹ 1,005",
      "100_gram": "₹ 10,050",
      "1_kg": "₹ 1,00,500"
    }
    '''
    
    # Input for text to convert
    input_text = st.text_area("Enter text to convert:", 
                              value="Ahmedabad ₹ 960 ₹ 9,600 ₹ 96,000\nJaipur ₹ 960 ₹ 9,600 ₹ 96,000",
                              height=150)
    
    if st.button("Convert"):
        if input_text:
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
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter text to convert.")

if __name__ == "__main__":
    main()
