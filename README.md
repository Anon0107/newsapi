# NewsAPI Headline Fetcher

A Python script that fetches the top 5 news headlines by category using the NewsAPI, saves them to a timestamped CSV file, and prints a clean summary to the console.

Built as part of a 5-month AI Automation Engineer roadmap — Day 2 focus: API authentication, `.env` secret management, and structured data export.

---

## What it does

- Prompts the user to choose a news category at runtime
- Validates the input and re-prompts if an invalid category is entered
- Calls the NewsAPI with the API key passed securely in the `Authorization` header
- Parses the JSON response and extracts headline, source, URL, published time, and fetch time
- Saves results to a timestamped CSV file using pandas
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
