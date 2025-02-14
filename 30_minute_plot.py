import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the CSV file
df = pd.read_csv("report.csv")

# Convert 'Start Time' and 'End Time' columns to datetime
df["Start Time"] = pd.to_datetime(df["Start Time"], format="%H:%M:%S")
df["End Time"] = pd.to_datetime(df["End Time"], format="%H:%M:%S")

# Create a dictionary to hold the total minutes per 30-minute span
# There are 48 possible 30-minute spans in a day (24 hours * 2)
half_hourly_activity = {i: 0 for i in range(48)}

# Iterate through each row and calculate the time spent in each 30-minute span
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

    # Determine the 30-minute span for start time
    start_span = start_hour * 2 + (1 if start_minute >= 30 else 0)
    end_span = end_hour * 2 + (1 if end_minute >= 30 else 0)

    # If start and end spans are the same, add total minutes to that span
    if start_span == end_span:
        half_hourly_activity[start_span] += total_minutes
    else:
        # Add remaining minutes in the start span
        remaining_start = 30 - start_minute if start_minute < 30 else 0
        if remaining_start > 0:
            half_hourly_activity[start_span] += remaining_start

        # Add full 30-minute spans if applicable
        if start_span < end_span - 1:
            full_spans = end_span - start_span - 1
            for span in range(start_span + 1, end_span):
                half_hourly_activity[span] += 30

        # Add remaining minutes in the end span
        remaining_end = end_minute if end_minute >= 30 else 0
        if remaining_end > 0:
            half_hourly_activity[end_span] += remaining_end

# Create a DataFrame from the half-hourly activity dictionary
half_hours_df = pd.DataFrame(
    {
        "Time Span": [
            f"{h:02d}:{m:02d}-{h:02d}:{m+30:02d}"
            for h, m in [(span // 2, 0 if span % 2 == 0 else 30) for span in range(48)]
        ],
        "Minutes": [half_hourly_activity[i] for i in range(48)],
    }
)

# Create the plot
plt.figure(figsize=(15, 6))
plt.bar(half_hours_df["Time Span"], half_hours_df["Minutes"], color="skyblue")
plt.title("Most Active 30-Minute Spans of the Day")
plt.xlabel("Time Span")
plt.ylabel("Total Minutes")
plt.grid(True)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
