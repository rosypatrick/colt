"""
Colt Wayfinder Search Engine

This module implements the search functionality for the Colt wayfinder tool,
using vector embeddings for semantic search capabilities.
"""

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("search_engine.log"),
        logging.StreamHandler()
    ]
)

class WayfinderSearchEngine:
    def __init__(self, data_directory="scraped_data"):
        self.data_directory = data_directory
        self.products = []
        self.solutions = []
        self.technical_docs = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.product_vectors = None
        self.solution_vectors = None
        self.combined_data = []
        self.combined_vectors = None
        self.combined_vectorizer = None
        
        # Load data
        self.load_data()
        
        # Create vector embeddings
        self.create_embeddings()

    def load_data(self):
        """Load the scraped data from JSON files."""
        try:
            # Load products
            product_path = os.path.join(self.data_directory, "products.json")
            if os.path.exists(product_path):
                with open(product_path, "r", encoding="utf-8") as f:
                    self.products = json.load(f)
                logging.info(f"Loaded {len(self.products)} products")
            
            # Load solutions
            solution_path = os.path.join(self.data_directory, "solutions.json")
            if os.path.exists(solution_path):
                with open(solution_path, "r", encoding="utf-8") as f:
                    self.solutions = json.load(f)
                logging.info(f"Loaded {len(self.solutions)} solutions")
            
            # Load technical docs
            docs_path = os.path.join(self.data_directory, "technical_docs.json")
            if os.path.exists(docs_path):
                with open(docs_path, "r", encoding="utf-8") as f:
                    self.technical_docs = json.load(f)
                logging.info(f"Loaded {len(self.technical_docs)} technical documents")
            
            # If no data files exist, use sample data for demo purposes
            if not self.products and not self.solutions and not self.technical_docs:
                self.load_sample_data()
        
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            # Fall back to sample data
            self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample data for demonstration purposes."""
        logging.info("Loading sample data for demonstration")
        
        # Sample products
        self.products = [
            {
                "id": "p1",
                "url": "http://colt.info/gb/en/products/smoke-control-ventilation/exhaust-fans",
                "title": "Industrial Exhaust Fan Series 500",
                "description": "Heavy-duty exhaust fans designed for smoke extraction in industrial environments. These fans are certified for operation at 400°C for 2 hours, making them ideal for emergency smoke extraction in factories, warehouses, and large commercial spaces.",
                "specifications": {
                    "Temperature Rating": "400°C for 2 hours",
                    "Airflow": "Up to 45,000 m³/h",
                    "Pressure": "Up to 1500 Pa",
                    "Power": "5.5 - 45 kW"
                },
                "categories": ["Smoke Control", "Ventilation", "Industrial"]
            },
            {
                "id": "p2",
                "url": "http://colt.info/gb/en/products/climate-control/air-handling-units",
                "title": "EcoVent Air Handling Unit",
                "description": "Energy-efficient air handling units for commercial buildings. The EcoVent series features heat recovery systems, variable speed fans, and advanced filtration to provide optimal indoor air quality while minimizing energy consumption.",
                "specifications": {
                    "Airflow": "1,000 - 25,000 m³/h",
                    "Heat Recovery Efficiency": "Up to 85%",
                    "Filtration": "ISO ePM1 55% (F7)",
                    "Controls": "Integrated BMS compatibility"
                },
                "categories": ["Climate Control", "Energy Efficiency", "Commercial"]
            },
            {
                "id": "p3",
                "url": "http://colt.info/gb/en/products/smoke-control-ventilation/natural-ventilators",
                "title": "SkyLite Natural Ventilator",
                "description": "Roof-mounted natural ventilators for day-to-day ventilation and smoke control. The SkyLite series uses aerodynamic principles to enhance natural airflow, providing efficient ventilation without energy consumption during normal operation, while ensuring reliable smoke extraction during emergencies.",
                "specifications": {
                    "Aerodynamic Free Area": "1.0 - 6.0 m²",
                    "Installation": "Roof-mounted",
                    "Operation": "Pneumatic, electric or mechanical",
                    "Testing": "EN 12101-2 certified"
                },
                "categories": ["Smoke Control", "Natural Ventilation", "Sustainable"]
            }
        ]
        
        # Sample solutions
        self.solutions = [
            {
                "id": "s1",
                "url": "http://colt.info/gb/en/solutions/commercial-buildings",
                "title": "Smoke Control for Commercial Buildings",
                "description": "Comprehensive smoke control solutions for office buildings, shopping centers, and multi-purpose commercial spaces. Our integrated approach combines mechanical and natural ventilation systems to create safe evacuation routes and enable firefighting operations during emergencies.",
                "industries": ["Commercial Real Estate", "Retail", "Office Buildings"],
                "related_products": ["p1", "p3"]
            },
            {
                "id": "s2",
                "url": "http://colt.info/gb/en/solutions/industrial-facilities",
                "title": "Climate Control for Industrial Facilities",
                "description": "Energy-efficient climate control solutions for manufacturing plants, warehouses, and industrial facilities. Our systems manage temperature, humidity, and air quality to optimize working conditions, protect inventory, and reduce energy costs.",
                "industries": ["Manufacturing", "Logistics", "Warehousing"],
                "related_products": ["p1", "p2"]
            }
        ]
        
        # Sample technical documents
        self.technical_docs = [
            {
                "id": "d1",
                "url": "http://colt.info/gb/en/technical/whitepapers/smoke-control-regulations",
                "title": "Guide to Smoke Control Regulations in Commercial Buildings",
                "type": "pdf",
                "related_products": ["p1", "p3"],
                "related_solutions": ["s1"]
            },
            {
                "id": "d2",
                "url": "http://colt.info/gb/en/technical/case-studies/manufacturing-climate-control",
                "title": "Case Study: Energy Optimization in Manufacturing Facilities",
                "type": "pdf",
                "related_products": ["p2"],
                "related_solutions": ["s2"]
            }
        ]
        
        logging.info(f"Loaded {len(self.products)} sample products, {len(self.solutions)} sample solutions, and {len(self.technical_docs)} sample technical documents")

    def create_embeddings(self):
        """Create vector embeddings for all content using TF-IDF."""
        try:
            # Create product text corpus
            product_texts = []
            for product in self.products:
                text = f"{product['title']} {product['description']}"
                if 'specifications' in product:
                    for key, value in product['specifications'].items():
                        text += f" {key} {value}"
                if 'categories' in product:
                    text += " " + " ".join(product['categories'])
                product_texts.append(text)
            
            # Create solution text corpus
            solution_texts = []
            for solution in self.solutions:
                text = f"{solution['title']} {solution['description']}"
                if 'industries' in solution:
                    text += " " + " ".join(solution['industries'])
                solution_texts.append(text)
            
            # Create combined corpus for unified search
            self.combined_data = []
            combined_texts = []
            
            # Add products to combined data
            for i, product in enumerate(self.products):
                self.combined_data.append({
                    "id": product.get("id", f"product_{i}"),
                    "type": "product",
                    "title": product["title"],
                    "description": product["description"],
                    "url": product["url"],
                    "categories": product.get("categories", [])
                })
                combined_texts.append(product_texts[i])
            
            # Add solutions to combined data
            for i, solution in enumerate(self.solutions):
                self.combined_data.append({
                    "id": solution.get("id", f"solution_{i}"),
                    "type": "solution",
                    "title": solution["title"],
                    "description": solution["description"],
                    "url": solution["url"],
                    "industries": solution.get("industries", [])
                })
                combined_texts.append(solution_texts[i])
            
            # Add technical docs to combined data
            for i, doc in enumerate(self.technical_docs):
                doc_text = f"{doc['title']}"
                self.combined_data.append({
                    "id": doc.get("id", f"doc_{i}"),
                    "type": "technical_document",
                    "title": doc["title"],
                    "url": doc["url"],
                    "doc_type": doc.get("type", "")
                })
                combined_texts.append(doc_text)
            
            # Create vector embeddings
            if product_texts:
                self.product_vectors = self.vectorizer.fit_transform(product_texts)
                logging.info(f"Created embeddings for {len(product_texts)} products")
            
            # Create new vectorizer for solutions to avoid contamination
            if solution_texts:
                solution_vectorizer = TfidfVectorizer(stop_words='english')
                self.solution_vectors = solution_vectorizer.fit_transform(solution_texts)
                logging.info(f"Created embeddings for {len(solution_texts)} solutions")
            
            # Create combined vectorizer for unified search
            if combined_texts:
                combined_vectorizer = TfidfVectorizer(stop_words='english')
                self.combined_vectors = combined_vectorizer.fit_transform(combined_texts)
                self.combined_vectorizer = combined_vectorizer
                logging.info(f"Created embeddings for {len(combined_texts)} combined items")
            
        except Exception as e:
            logging.error(f"Error creating embeddings: {str(e)}")
    
    def search(self, query, result_type=None, limit=10):
        """
        Search for content based on the query.
        
        Args:
            query (str): The search query
            result_type (str, optional): Filter by type ('product', 'solution', 'technical_document')
            limit (int, optional): Maximum number of results to return
            
        Returns:
            list: Matching results with relevance scores
        """
        if not self.combined_vectors or not self.combined_vectorizer:
            logging.error("Search index not built. Cannot perform search.")
            return []
        
        try:
            # Transform the query to the same vector space
            query_vector = self.combined_vectorizer.transform([query])
            
            # Calculate similarity scores
            similarity_scores = cosine_similarity(query_vector, self.combined_vectors).flatten()
            
            # Get top results with their scores
            results = []
            for i, score in enumerate(similarity_scores):
                if result_type and self.combined_data[i]["type"] != result_type:
                    continue
                
                result = self.combined_data[i].copy()
                result["relevance_score"] = float(score)
                results.append(result)
            
            # Sort by relevance score (descending) and limit results
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logging.error(f"Error during search: {str(e)}")
            return []
    
    def filter_by_category(self, results, category):
        """Filter results by category."""
        filtered = []
        for result in results:
            if result["type"] == "product" and "categories" in result and category in result["categories"]:
                filtered.append(result)
            elif result["type"] == "solution" and "industries" in result and category in result["industries"]:
                filtered.append(result)
        return filtered
    
    def get_related_content(self, item_id, limit=5):
        """Find content related to a specific item."""
        # This is a placeholder for a more sophisticated recommendation engine
        if not self.combined_data:
            return []
        
        # Find the target item
        target_item = None
        for item in self.combined_data:
            if item.get("id") == item_id:
                target_item = item
                break
        
        if not target_item:
            return []
        
        # Find related items based on text similarity
        if target_item["type"] == "product":
            # For a product, find related solutions and other products
            search_terms = f"{target_item['title']} {target_item['description']}"
            if "categories" in target_item:
                search_terms += " " + " ".join(target_item["categories"])
            
            results = self.search(search_terms, limit=limit+1)
            # Remove the original item from results
            results = [r for r in results if r["id"] != item_id]
            return results[:limit]
            
        elif target_item["type"] == "solution":
            # For a solution, find related products and other solutions
            search_terms = f"{target_item['title']} {target_item['description']}"
            if "industries" in target_item:
                search_terms += " " + " ".join(target_item["industries"])
            
            results = self.search(search_terms, limit=limit+1)
            # Remove the original item from results
            results = [r for r in results if r["id"] != item_id]
            return results[:limit]
        
        return []
    
    def guided_search(self, industry=None, problem_type=None, building_type=None, limit=10):
        """
        Perform guided search based on user inputs about their needs.
        
        Args:
            industry (str, optional): Industry the user is in
            problem_type (str, optional): Type of problem they're trying to solve
            building_type (str, optional): Type of building they're working with
            limit (int, optional): Maximum number of results to return
            
        Returns:
            list: Curated results for the user's needs
        """
        search_terms = []
        if industry:
            search_terms.append(industry)
        if problem_type:
            search_terms.append(problem_type)
        if building_type:
            search_terms.append(building_type)
        
        if not search_terms:
            return []
        
        query = " ".join(search_terms)
        results = self.search(query, limit=limit)
        
        # Add a recommendation type to each result for the frontend to use
        for result in results:
            if result["type"] == "solution":
                result["recommendation_type"] = "Recommended Solution"
            elif result["type"] == "product":
                result["recommendation_type"] = "Suggested Product"
            elif result["type"] == "technical_document":
                result["recommendation_type"] = "Helpful Resource"
        
        return results

# Example usage
if __name__ == "__main__":
    search_engine = WayfinderSearchEngine()
    
    # Perform a search
    results = search_engine.search("smoke control commercial building")
    print(f"Found {len(results)} results:")
    for result in results:
        print(f"- {result['title']} ({result['type']}) - Score: {result['relevance_score']:.2f}")
    
    # Try guided search
    guided_results = search_engine.guided_search(
        industry="Commercial Real Estate",
        problem_type="Smoke Control",
        building_type="Office Building"
    )
    print(f"\nGuided search found {len(guided_results)} results:")
    for result in guided_results:
        print(f"- {result['title']} ({result['recommendation_type']})")
