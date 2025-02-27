# Python Gutenberg Search Engine v1.0

## Introduction
This project is a sophisticated search engine designed to provide efficient search capabilities over a large collection of texts from Project Gutenberg. It leverages the inverted index algorithm to ensure fast and accurate search results.

## Functionalities
- **Crawling and Downloading Books**: Downloads a specified number of books from Project Gutenberg.
- **Processing Downloaded Books**: Processes the downloaded books and stores them in a JSON format.
- **Building Inverted Index**: Creates an inverted index using the processed data.
- **Building Metadata Index**: Additionally creates a metadata-based index for more advanced querying.
- **Querying the Index**: Searches the inverted index for specified search terms and returns relevant results.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/luis-guillen/Python_Gutenberg_Search-Engine_v1.0.git
   cd Python_Gutenberg_Search-Engine_v1.0
   ```
2. Install the necessary dependencies (If `requirements.txt` is available):
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To use the search engine, run the main script and follow the instructions:
```bash
python search_engine2/main.py
```
This will execute the full pipeline from crawling books to querying the index.

## Pipeline Overview
1. **Crawling**: The script starts by crawling and downloading books.
2. **Processing**: It processes the downloaded books and stores them in JSON format.
3. **Indexing**: The script builds an inverted index and a metadata index from the processed data.
4. **Querying**: Finally, it initializes the query engine and searches the inverted index for the specified search terms.

## Example
Here is an example of how to use the search engine:
```python
# Initialize the query engine with the inverted index
engine = query_engine.QueryEngine('inverted_index.json')
# Define the search term
search_term = "freedom"
# Perform the search
search_results = engine.query(search_term)
# Display the results
if search_results:
    for result in search_results:
        print(result)
else:
    print(f"No results found for '{search_term}'.")
```

## License
This project is licensed under the GNU.

## Contributors
- Luis Guillen

For any additional information or support, please contact me via the provided means.
