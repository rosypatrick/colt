"""
Script to check search results and identify unwanted text.
"""

from search_engine import WayfinderSearchEngine

def main():
    # Initialize the search engine
    engine = WayfinderSearchEngine()
    
    # Perform a search for "smoke detectors"
    results = engine.search("smoke detectors")
    
    print(f"Found {len(results)} results:")
    
    # Print the first 3 results
    for i, result in enumerate(results[:3]):
        print(f"\nResult {i+1}: {result['title']}")
        print(f"Description: {result['description'][:200]}...")
        
        # Check if the unwanted text is in the description
        unwanted_text = "We use cookies on our website colt.info/gb/en."
        if unwanted_text in result['description']:
            print(f"FOUND UNWANTED TEXT in result {i+1}")
            
            # Find the position of the unwanted text
            pos = result['description'].find(unwanted_text)
            print(f"Position: {pos}")
            
            # Print the context around the unwanted text
            start = max(0, pos - 20)
            end = min(len(result['description']), pos + len(unwanted_text) + 20)
            print(f"Context: ...{result['description'][start:end]}...")

if __name__ == "__main__":
    main()
