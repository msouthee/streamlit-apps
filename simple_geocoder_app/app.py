## Source code from https://courses.spatialthoughts.com/python-dataviz.html#create-a-simple-geocoder-app
## Date: 2024-11-21


import folium
import requests
import streamlit as st
from streamlit_folium import st_folium

st.title('A Simple Geocoder')
st.markdown('This app uses the [OpenRouteService API](https://openrouteservice.org/) '
            'to geocode the input address and display the results on the map.')

address = st.text_input('Enter an address:')

# Dropdown to select basemap
basemap = st.selectbox('Select a basemap', ['OpenStreetMap', 'CartoDB Positron', 'CartoDB DarkMatter'])

# Help doc: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
# Get your API key from the secrets file when developing locally [don't commit secrets.toml to github]
ORS_API_KEY = st.secrets['ORS_API_KEY']

# Run the geocoder and cache the data result
@st.cache_data
def geocode(query):
    parameters = {
        'api_key': ORS_API_KEY,
        'text': query
    }

    response = requests.get(
        'https://api.openrouteservice.org/geocode/search',
        params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            x, y = data['features'][0]['geometry']['coordinates']
            return(y, x)  # note order is flipped!

# if there is content in the input box, run the geocoder
if address:
    results = geocode(address)
    
    if results:
        # Print the coordinates
        st.write('Geocoded Coordinates: {}, {}'.format(results[0], results[1]))
    
        # Add the results to an interactive map
        m = folium.Map(location=results, tiles=basemap, zoom_start=12)
        folium.Marker(
            results,
            popup=address,
            icon=folium.Icon(color='green', icon='crosshairs', prefix='fa')).add_to(m)
        st_folium(m, width=800)
    
    else:
        st.error('Request failed. No results.')

