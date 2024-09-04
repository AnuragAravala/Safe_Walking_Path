import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('NYC_crime_with_streetlight.csv')

# Round Latitude and Longitude to 4 decimal places
df['Rounded_Latitude'] = df['Latitude'].round(4)
df['Rounded_Longitude'] = df['Longitude'].round(4)

# Extract the month from CMPLNT_FR_DT
df['Month'] = pd.to_datetime(df['CMPLNT_FR_DT']).dt.month

# Create 6 segments based on the month
def month_to_segment(month):
    if month in [1, 2]:
        return 'Jan-Feb'
    elif month in [3, 4]:
        return 'Mar-Apr'
    elif month in [5, 6]:
        return 'May-Jun'
    elif month in [7, 8]:
        return 'Jul-Aug'
    elif month in [9, 10]:
        return 'Sep-Oct'
    else:
        return 'Nov-Dec'

df['Month_Segment'] = df['Month'].apply(month_to_segment)

# Define the average percentage of the day that is daylight, twilight, and darkness
daylight_percentage = 0.5110
twilight_percentage = 0.0539
darkness_percentage = 0.4351

# # Function to normalize counts based on light level
# def normalize_count(row):
#     if row['Light_Level'] == 1:
#         return row['Count'] / daylight_percentage
#     elif row['Light_Level'] == 0.5:
#         return row['Count'] / twilight_percentage
#     else:
#         return row['Count'] / darkness_percentage

# Group by the rounded latitude and longitude, daylight condition (Light_Level), streetlight, and month segment
grouped_df = df.groupby(['Rounded_Latitude', 'Rounded_Longitude', 'Month_Segment']).size().reset_index(name='Count')

# # Normalize the counts
# grouped_df['Normalized_Count'] = grouped_df.apply(normalize_count, axis=1)

# Calculate statistical measures (mean, Q1, Q3, and other percentiles) for the normalized counts
mean_count = grouped_df['Count'].mean()
q1 = grouped_df['Count'].quantile(0.25)
q3 = grouped_df['Count'].quantile(0.75)
q31 = grouped_df['Count'].quantile(0.90)
q32 = grouped_df['Count'].quantile(0.95)
q33 = grouped_df['Count'].quantile(0.99)
q34 = grouped_df['Count'].quantile(0.999)
q35 = grouped_df['Count'].quantile(0.9999)

# Display the results
print("Grouped Data:\n", grouped_df)
print("\nStatistics:")
print(f"Mean Count: {mean_count:.4f}")
print(f"Q1 (25th percentile): {q1:.4f}")
print(f"Q3 (75th percentile): {q3:.4f}")
print(f"Q31 (90th percentile): {q31:.4f}")
print(f"Q32 (95th percentile): {q32:.4f}")
print(f"Q33 (99th percentile): {q33:.4f}")
print(f"Q34 (99.9th percentile): {q34:.4f}")
print(f"Q35 (99.99th percentile): {q35:.4f}")

# Save the DataFrame to a CSV file
# grouped_df.to_csv('grouped_data2.csv', index=False)

# Calculate and print the average normalized count for each month segment
average_per_month_segment = grouped_df.groupby('Month_Segment')['Count'].mean().reset_index()

# Display the average for each month segment
print("Average Normalized Count per Month Segment:")
print(average_per_month_segment)