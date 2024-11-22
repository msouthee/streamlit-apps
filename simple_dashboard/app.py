## Source code from https://courses.spatialthoughts.com/python-dataviz.html#create-a-simple-dashboard
## Date: 2024-11-21

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('A Simple Dashboard')
st.write('This dashboard displays a chart of the selected region.')

# # Access the data [runs each time]
# data_url = 'https://github.com/spatialthoughts/python-dataviz-web/releases/download/osm/'
# csv_file = 'highway_lengths_by_district.csv'

# url = data_url + csv_file
# df = pd.read_csv(url)

# # Shows data table in the app
# st.dataframe(df)


# Use a function to cache the input data so that is doesn't need to be fetched each time the app excutes the script
@st.cache_data
def load_data():
    data_url = 'https://github.com/spatialthoughts/python-dataviz-web/releases/download/osm/'
    csv_file = 'highway_lengths_by_district.csv'

    url = data_url + csv_file
    df = pd.read_csv(url)

    return df

# Run the function to load the data [once]
df = load_data()

# Dropdown menu to select a district
districts = df.DISTRICT.values
district = st.selectbox('Select a district', districts)

# Assign the selected district data to a variable
filtered = df[df['DISTRICT'] == district]

# # Create a plot to show the data for the selected region
# fig, ax = plt.subplots(1,1)
#
# Plot the bar chart based on the filtered data with hard-coded colors
# filtered.plot(kind='bar', ax=ax, color=['#0000FF', '#FF0000'],
#               ylabel='Kilometers', xlabel='Category')
# ax.set_title('Length of Highways')
# ax.set_ylim(0, 2500)
# ax.set_xticklabels([])
# stats = st.pyplot(fig)


# Add the ability for the user to select the color themselves and choose km vs. miles
col1, col2, col3 = st.columns(3)

nh_color = col1.color_picker('Pick NH Color', '#0000FF', key='nh')
sh_color = col2.color_picker('Pick SH Color', '#FF0000', key='sh')
units = col3.radio('Units', ['km', 'miles'])

# If user selects miles
if units == "miles":
    filtered = filtered[['NH', 'SH']]*0.621371
    unit_label = 'Miles'
    ylimit = 1600

# If user selects kilometers
else:
    unit_label = 'Kilometers'
    ylimit = 2500

# Create a plot to show the data for the selected region
fig, ax = plt.subplots(1,1)

# Plot the bar chart based on the filtered data with custom colors
filtered.plot(kind='bar', ax=ax, color=[nh_color, sh_color],
            ylabel=unit_label, xlabel='Category')
ax.set_title('Length of Highways')
ax.set_ylim(0, ylimit)
ax.set_xticklabels([])
stats = st.pyplot(fig)
