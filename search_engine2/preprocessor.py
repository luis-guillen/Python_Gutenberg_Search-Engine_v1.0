import os
import re
import json
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

# Configurations
OUTPUT_PATH = "output_books.json"
STOPWORDS_SET = frozenset(stopwords.words('english'))  # Using frozenset for immutable stopwords


class BookProcessor:
    """Handles the processing of books, including metadata extraction and text cleaning."""

    def __init__(self, file_content):
        self.content = file_content
        self.metadata = self.extract_metadata()

    def extract_metadata(self):
        """Extracts metadata from the book content."""
        return {
            'title': self.find_metadata(r'Title:\s*(.+)'),
            'author': self.find_metadata(r'Author:\s*(.+)'),
            'date': self.extract_year(),
            'language': self.find_metadata(r'Language:\s*(.+)'),
            'credits': self.find_metadata(r'Credits:\s*(.+)'),
            'ebook_number': self.find_metadata(r'eBook (#\d+)', fallback='Unknown')
        }

    def find_metadata(self, pattern, fallback="Unknown"):
        """Helper method to find metadata using regex and fallback value if not found."""
        match = re.search(pattern, self.content)
        return match.group(1).strip() if match else fallback

    def extract_year(self):
        """Extracts the publication year if available in the metadata."""
        date_match = self.find_metadata(r'Release Date:\s*(.+)', fallback=None)
        if date_match:
            year_match = re.search(r'(\d{4})', date_match)
            return year_match.group(1) if year_match else 'Unknown'
        return 'Unknown'

    def clean_content(self):
        """Cleans the main text content by removing stopwords and short words."""
        text_section = self.extract_main_content()
        word_list = self.tokenize_text(text_section)
        return self.filter_words(word_list)

    def extract_main_content(self):
        """Extracts the main content of the book, ignoring headers."""
        start_match = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK', self.content)
        return self.content[start_match.end():] if start_match else self.content

    def tokenize_text(self, text):
        """Tokenizes the text into words."""
        return re.findall(r'\b\w+\b', text.lower())

    def filter_words(self, words):
        """Filters out stopwords and short words."""
        return {word for word in words if word not in STOPWORDS_SET and len(word) > 2}


class BookManager:
    """Manages the reading, processing, and saving of book data."""

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.processed_books = []

    def process_books(self):
        """Processes all book files in the given directory."""
        for book_file in self.list_files():
            file_content = self.read_file(book_file)
            book_data = self.process_single_book(file_content)
            self.processed_books.append(book_data)

    def list_files(self):
        """Lists all valid book files (.txt or .html) in the directory."""
        return [f for f in os.listdir(self.directory_path) if f.endswith(('.txt', '.html'))]

    def read_file(self, filename):
        """Reads the content of a book file."""
        with open(os.path.join(self.directory_path, filename), 'r', encoding='utf-8') as file:
            return file.read()

    def process_single_book(self, content):
        """Processes a single book by extracting metadata and cleaning its text."""
        processor = BookProcessor(content)
        cleaned_words = processor.clean_content()
        return {
            'title': processor.metadata['title'],
            'author': processor.metadata['author'],
            'date': processor.metadata['date'],
            'language': processor.metadata['language'],
            'credits': processor.metadata['credits'],
            'ebook_number': processor.metadata['ebook_number'],
            'words': list(cleaned_words)  # Convert set to list for JSON serialization
        }

    def save_books_to_json(self, output_file):
        """Saves the processed book data to a JSON file."""
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.processed_books, json_file, ensure_ascii=False, indent=4)
        print(f"Saved {len(self.processed_books)} books to {output_file}")


# Runner function
def run_book_processing(book_folder, output_path):
    """Runs the entire book processing pipeline."""
    book_manager = BookManager(book_folder)
    book_manager.process_books()  # Process all books
    book_manager.save_books_to_json(output_path)  # Save the result



