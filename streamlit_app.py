# streamlit_app.py
import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

st.title(" 🩸 Blood Report Analysis")

# File upload
blood_report = st.file_uploader("Upload your blood report", type=["pdf"])

# Location inputs
city = st.text_input("City")
state = st.text_input("State")
country = st.text_input("Country")

if st.button("Analyze"):
    if blood_report and city and state and country:
        # Preparing the form data
        files = {'blood_report': blood_report}
        data = {'city': city, 'state': state, 'country': country}

        # Sending POST request to the Flask server
        try:
            # Display spinner while the analysis is being performed
            with st.spinner("Analyzing... Please Wait. It may take some time."):
                url = os.getenv("BACKEND_URL")
                post_url = f"{url}/analyze"
                # print(requests.get(f"{url}/health").text)  # Checking backend health
                response = requests.post(post_url, files=files, data=data)  # Change URL as per deployment
                response.raise_for_status()
                result = response.json()
            
            # Display results after analysis is complete
            st.subheader("Analysis")
            st.write(result.get('analysis', 'No analysis available'))

            st.subheader("Recommendations")
            st.write(result.get('recommendations', 'No recommendations available'))

            st.subheader("Specialist Recommendations")
            st.write(result.get('specialist_recommendations', 'No specialist recommendations available'))

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a file and fill out all location fields.")
