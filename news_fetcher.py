import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
load_dotenv() # Load .env file
API_KEY = os.getenv('NEWS_API_KEY') # Access API key

if not API_KEY:
    raise ValueError('NEWS_API_KEY not found. Check your .env file.')
    # Check if key is present
BASE_URL = 'https://newsapi.org/v2/top-headlines'
# Verify input category
categories = ['business','entertainment','general','health','science','sports','technology']
category = input('Enter a category(business/entertainment/general/health/science/sports/technology): ')
while category.lower() not in categories:
    print(f'Invalid category entered: {category}')
    category = input('Enter a category(business/entertainment/general/health/science/sports/technology): ')
category = category.lower()
params = {
    'category': category,
    'language': 'en',
    'pageSize': 5,
}
headers = {
    'Authorization': f'Bearer {API_KEY}'
}
try: 
    response = requests.get(BASE_URL, headers=headers, params=params) ## GET with API key set in headers and parameters specified
    response.raise_for_status() # Error handling
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f'HTTP error: {e}')
    raise
except requests.exceptions.ConnectionError:
    print(f'No internet connection')
    raise

articles = data['articles']
fetched_at = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
rows = []
for article in articles:
    rows.append({
        'headline':     article['title'],
        'source':       article['source']['name'],
        'url':          article['url'],
        'published_at': article['publishedAt'],
        'fetched_at':   fetched_at
    })
df = pd.DataFrame(rows)
filename = f'{category}_headlines_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
df.to_csv(filename, index=False) # Save file

# Print summary
print(f'{"─"*70}')
print(f'  TOP 5 {category.upper()} HEADLINES  ({datetime.now().strftime("%d %b %Y")})  ({data["totalResults"]} results found)')
print(f'{"─"*70}')

for i, row in enumerate(rows, 1):
    print(f'\n{i}. {row["headline"]}')
    print(f'   Source : {row["source"]}')
    print(f'   URL    : {row["url"]}')
    print(f'   Posted : {row["published_at"]}')

print(f'\n{"─"*70}')
print(f'Saved to {filename}')