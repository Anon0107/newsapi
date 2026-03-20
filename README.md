# NewsAPI Headline Fetcher and Digester

### news_fetcher.py
A Python script that fetches the top 5 news headlines by category using the NewsAPI, saves them to a timestamped CSV file, and prints a clean summary to the console.

### news_digest.py
A Python script that fetches top 3 news headlines by multiple categories (up to 3) using the NewsAPI, removing duplicate news and saves them to a timestampted CSV file, then prints a clean summary to the console.

---

## What both scripts does

### news_fetcher.py
- Prompts the user to choose a news category at runtime
- Validates the input and re-prompts if an invalid category is entered
- Calls the NewsAPI with the API key passed securely in the `Authorization` header
- Parses the JSON response and extracts headline, source, URL, published time, and fetch time
- Saves results to a timestamped CSV file using pandas
- Prints a formatted summary to the console
### news_digest.py
- Prompts the user to choose a number between 1-3 and enter the number of news categories at runtime
- Validates the inputs and re-prompts if an invalid number or category is entered
- Calls the NewsAPI with the API key passed securely in the `Authorization` header
- Parses the JSON response and extracts headline, source, URL, published time, and fetch time
- Removes duplicate news and saves results to a timestamped CSV file using pandas
- Prints a formatted summary to the console

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Anon0107/newsapi.git
cd newsapi
```

### 2. Install dependencies

```bash
pip install requests pandas python-dotenv
```

### 3. Get a free API key

Sign up at [newsapi.org](https://newsapi.org) and copy your API key.

### 4. Create a `.env` file

Create a file called `.env` in the project root:

```
NEWS_API_KEY=your_actual_key_here
```

Never commit this file. It is already listed in `.gitignore`.

### 5. Run the script

```bash
python news_fetcher.py
```
or
```bash
python news_digest.py
```
