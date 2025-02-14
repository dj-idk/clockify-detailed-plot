import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the CSV file
df = pd.read_csv("report.csv")

# Convert 'Start Time' and 'End Time' columns to datetime
df["Start Time"] = pd.to_datetime(df["Start Time"], format="%H:%M:%S")
df["End Time"] = pd.to_datetime(df["End Time"], format="%H:%M:%S")

# Filter the DataFrame to include only rows where the start time is between 5 AM and 9 PM
df = df[
    (df["Start Time"].dt.hour >= 5)
    & (df["Start Time"].dt.hour <= 21)
    & (df["End Time"].dt.hour >= 5)
    & (df["End Time"].dt.hour <= 21)
]

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

# Filter the DataFrame to include only the time spans between 5 AM and 9 PM
half_hours_df = half_hours_df[
    (half_hours_df["Time Span"] >= "05:00-05:30")
    & (half_hours_df["Time Span"] <= "21:00-21:30")
]

# Sort the DataFrame by Minutes in descending order
sorted_df = half_hours_df.sort_values(by="Minutes", ascending=False)

# Get top 10 most active and least active spans
top_10_most_active = sorted_df.head(10)
top_10_least_active = sorted_df.tail(10)

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot top 10 most active
ax1.bar(top_10_most_active["Time Span"], top_10_most_active["Minutes"], color="skyblue")
ax1.set_title("Top 10 Most Active 30-Minute Spans")
ax1.set_xlabel("Time Span")
ax1.set_ylabel("Total Minutes")
ax1.grid(True)
ax1.tick_params(axis="x", rotation=45)

# Plot top 10 least active
ax2.bar(
    top_10_least_active["Time Span"], top_10_least_active["Minutes"], color="skyblue"
)
ax2.set_title("Top 10 Least Active 30-Minute Spans")
ax2.set_xlabel("Time Span")
ax2.set_ylabel("Total Minutes")
ax2.grid(True)
ax2.tick_params(axis="x", rotation=45)

with open("activity_report.txt", "w") as file:
    file.write("Top Ten Most Active 30 Minutes Spans:\n")
    for i, row in top_10_most_active.iterrows():
        file.write(f"{i + 1}. {row['Time Span']} - {row['Minutes']} minutes\n")

    file.write("\nTop Ten Least Active 30 Minutes Spans:\n")
    for i, row in top_10_least_active.iterrows():
        file.write(f"{i + 1}. {row['Time Span']} - {row['Minutes']} minutes\n")

plt.tight_layout()
plt.show()
