import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the CSV file
df = pd.read_csv("report.csv")

# Convert 'Start Time' and 'End Time' columns to datetime
df["Start Time"] = pd.to_datetime(df["Start Time"], format="%H:%M:%S")
df["End Time"] = pd.to_datetime(df["End Time"], format="%H:%M:%S")

# Create a dictionary to hold the total minutes per hour
hourly_activity = {i: 0 for i in range(24)}

# Iterate through each row and calculate the time spent in each hour
for index, row in df.iterrows():
    start_time = row["Start Time"]
    end_time = row["End Time"]

    # Get the hour and minute for start and end times
    start_hour = start_time.hour
    start_minute = start_time.minute
    end_hour = end_time.hour
    end_minute = end_time.minute

    # Calculate total minutes
    total_minutes = (end_time - start_time).total_seconds() / 60

    if start_hour == end_hour:
        hourly_activity[start_hour] += total_minutes
    else:
        # Add the remaining minutes in the start hour
        remaining_start = 60 - start_minute
        hourly_activity[start_hour] += remaining_start

        # Add full hours
        full_hours = end_hour - start_hour - 1
        if full_hours > 0:
            for hour in range(start_hour + 1, end_hour):
                hourly_activity[hour] += 60

        # Add the minutes in the end hour
        hourly_activity[end_hour] += end_minute

# Create a DataFrame from the hourly activity dictionary
hours_df = pd.DataFrame(
    {"Hour": range(24), "Minutes": [hourly_activity[i] for i in range(24)]}
)

# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(hours_df["Hour"], hours_df["Minutes"], color="skyblue")
plt.title("Most Active Hours of the Day")
plt.xlabel("Hour")
plt.ylabel("Total Minutes")
plt.grid(True)
plt.xticks(range(24))
plt.show()
