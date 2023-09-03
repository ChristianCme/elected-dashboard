import streamlit as st
import requests
import pandas as pd

# Streamlit app title
st.title('Congress Voting Record Dashboard')

#Loads Voting Google sheet
@st.cache_data(ttl=600)
def load_data():
    house_csv_url = "https://docs.google.com/spreadsheets/d/1gPBdBrqVCbtuy7f1bjOdCDUzEv5RqbbU1yYAr3KoHYE/export?format=csv&gid=1289123714"
    senate_csv_url = "https://docs.google.com/spreadsheets/d/1gPBdBrqVCbtuy7f1bjOdCDUzEv5RqbbU1yYAr3KoHYE/export?format=csv&gid=0"
    return (pd.read_csv(house_csv_url), pd.read_csv(senate_csv_url))

house_data, senate_data = load_data()
st.write("Original Data provided [here](https://docs.google.com/spreadsheets/d/1gPBdBrqVCbtuy7f1bjOdCDUzEv5RqbbU1yYAr3KoHYE/edit#gid=1289123714)")
with st.expander("Raw Data"):
    st.write(house_data)
    st.write(senate_data)

# Input for zip code
zip_code = st.text_input('Enter your zip code:')

# Function to fetch Congress people for ZIP
def get_rep_by_district(zip_code):
    # Replace [ZIP] with your actual ZIP code
    url = f"https://whoismyrepresentative.com/getall_mems.php?zip={zip_code}&output=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        members = data['results']
        return members
    else:
        return False
        

# Check if the user has entered a valid zip code
if zip_code and zip_code.isdigit() and len(zip_code) == 5:
    members = get_rep_by_district(zip_code)
    if not members:
        st.error('API Failed', icon="🚨")
    else:
        house_local = [reps for reps in members if reps.get("district") != ""]
        senate_local = [reps for reps in members if reps.get("district") == ""]  
    
        st.write("## House Reps")
        if len(house_local) > 1:
            st.info("More than one Representative for Zip")
        # st.write(house_local)
        district_lists = []
        for rep in house_local:
            state = rep['state']
            district = rep['district']
            district = district.zfill(2)
            district_lists.append(state + '-' + district)
        st.write(house_data.loc[house_data['CD'].isin(district_lists)])


        st.write("## Senators")
        state = senate_local[0]['state']
        st.write(state)
        states = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
        st.write(states[state])
        st.write(senate_data.loc[senate_data['State'] == states[state]])

elif zip_code:
    st.warning('Please enter a valid 5-digit zip code.')

