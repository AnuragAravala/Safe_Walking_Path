from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun

# Define the location (New York City in this case)
nyc = LocationInfo("New York", "USA")
nyc_tz = nyc.timezone

# Initialize totals for each period
total_daylight = 0
total_twilight = 0
total_darkness = 0
num_days = 365  # Number of days in the year

# Loop over each day in the year
for day_offset in range(num_days):
    current_date = datetime(2024, 1, 1) + timedelta(days=day_offset)
    
    # Get sunrise, sunset, and twilight times
    s = sun(nyc.observer, date=current_date.date(), tzinfo=nyc_tz)
    sunrise = s['sunrise'].time()
    sunset = s['sunset'].time()
    civil_twilight_start = s['dawn'].time()
    civil_twilight_end = s['dusk'].time()
    
    # Calculate durations in minutes
    daylight_duration = (datetime.combine(current_date.date(), sunset) - datetime.combine(current_date.date(), sunrise)).total_seconds() / 60
    twilight_duration = ((datetime.combine(current_date.date(), sunrise) - datetime.combine(current_date.date(), civil_twilight_start)) +
                         (datetime.combine(current_date.date(), civil_twilight_end) - datetime.combine(current_date.date(), sunset))).total_seconds() / 60
    darkness_duration = 24 * 60 - (daylight_duration + twilight_duration)  # Total minutes in a day minus daylight and twilight
    
    # Accumulate the totals
    total_daylight += daylight_duration
    total_twilight += twilight_duration
    total_darkness += darkness_duration

# Calculate average percentages
average_daylight_percentage = (total_daylight / (num_days * 24 * 60)) * 100
average_twilight_percentage = (total_twilight / (num_days * 24 * 60)) * 100
average_darkness_percentage = (total_darkness / (num_days * 24 * 60)) * 100

# Display the results
print(f"Average Daylight: {average_daylight_percentage:.2f}%")
print(f"Average Twilight: {average_twilight_percentage:.2f}%")
print(f"Average Darkness: {average_darkness_percentage:.2f}%")
