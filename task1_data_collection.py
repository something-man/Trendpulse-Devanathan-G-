import requests
import time
import json
from datetime import datetime
from pathlib import Path


# Hacker News API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
BEST_STORIES_URL = "https://hacker-news.firebaseio.com/v0/beststories.json"
NEW_STORIES_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}"

headers = {
    "User-Agent": "TrendPulse/1.0"
}


# Keywords for each category
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


def get_story_ids(url):
    """Fetch a list of story IDs from Hacker News."""
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print("Failed to fetch story IDs:", error)
        return []


def fetch_story(story_id):
    """Fetch one Hacker News story safely."""
    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        story = response.json()

        if not story or story.get("type") != "story":
            return None

        title = story.get("title", "")

        if not title:
            return None

        return {
            "post_id": story.get("id"),
            "title": title,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "")
        }

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


# Fetch the first 500 top stories as required
top_story_ids = get_story_ids(TOP_STORIES_URL)[:500]

print(f"Fetched {len(top_story_ids)} top story IDs.")


# Fetch story details
stories = []

for story_id in top_story_ids:
    story = fetch_story(story_id)

    if story is not None:
        stories.append(story)

print(f"Successfully fetched {len(stories)} stories.")


# Track category limits
category_counts = {
    category: 0
    for category in categories
}

final_stories = []


def find_category(title):
    """Return the strongest available category match."""

    title_lower = title.lower()
    matching_categories = []

    for category, keywords in categories.items():

        matches = sum(
            keyword.lower() in title_lower
            for keyword in keywords
        )

        if matches > 0:
            matching_categories.append(
                (category, matches)
            )

    if not matching_categories:
        return None

    matching_categories.sort(
        key=lambda item: item[1],
        reverse=True
    )

    # Use the strongest category that has room.
    for category, _ in matching_categories:
        if category_counts[category] < 25:
            return category

    return None


def add_stories(story_list):
    """Categorise stories and add them to the final dataset."""

    for story in story_list:

        if len(final_stories) >= 100:
            break

        category = find_category(story["title"])

        if category is None:
            continue

        story_data = {
            "post_id": story["post_id"],
            "title": story["title"],
            "category": category,
            "score": story["score"],
            "num_comments": story["num_comments"],
            "author": story["author"],
            "collected_at": datetime.now().isoformat()
        }

        final_stories.append(story_data)
        category_counts[category] += 1


# Categorise the first 500 top stories
add_stories(stories)


# If fewer than 100 stories are found, check best stories.
if len(final_stories) < 100:

    print(
        f"\nOnly {len(final_stories)} matching stories "
        "were found in the first 500 top stories."
    )
    print("Checking additional Hacker News stories...")

    best_story_ids = get_story_ids(BEST_STORIES_URL)

    existing_ids = set(top_story_ids)

    additional_best_ids = [
        story_id
        for story_id in best_story_ids
        if story_id not in existing_ids
    ]

    for story_id in additional_best_ids:

        if len(final_stories) >= 100:
            break

        story = fetch_story(story_id)

        if story is not None:
            add_stories([story])


# If still fewer than 100, check new stories.
if len(final_stories) < 100:

    print(
        f"Still only {len(final_stories)} stories."
    )
    print("Checking additional new Hacker News stories...")

    new_story_ids = get_story_ids(NEW_STORIES_URL)

    existing_ids = {
        story["post_id"]
        for story in final_stories
    }

    for story_id in new_story_ids:

        if len(final_stories) >= 100:
            break

        if story_id in existing_ids:
            continue

        story = fetch_story(story_id)

        if story is not None:
            add_stories([story])


# Print category totals.
print()
print("Category Results")
print("-------------------------")

for category in categories:

    print(
        f"{category}: "
        f"{category_counts[category]} stories collected"
    )

    time.sleep(2)


# Create data folder.
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)


# Create date-based output filename.
date_string = datetime.now().strftime("%Y%m%d")
output_file = data_folder / f"trends_{date_string}.json"


# Save collected stories as JSON.
with open(output_file, "w", encoding="utf-8") as file:

    json.dump(
        final_stories,
        file,
        indent=2,
        ensure_ascii=False
    )


print()
print(f"Collected {len(final_stories)} stories.")
print(f"Saved to {output_file}")
