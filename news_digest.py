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
categories = ['business','entertainment','general','health','science','sports','technology']
cat_num = 0
# Verify input categories
while cat_num not in [1,2,3]:
    try:
        cat_num = int(input('How many categories? (1-3): '))
        if cat_num not in [1,2,3]:
            print('Please enter a number from 1-3')
    except ValueError:
        print(f'Please enter a number')
        continue
cat_input = []
while len(cat_input) != cat_num:
    cat = input(f'Enter category {len(cat_input)+1}: ')
    if cat.lower() not in categories:
        print(f'Invalid category entered: {cat}')
    else:
        cat_input.append(cat.lower())
headers = {
    'Authorization': f'Bearer {API_KEY}'
}
fetched_at = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
rows = []
for category in cat_input: # Loop through categories requested
    params = {
        'category': category,
        'language': "en",
        'pageSize': 3,
    }
    try:
        response = requests.get(BASE_URL,headers = headers,params = params) # GET with API key set in headers and parameters specified
        response.raise_for_status() # Error handling
        data = response.json()
        articles = data['articles']
        for article in articles:
            rows.append({
                'category':     category,
                'headline':     article['title'],
                'source':       article['source']['name'],
                'url':          article['url'],
                'published_at': article['publishedAt'],
                'fetched_at':   fetched_at
            })
    except requests.exceptions.ConnectionError:
        print(f'Invalid Internet connection, {category} headlines not loaded')
        continue
    except requests.exceptions.HTTPError as e:
        print(f'HTTP Error: {e}, {category} headlines not loaded')
        continue
df = pd.DataFrame(rows)
filename = f'digest_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
df = df.drop_duplicates(subset = 'url',keep = 'first') # Remove duplicates
num_dupe = len(rows) - df.shape[0]
df.to_csv(filename,index = False) # Save cleaned file
# Print summary
for category in cat_input:
    print(f'{"─"*70}')
    print(f'   TOP 3 {category.upper()} HEADLINES')
    print(f'{"─"*70}')
    for index,row in enumerate(filter(lambda x : x['category'] == category,rows),1):
        print(f'{index}. {row["headline"]}')
        print(f'   Source : {row["source"]}')
        print(f'   URL    : {row["url"]}')
        print(f'   Posted : {row["published_at"]}')
print(f'{"─"*70}')
print(f'Total: {len(rows)} headlines | {num_dupe} duplicate(s) removed')
print(f'Saved to {filename}')