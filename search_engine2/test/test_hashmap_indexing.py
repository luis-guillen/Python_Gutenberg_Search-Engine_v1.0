import pytest
from indexer import create_inverted_index

# Path to the processed books JSON file
PROCESSED_JSON_FILE = "../output_books.json"

@pytest.mark.benchmark
def test_hashmap_indexing_performance(benchmark):
    """Benchmark the performance of the Hashmap-based Inverted Index."""
    benchmark.pedantic(create_inverted_index,
                       args=(PROCESSED_JSON_FILE,),
                       rounds=3, warmup_rounds=2, iterations=4)
