import pandas as pd
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz
import requests

# Load the CSV file with error handling and data type specification
crime_data = pd.read_csv("NYC_crime.csv", dtype=str, low_memory=False)

# Clean the date column by filtering out invalid dates
def clean_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%m/%d/%Y')
    except ValueError:
        return pd.NaT  # Return NaT (Not a Time) for invalid dates

# Apply the cleaning function to the date column
crime_data['CMPLNT_FR_DT'] = crime_data['CMPLNT_FR_DT'].apply(clean_date)

# Filter for years after 2018
crime_data = crime_data[crime_data['CMPLNT_FR_DT'].dt.year > 2018]

# Drop rows with invalid dates
crime_data = crime_data.dropna(subset=['CMPLNT_FR_DT'])

# Convert the time column
crime_data['CMPLNT_FR_TM'] = pd.to_datetime(crime_data['CMPLNT_FR_TM'], format='%H:%M:%S', errors='coerce').dt.time

# Drop rows with invalid times
crime_data = crime_data.dropna(subset=['CMPLNT_FR_TM'])

# Set up the location for New York City
nyc = LocationInfo("New York City", "USA", "America/New_York", 40.7128, -74.0060)

# Get the timezone object
nyc_tz = pytz.timezone("America/New_York")


def light_level(complaint_date, complaint_time):
    try:
        s = sun(nyc.observer, date = complaint_date.date(),  tzinfo=nyc_tz)
        sunrise = s['sunrise'].time()
        sunset = s['sunset'].time()
        
        civil_twilight_start = s['dawn'].time()  # Start of civil twilight (before sunrise)
        civil_twilight_end = s['dusk'].time()    # End of civil twilight (after sunset)

        # Determine the light level based on time of day
        if complaint_time < civil_twilight_start or complaint_time > civil_twilight_end:
            return 0  # Night
        elif civil_twilight_start <= complaint_time < sunrise or sunset < complaint_time <= civil_twilight_end:
            return 0.5  # Twilight (dawn/dusk)
        else:
            return 1  # Daylight

        return sunrise, sunset, 1 if sunrise <= complaint_time <= sunset else 0, complaint_date
    except ValueError as e:
        print(f"Error: {e}")
        return None  # Return None if the sun calculation fails

# Apply the function to the dataset
crime_data['Light_Level'] = crime_data.apply(
    lambda row: light_level(row['CMPLNT_FR_DT'], row['CMPLNT_FR_TM']), axis=1
)

# Drop rows where Light_Level couldn't be calculated
crime_data = crime_data.dropna(subset=['Light_Level'])

# # Print the first few rows to verify the results
# print(crime_data)

# Save the results to a CSV file
crime_data.to_csv('NYC_crime_s.csv', index=False)

