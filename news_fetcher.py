import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise ValueError("NEWS_API_KEY not found. Check your .env file.")

BASE_URL = "https://newsapi.org/v2/top-headlines"

categories = ['business','entertainment','general','health','science','sports','technology']
category = input('Enter a category(business/entertainment/general/health/science/sports/technology): ')
while category.lower() not in categories:
    print(f'Invalid category entered: {category}')
    category = input('Enter a category(business/entertainment/general/health/science/sports/technology): ')
category = category.lower()
params = {
    "category": category,
    "language": "en",
    "pageSize": 5,
}
headers = {
    "Authorization": f"Bearer {API_KEY}"
}
try: 
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f'HTTP error: {e}')
    raise
except requests.exceptions.ConnectionError:
    print(f'No internet connection')
    raise

data = response.json()
articles = data["articles"]

rows = []
for article in articles:
    rows.append({
        "headline":     article["title"],
        "source":       article["source"]["name"],
        "url":          article["url"],
        "published_at": article["publishedAt"],
        "fetched_at":   datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    })
df = pd.DataFrame(rows)
filename = f"{category}_headlines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(filename, index=False)

# Print summary
print(f"{'─'*70}")
print(f"  TOP 5 {category.upper()} HEADLINES  ({datetime.now().strftime('%d %b %Y')})  ({data['totalResults']} results found)")
print(f"{'─'*70}")

for i, row in enumerate(rows, 1):
    print(f"\n{i}. {row['headline']}")
    print(f"   Source : {row['source']}")
    print(f"   URL    : {row['url']}")
    print(f"   Posted : {row['published_at']}")

print(f"\n{'─'*70}")
print(f"Saved to {filename}")