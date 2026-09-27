import pandas as pd

import matplotlib.pyplot as plt

from pathlib import Path





# ---------------------------------------------------------

# Step 1: Load the analysed CSV

# ---------------------------------------------------------



data_folder = Path("data")

output_folder = Path("outputs")



# Create outputs folder if it does not exist.

output_folder.mkdir(exist_ok=True)



input_file = data_folder / "trends_analysed.csv"



df = pd.read_csv(input_file)



print(f"Loaded data: {df.shape}")





# ---------------------------------------------------------

# Chart 1: Top 10 Stories by Score

# ---------------------------------------------------------



# Sort stories by score and select the top 10.

top_10 = df.nlargest(10, "score").sort_values("score")



# Shorten long titles for easier display.

short_titles = top_10["title"].apply(

    lambda title: title[:50] + "..."

    if len(title) > 50

    else title

)



plt.figure(figsize=(10, 7))



plt.barh(

    short_titles,

    top_10["score"]

)



plt.title("Top 10 Stories by Score")

plt.xlabel("Score")

plt.ylabel("Story Title")



plt.tight_layout()



# Save before showing.

plt.savefig(

    output_folder / "chart1_top_stories.png",

    dpi=150,

    bbox_inches="tight"

)



plt.show()

plt.close()





# ---------------------------------------------------------

# Chart 2: Stories per Category

# ---------------------------------------------------------



category_counts = df["category"].value_counts()



plt.figure(figsize=(9, 6))



# Give each bar a different colour.

plt.bar(

    category_counts.index,

    category_counts.values,

    color=[

        "blue",

        "green",

        "orange",

        "red",

        "purple"

    ][:len(category_counts)]

)



plt.title("Stories per Category")

plt.xlabel("Category")

plt.ylabel("Number of Stories")



plt.xticks(rotation=20)



plt.tight_layout()



# Save before showing.

plt.savefig(

    output_folder / "chart2_categories.png",

    dpi=150,

    bbox_inches="tight"

)



plt.show()

plt.close()





# ---------------------------------------------------------

# Chart 3: Score vs Comments

# ---------------------------------------------------------



plt.figure(figsize=(10, 7))



# Separate popular and non-popular stories.

popular = df[df["is_popular"] == True]

not_popular = df[df["is_popular"] == False]



plt.scatter(

    not_popular["score"],

    not_popular["num_comments"],

    label="Not Popular"

)



plt.scatter(

    popular["score"],

    popular["num_comments"],

    label="Popular"

)



plt.title("Score vs Comments")

plt.xlabel("Score")

plt.ylabel("Number of Comments")

plt.legend()



plt.tight_layout()



# Save before showing.

plt.savefig(

    output_folder / "chart3_scatter.png",

    dpi=150,

    bbox_inches="tight"

)



plt.show()

plt.close()





# ---------------------------------------------------------

# Bonus: TrendPulse Dashboard

# ---------------------------------------------------------



fig, axes = plt.subplots(

    2,

    2,

    figsize=(18, 12)

)



fig.suptitle(

    "TrendPulse Dashboard",

    fontsize=18

)





# Dashboard Chart 1

axes[0, 0].barh(

    short_titles,

    top_10["score"]

)



axes[0, 0].set_title(

    "Top 10 Stories by Score"

)



axes[0, 0].set_xlabel("Score")

axes[0, 0].set_ylabel("Story Title")





# Dashboard Chart 2

axes[0, 1].bar(

    category_counts.index,

    category_counts.values,

    color=[

        "blue",

        "green",

        "orange",

        "red",

        "purple"

    ][:len(category_counts)]

)



axes[0, 1].set_title(

    "Stories per Category"

)



axes[0, 1].set_xlabel("Category")

axes[0, 1].set_ylabel("Number of Stories")



axes[0, 1].tick_params(

    axis="x",

    rotation=20

)





# Dashboard Chart 3

axes[1, 0].scatter(

    not_popular["score"],

    not_popular["num_comments"],

    label="Not Popular"

)



axes[1, 0].scatter(

    popular["score"],

    popular["num_comments"],

    label="Popular"

)



axes[1, 0].set_title(

    "Score vs Comments"

)



axes[1, 0].set_xlabel("Score")

axes[1, 0].set_ylabel("Number of Comments")

axes[1, 0].legend()





# Remove the unused fourth subplot.

axes[1, 1].axis("off")





plt.tight_layout(

    rect=[0, 0, 1, 0.95]

)



# Save the dashboard.

plt.savefig(

    output_folder / "dashboard.png",

    dpi=150,

    bbox_inches="tight"

)



plt.show()

plt.close()





# ---------------------------------------------------------

# Final confirmation

# ---------------------------------------------------------



print()

print("Visualization files created:")



print(

    output_folder / "chart1_top_stories.png"

)



print(

    output_folder / "chart2_categories.png"

)



print(

    output_folder / "chart3_scatter.png"

)



print(

    output_folder / "dashboard.png"

)