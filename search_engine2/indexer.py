import json

# Simple Inverted Indexer using HashMap (Dictionary)
def create_inverted_index(json_file):
    """Creates an inverted index using a simple dictionary (hashmap) structure."""
    inverted_index = {}

    # Open and read the JSON file containing processed book data
    with open(json_file, 'r', encoding='utf-8') as file:
        books = json.load(file)

    # Iterate over each book in the JSON file
    for book in books:
        book_id = book['ebook_number']
        if book_id is None:
            continue

        # Iterate over each word in the book and build the inverted index
        for word in book['words']:
            word = word.lower()  # Normalize word to lowercase
            if word in inverted_index:
                # If the word is already in the index, append the book ID to its list
                if book_id not in inverted_index[word]:
                    inverted_index[word].append(book_id)
            else:
                # If the word is not in the index, create a new entry with the book ID
                inverted_index[word] = [book_id]

    # Write the inverted index to a JSON file
    with open('inverted_index.json', 'w', encoding='utf-8') as file:
        json.dump(inverted_index, file, indent=4)

    return inverted_index

# Function to create an index for metadata fields like title, author, etc.
def create_metadata_index(json_file):
    """Creates a metadata index for fields like title, author, release date, and language."""
    metadata_index = {}

    # Open and read the JSON file containing book data
    with open(json_file, 'r', encoding='utf-8') as file:
        books = json.load(file)

    # Iterate over each book in the JSON file
    for book in books:
        book_id = book['ebook_number']
        if book_id is None:
            continue

        # Index metadata fields (excluding 'words')
        for field, value in book.items():
            if field != 'words':
                value = value.lower()  # Normalize to lowercase
                if value in metadata_index:
                    # Append the book ID if it is not already in the list
                    if book_id not in metadata_index[value]:
                        metadata_index[value].append(book_id)
                else:
                    # Create a new entry in the metadata index
                    metadata_index[value] = [book_id]

    # Write the metadata index to a JSON file
    with open('metadata_index.json', 'w', encoding='utf-8') as file:
        json.dump(metadata_index, file, indent=4)

    return metadata_index
