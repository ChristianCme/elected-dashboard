import streamlit as st
import requests

# Streamlit app title
st.title('Zip Code Information App')

# Input for zip code
zip_code = st.text_input('Enter your zip code:')

# Function to fetch state information
def get_state_info(zip_code):
    state_api_url = f'https://openstates.org/api/v1/legislators/geo/?lat=0&long=0&apikey=YOUR_OPEN_STATES_API_KEY'
    response = requests.get(state_api_url)
    data = response.json()
    if data:
        return data[0]['state']
    return None

# Function to fetch House of Representatives district information
def get_rep_district(zip_code):
    congress_api_url = f'https://theunitedstates.io/congress-phrases/congresses/117/sessions/1/congresspersons/house/?format=json'
    response = requests.get(congress_api_url)
    data = response.json()
    for congressperson in data:
        if zip_code in congressperson['district']['postal_codes']:
            return congressperson['name'], congressperson['district']['name']
    return None, None

# Check if the user has entered a valid zip code
if zip_code and zip_code.isdigit() and len(zip_code) == 5:
    state_info = get_state_info(zip_code)
    rep_name, rep_district = get_rep_district(zip_code)

    if state_info:
        st.write(f'**State:** {state_info}')

    if rep_name and rep_district:
        st.write(f'**House of Representatives District:** {rep_district}')
        st.write(f'**Your Representative:** {rep_name}')
    elif rep_name:
        st.write(f'**Your Representative:** {rep_name}')
    else:
        st.warning('House of Representatives information not found for this zip code.')

elif zip_code:
    st.warning('Please enter a valid 5-digit zip code.')

# Note: Replace 'YOUR_OPEN_STATES_API_KEY' with your actual Open States API key.
