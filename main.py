import streamlit as st
import plotly.express as px
from Backend import get_data

# Setting the title of the Streamlit app
st.title('Weather forecast for the Next Days')

# Creating a text input field for the user to enter the place
place = st.text_input("Place: ")

# Creating a slider for the user to select the number of forecast days, with a help tooltip
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")

# Creating a dropdown (select box) for the user to choose between "Temperature" and "Sky"
options = st.selectbox("Select to view",
                       ("Temperature", "Sky"))

# Displaying a subheader that dynamically updates based on the user's input
st.subheader(f"{options} for the next {days} days in {place}")

# Checking if the place input is provided by the user
if place:
    try:
        # Fetching filtered data using the get_data function from the Backend module
        filtered_Data = get_data(place, days)

        # If the user selects "Temperature"
        if options == "Temperature":
            # Extracting temperatures and dates from the filtered data
            temperatures = [dict['main']['temp'] / 10 for dict in filtered_Data]
            date = [dict["dt_txt"] for dict in filtered_Data]

            # Creating a line chart using Plotly Express with the dates and temperatures
            figure = px.line(x=date, y=temperatures, labels={"x": "Date",
                                                             "y": "Temperature (C)"})
            # Displaying the chart in the Streamlit app
            st.plotly_chart(figure)

        # If the user selects "Sky"
        if options == "Sky":
            # Dictionary mapping sky conditions to image file paths
            images = {"Clear": "images/clear.png",
                      "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png",
                      "Snow": "images/snow.png"}

            # Extracting sky conditions and dates from the filtered data
            Sky_conditions = [dict['weather'][0]['main'] for dict in filtered_Data]
            dates = [dict["dt_txt"] for dict in filtered_Data]

            # Mapping sky conditions to image file paths
            images_path = [images[condition] for condition in Sky_conditions]

            # Displaying the corresponding images and dates in rows
            for i in range(0, len(dates), 3):
                cols = st.columns(3)  # Creating a new row with 3 columns

                for col, date, condition, img_path in zip(cols, dates[i:i + 3], Sky_conditions[i:i + 3],
                                                          images_path[i:i + 3]):
                    with col:
                        st.image(img_path, width=120)
                        st.write(f"{date} - {condition}")  # Displaying the date and condition below the image

    # Handling KeyError in case of invalid place name or missing data
    except KeyError:
        st.write("Please check the place name and try again.")
