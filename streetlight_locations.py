import pandas as pd

# Load the CSV file with error handling and data type specification
streetlight = pd.read_csv("streetlight.csv", dtype=str, low_memory=False)

# Extract unique locations from the 'Location' column
unique_locations = streetlight['Location'].unique()

# Convert to a DataFrame
unique_locations_df = pd.DataFrame(unique_locations, columns=['Location'])

def crop_lat_lon(location):
    if isinstance(location, str):
        try:
            # Strip any extraneous characters and split the location
            lat, lon = location.strip('()').split(',')
            lat, lon = float(lat), float(lon)
            return (round(lat, 4), round(lon, 4))
        except ValueError:
            return None  # Return None if there's an error
    else:
        return None  # Return None if location is not a string

# Apply the cropping function to the 'Location' column
unique_locations_df['Location'] = unique_locations_df['Location'].apply(crop_lat_lon)

# Remove rows where 'Location' is None
unique_locations_df = unique_locations_df.dropna(subset=['Location'])

# Split the 'Location' column into 'Latitude' and 'Longitude'
unique_locations_df[['Latitude', 'Longitude']] = pd.DataFrame(unique_locations_df['Location'].tolist(), index=unique_locations_df.index)

# Drop the original 'Location' column
unique_locations_df = unique_locations_df.drop(columns=['Location'])


# Sort by 'Latitude' as primary and 'Longitude' as secondary
unique_locations_df = unique_locations_df.sort_values(by=['Latitude', 'Longitude'])

# Save the sorted unique locations to a new CSV file
unique_locations_df.to_csv('unique_locations_sorted.csv', index=False)