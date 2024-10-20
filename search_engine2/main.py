import crawler
import preprocessor
import indexer
import query_engine
import json


def execute_pipeline():
    """Executes the full pipeline from crawling books to querying the index."""

    # Folder and file paths
    folder_path = "datalake_storage"
    processed_json_path = "output_books.json"

    # Crawl and download books
    print("Step 1: Crawling and downloading books...")
    books_to_crawl = 20
    crawler.run_crawler(books_to_crawl)

    # Process downloaded books and store them in JSON
    print("Step 2: Processing downloaded books...")
    preprocessor.run_book_processing(folder_path, processed_json_path)

    # Create an inverted index using a hashmap
    print("Step 3: Building inverted index from processed data...")
    indexer.create_inverted_index(processed_json_path)

    # Create a metadata-based index for additional querying
    print("Step 4: Building metadata index...")
    indexer.create_metadata_index(processed_json_path)

    # Initialize the query engine and search the inverted index
    print("Step 5: Searching the inverted index...")
    engine = query_engine.QueryEngine('inverted_index.json')
    search_term = "freedom"
    search_results = engine.query(search_term)

    print(f"Results for the search term '{search_term}':")
    if search_results:
        for result in search_results:
            print(result)
    else:
        print(f"No results found for '{search_term}'.")


if __name__ == "__main__":
    execute_pipeline()
