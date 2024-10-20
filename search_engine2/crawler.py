import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

# Configuration for scraping
ROOT_URL = "https://www.gutenberg.org"
TOP_BOOKS_URL = f"{ROOT_URL}/browse/scores/top"
STORAGE_DIR = "datalake_storage"


# Ensure the directory exists for storing the books
def setup_storage(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    print(f"Storage directory is set to: {directory}")


# Retrieve book URLs from the top books section
def retrieve_book_urls():
    print("Fetching the top books from Gutenberg...")
    try:
        page_response = requests.get(TOP_BOOKS_URL)
        page_response.raise_for_status()
        soup = BeautifulSoup(page_response.content, 'html.parser')

        # Extract book links
        urls = []
        for anchor in soup.find_all('a', href=True):
            if anchor['href'].startswith('/ebooks/'):
                urls.append(f"{ROOT_URL}{anchor['href']}")

        print(f"Found {len(urls)} book links.")
        return urls
    except Exception as error:
        print(f"Failed to retrieve book links: {error}")
        return []


# Function to attempt downloading the book in different formats
def fetch_book_content(book_identifier):
    extensions = ['txt', 'html', 'epub', 'mobi']
    base_url = f"https://gutenberg.org/cache/epub/{book_identifier}/pg{book_identifier}"

    # Try downloading the book in multiple formats
    for ext in extensions:
        download_url = f"{base_url}.{ext}"
        file_path = os.path.join(STORAGE_DIR, f"{book_identifier}.{ext}")

        # Check if the file already exists
        if os.path.isfile(file_path):
            print(f"{book_identifier}.{ext} already exists, skipping download.")
            return

        print(f"Trying to download book {book_identifier} from {download_url}...")
        try:
            response = requests.get(download_url)
            response.raise_for_status()
            # Save the file to the storage directory
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded {book_identifier} in {ext} format.")
            return
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {download_url}: {e}")

    print(f"Could not download book {book_identifier} in any supported format.")


# Crawl through books and initiate download process
def run_crawler(book_limit):
    # Initialize storage
    setup_storage(STORAGE_DIR)

    # Retrieve all available book links
    book_urls = retrieve_book_urls()
    if not book_urls:
        print("No book URLs were found, exiting.")
        return

    # Extract book IDs from the URLs
    book_ids = [url.split('/')[-1] for url in book_urls]

    # Parallel download using a thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        for book_id in book_ids[:book_limit]:
            executor.submit(fetch_book_content, book_id)
            time.sleep(0.5)  # Throttling requests to avoid overwhelming the server

