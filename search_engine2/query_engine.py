import json

class QueryEngine:
    """A simple engine for querying an inverted index stored in a JSON file."""

    def __init__(self, index_filepath):
        """Initialize the engine by loading the inverted index from the given JSON file."""
        self.index = self._load_index_from_file(index_filepath)

    def _load_index_from_file(self, filepath):
        """Load the inverted index from a JSON file with error handling."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Index file '{filepath}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in index file '{filepath}'.")
            return {}

    def query(self, search_term):
        """Search for a term in the index and return the associated book IDs."""
        normalized_term = search_term.lower()
        return self.index.get(normalized_term, [])
