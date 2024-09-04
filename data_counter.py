import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('NYC_crime_with_streetlight.csv')

# Ensure relevant columns are present and handle missing data if necessary
df['ADDR_PCT_CD'] = df['ADDR_PCT_CD'].fillna('Unknown')
df['Light_Level'] = df['Light_Level'].fillna(0)
df['Streetlight'] = df['Streetlight'].fillna(0)

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

# Group by precinct (ADDR_PCT_CD), daylight condition (Light_Level), streetlight, and month segment, then count occurrences
count_df = df.groupby(['ADDR_PCT_CD', 'Light_Level', 'Streetlight', 'Month_Segment']).size().reset_index(name='Count')

# Calculate the average, Q1, and Q3
average_count = count_df['Count'].mean()
q1 = count_df['Count'].quantile(0.25)
q3 = count_df['Count'].quantile(0.75)

# Display the results
print("Grouped Data:\n", count_df)
print("\nStatistics:")
print(f"Average Count: {average_count}")
print(f"Q1 (25th percentile): {q1}")
print(f"Q3 (75th percentile): {q3}")