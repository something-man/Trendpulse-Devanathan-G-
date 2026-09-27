import pandas as pd
import numpy as np
from pathlib import Path


# Load the cleaned CSV created in Task 2.
data_folder = Path("data")
input_file = data_folder / "trends_clean.csv"

df = pd.read_csv(input_file)

print(f"Loaded data: {df.shape}")


# Display the first five rows.
print()
print("First 5 rows:")
print(df.head())


# Calculate average score and average comments.
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print()
print(f"Average score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# Convert the score column to a NumPy array for analysis.
scores = df["score"].to_numpy()


# Calculate the requested NumPy statistics.
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print()
print("--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")


# Find the category containing the most stories.
category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print()
print(
    f"Most stories in: {most_common_category} "
    f"({most_common_count} stories)"
)


# Find the story with the highest number of comments.
most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[
    most_commented_index, "title"
]

most_commented_count = df.loc[
    most_commented_index, "num_comments"
]

print()
print(
    f'Most commented story: "{most_commented_title}" '
    f"— {most_commented_count} comments"
)


# Add engagement: comments received per score point.
df["engagement"] = (
    df["num_comments"] /
    (df["score"] + 1)
)


# Mark stories whose score is above the average score.
df["is_popular"] = (
    df["score"] > average_score
)


# Save the analysed data for Task 4.
output_file = data_folder / "trends_analysed.csv"

df.to_csv(
    output_file,
    index=False
)

print()
print(f"Saved to {output_file}")
