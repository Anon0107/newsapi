import os
import requests
import logging
import time
import sys
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Logging setup
logging.basicConfig(level = logging.DEBUG, # Change to DEBUG for development mode,INFO for production mode
                    format = '%(asctime)s | %(levelname)-8s | %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler('news_saver.log'),
                              logging.StreamHandler()
                        ])
logger = logging.getLogger(__name__)
# Get and verify for valid user inputs
def get_user_inputs():
    categories = ['business','entertainment','general','health','science','sports','technology']
    input_cat = ''
    while input_cat not in categories:
        input_cat = input('Enter a category(business/entertainment/general(default if no input)/health/science/sports/technology): ').lower()
        if not input_cat:
            input_cat = 'general'
            logger.info(f'Category: {input_cat} entered by user')
        elif input_cat not in categories:
            print('Please enter a valid category or leave it blank')
        else:
            logger.info(f'Category {input_cat} entered by user')
    while True:
        try:
            input_page = int(input('Enter a page count(1-5): '))
            if input_page in [num for num in range(1,6)]:
                logger.info(f'Page count: {input_page} entered by user')
                break
            else:
                print('Please enter a number in 1-5')
        except ValueError:
            print('Please enter a number')
    return (input_cat,input_page)
# Fetch articles by page number
def fetch_page(category,page):
    params = {
        'category' : category,
        'page'     : page,
        'language' : 'en'
    }
    # Error handling and retry up to 2 times
    for attempt in range(1,3):
        try:
            response = requests.get(url,headers = headers,params = params,timeout = 10)
            response.raise_for_status()
            data = response.json()
            break
        except requests.exceptions.HTTPError as e:
            logger.exception(f'Attempt {attempt} for page {page}: HTTP Error: {e}')
        except requests.exceptions.ConnectionError as e:
            logger.warning(f'Attempt {attempt} for page {page}: No Internet connection')
        except requests.exceptions.Timeout as e:
            logger.warning(f'Attempt {attempt} for page {page}: Connection timeout')
        except requests.exceptions.RequestException as e:
            logger.exception(f'Attempt {attempt} for page {page}: Unexpected error: {e}')
        if attempt == 1:
            logger.warning(f'Retrying in 2 seconds')
            time.sleep(2)
    else:
        data = None
    return data
# Fetch all articles from every page
def fetch_all_pages(category,page_count):
    result = []
    for page in range(1,page_count + 1):
        data = fetch_page(category,page)
        if data is None:
            logger.error(f'NewsAPI down for page {page}')
        elif not data:
            logger.warning(f'No news found for page {page}')
        else:
            articles = data['articles']
            rows = []
            for article in articles: # Extract useful information of articles
                rows.append({
                    'title'      : article.get('title',''),
                    'source'     : article['source']['name'],
                    'author'     : article.get('author',''),
                    'url'        : article['url'],
                    'publishedAt': article['publishedAt']
                })
            result.extend(rows)
            logger.debug(f'Page {page} loaded')
    return result

# Extract API key from .env file
load_dotenv()
API_KEY = os.getenv('NEWS_API_KEY')
url = 'https://newsapi.org/v2/top-headlines'
headers = {
    'Authorization' : f'Bearer {API_KEY}'
    }
# Check for API key
if not API_KEY:
    logger.critical("NewsAPI key not found in .env, exiting")
    sys.exit(1)
# Main script that runs everything and saves file
def main():
    category,page_count = get_user_inputs()
    result = fetch_all_pages(category,page_count)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    if not result:
        logger.critical(f'No news fetched at {current_time}, exiting')
        sys.exit(1)
    else:
        df = pd.DataFrame(result)
        filename = f'{category}_news_{current_time}.csv'
        df.to_csv(filename,index = False,encoding='utf-8-sig') # Saves csv file
        logger.info(f'File {filename} saved')
        
if __name__  == '__main__' :
    main()
            
        