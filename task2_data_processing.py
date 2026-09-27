import pandas as pd
from pathlib import Path


# Find the JSON file created by Task 1.
data_folder = Path("data")
json_files = sorted(data_folder.glob("trends_*.json"))

if not json_files:
    raise FileNotFoundError(
        "No trends_YYYYMMDD.json file was found in the data folder."
    )

# Use the latest JSON file.
input_file = json_files[-1]

# Load the JSON data into a Pandas DataFrame.
df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# Remove duplicate stories using post_id.
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# Convert score and num_comments to numeric values.
# Invalid values are converted to NaN.
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
    df["num_comments"], errors="coerce"
)


# Remove rows where required fields are missing.
df = df.dropna(
    subset=["post_id", "title", "score"]
)

print(f"After removing nulls: {len(df)}")


# Replace missing comment counts with zero.
# Then convert both numeric columns to integers.
df["num_comments"] = df["num_comments"].fillna(0)

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# Remove stories with a score below 5.
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# Remove extra whitespace from story titles.
df["title"] = df["title"].str.strip()


# Save the cleaned DataFrame as a CSV file.
output_file = data_folder / "trends_clean.csv"

df.to_csv(
    output_file,
    index=False
)

print()
print(f"Saved {len(df)} rows to {output_file}")


# Print the number of stories in each category.
print()
print("Stories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")
