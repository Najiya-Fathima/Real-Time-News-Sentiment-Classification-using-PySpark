# data_producer.py

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from newsapi import NewsApiClient
from requests.exceptions import ReadTimeout # Import the specific exception

load_dotenv()
api_key = os.getenv('NEWS_API')
if not api_key:
    raise ValueError('NEWS API KEY not found in the environment variable')

newsapi = NewsApiClient(api_key=api_key)

# Create a directory to simulate a data stream
stream_dir = "news_stream"
os.makedirs(stream_dir, exist_ok=True)

print("Starting data producer. Press Ctrl+C to stop.")
try:
    while True:
        try:
            # --- This is the new, resilient block ---
            print(f"[{datetime.now()}] Fetching new headlines...")
            top_headlines = newsapi.get_top_headlines(sources='bbc-news')
            
            # This part only runs if the above line succeeds
            titles = [article['title'] for article in top_headlines['articles']]
            file_name = f"headlines_{int(time.time())}.json"
            file_path = os.path.join(stream_dir, file_name)
            with open(file_path, "w") as f:
                json.dump({"headlines": titles}, f)

            print(f"Saved {len(titles)} headlines to {file_path}")

        except ReadTimeout:
            # This block runs if a timeout occurs
            print(f"[{datetime.now()}] Read timeout occurred. Retrying in 30 seconds...")
        
        # This sleep happens regardless of success or failure
        time.sleep(30) # Wait 30 seconds before the next attempt

except KeyboardInterrupt:
    print("\nData producer stopped.")