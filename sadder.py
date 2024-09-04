import pandas as pd

# Load the NYC crime data and unique locations data
crime_data = pd.read_csv("NYC_crime_s.csv", dtype=str, low_memory=False)
unique_locations = pd.read_csv("unique_locations_sorted.csv", dtype=str, low_memory=False)

# Ensure latitude and longitude columns are in float format and rounded to 4 decimal places
crime_data['Latitude'] = pd.to_numeric(crime_data['Latitude']).round(4)
crime_data['Longitude'] = pd.to_numeric(crime_data['Longitude']).round(4)

unique_locations['Latitude'] = pd.to_numeric(unique_locations['Latitude']).round(4)
unique_locations['Longitude'] = pd.to_numeric(unique_locations['Longitude']).round(4)

# Merge the crime data with the unique locations data on latitude and longitude
merged_data = pd.merge(crime_data, unique_locations, on=['Latitude', 'Longitude'], how='left', indicator=True)

# Add a 'Streetlight' column where the merge was successful
merged_data['Streetlight'] = merged_data['_merge'].apply(lambda x: 1 if x == 'both' else 0)

# Drop the '_merge' column as it's no longer needed
merged_data = merged_data.drop(columns=['_merge'])

# Save the resulting data to a new CSV file
merged_data.to_csv('NYC_crime_with_streetlight.csv', index=False)

# Print the first few rows to verify the results
print(merged_data.head())
