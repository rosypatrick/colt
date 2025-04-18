"""
Colt Wayfinder Search Engine (Simplified Version)

A simplified version of the search engine that doesn't require scikit-learn.
"""

import json
import os
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
        self.combined_data = []
        
        # Load data
        self.load_data()

    def load_data(self):
        """Load the scraped data from JSON files or use sample data."""
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
            
            # Create combined data
            self.combined_data = []
            
            # Add products to combined data
            for i, product in enumerate(self.products):
                self.combined_data.append({
                    "id": product.get("id", f"product_{i}"),
                    "type": "product",
                    "title": product["title"],
                    "description": product["description"],
                    "url": product.get("url", ""),
                    "categories": product.get("categories", []),
                    "specifications": product.get("specifications", {})
                })
            
            # Add solutions to combined data
            for i, solution in enumerate(self.solutions):
                self.combined_data.append({
                    "id": solution.get("id", f"solution_{i}"),
                    "type": "solution",
                    "title": solution["title"],
                    "description": solution["description"],
                    "url": solution.get("url", ""),
                    "industries": solution.get("industries", []),
                    "relatedProducts": solution.get("relatedProducts", [])
                })
            
            # Add technical docs to combined data
            for i, doc in enumerate(self.technical_docs):
                self.combined_data.append({
                    "id": doc.get("id", f"doc_{i}"),
                    "type": "technical_document",
                    "title": doc["title"],
                    "description": doc.get("description", ""),
                    "url": doc.get("url", ""),
                    "docType": doc.get("type", ""),
                    "relatedProducts": doc.get("relatedProducts", []),
                    "relatedSolutions": doc.get("relatedSolutions", [])
                })
            
            logging.info(f"Prepared {len(self.combined_data)} total items for search")
        
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
                "relatedProducts": ["p1", "p3"]
            },
            {
                "id": "s2",
                "url": "http://colt.info/gb/en/solutions/industrial-facilities",
                "title": "Climate Control for Industrial Facilities",
                "description": "Energy-efficient climate control solutions for manufacturing plants, warehouses, and industrial facilities. Our systems manage temperature, humidity, and air quality to optimize working conditions, protect inventory, and reduce energy costs.",
                "industries": ["Manufacturing", "Logistics", "Warehousing"],
                "relatedProducts": ["p1", "p2"]
            }
        ]
        
        # Sample technical documents
        self.technical_docs = [
            {
                "id": "d1",
                "url": "http://colt.info/gb/en/technical/whitepapers/smoke-control-regulations",
                "title": "Guide to Smoke Control Regulations in Commercial Buildings",
                "description": "Comprehensive guide to regulatory requirements for smoke control systems in commercial buildings across different regions.",
                "type": "pdf",
                "relatedProducts": ["p1", "p3"],
                "relatedSolutions": ["s1"]
            },
            {
                "id": "d2",
                "url": "http://colt.info/gb/en/technical/case-studies/manufacturing-climate-control",
                "title": "Case Study: Energy Optimization in Manufacturing Facilities",
                "description": "Learn how a major manufacturing facility reduced energy consumption by 35% using Colt climate control solutions.",
                "type": "pdf",
                "relatedProducts": ["p2"],
                "relatedSolutions": ["s2"]
            }
        ]
        
        logging.info(f"Loaded {len(self.products)} sample products, {len(self.solutions)} sample solutions, and {len(self.technical_docs)} sample technical documents")
    
    def search(self, query, result_type=None, limit=10):
        """
        Simple search implementation using keyword matching.
        
        Args:
            query (str): The search query
            result_type (str, optional): Filter by type ('product', 'solution', 'technical_document')
            limit (int, optional): Maximum number of results to return
            
        Returns:
            list: Matching results with relevance scores
        """
        try:
            query = query.lower()
            results = []
            
            for item in self.combined_data:
                # Skip if filtering by type and this item doesn't match
                if result_type and item["type"] != result_type:
                    continue
                
                score = 0
                
                # Check title for match (highest weight)
                if query in item["title"].lower():
                    score += 3
                
                # Check description for match
                if "description" in item and query in item["description"].lower():
                    score += 2
                
                # Check categories/industries for match
                if "categories" in item:
                    for category in item["categories"]:
                        if query in category.lower():
                            score += 1
                
                if "industries" in item:
                    for industry in item["industries"]:
                        if query in industry.lower():
                            score += 1
                
                if score > 0:
                    result = item.copy()
                    result["relevance_score"] = score
                    results.append(result)
            
            # Sort by relevance score (descending)
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
        try:
            # Find the target item
            target_item = None
            for item in self.combined_data:
                if item.get("id") == item_id:
                    target_item = item
                    break
            
            if not target_item:
                return []
            
            # Find related items
            related_items = []
            
            # If it's a product, find related solutions and technical docs
            if target_item["type"] == "product":
                # Find solutions that reference this product
                for item in self.combined_data:
                    if item["type"] == "solution" and "relatedProducts" in item and item_id in item["relatedProducts"]:
                        related_items.append(item)
                    
                    if item["type"] == "technical_document" and "relatedProducts" in item and item_id in item["relatedProducts"]:
                        related_items.append(item)
                
                # Find products in the same category
                if "categories" in target_item:
                    for item in self.combined_data:
                        if item["type"] == "product" and item["id"] != item_id and "categories" in item:
                            for category in target_item["categories"]:
                                if category in item["categories"]:
                                    related_items.append(item)
                                    break
            
            # If it's a solution, find related products and technical docs
            elif target_item["type"] == "solution":
                # Find related products
                if "relatedProducts" in target_item:
                    for item in self.combined_data:
                        if item["type"] == "product" and item["id"] in target_item["relatedProducts"]:
                            related_items.append(item)
                
                # Find technical docs related to this solution
                for item in self.combined_data:
                    if item["type"] == "technical_document" and "relatedSolutions" in item and target_item["id"] in item["relatedSolutions"]:
                        related_items.append(item)
            
            # Remove duplicates and limit results
            unique_ids = set()
            unique_items = []
            
            for item in related_items:
                if item["id"] not in unique_ids:
                    unique_ids.add(item["id"])
                    unique_items.append(item)
            
            return unique_items[:limit]
            
        except Exception as e:
            logging.error(f"Error getting related content: {str(e)}")
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
        try:
            results = []
            
            # First, find solutions for the specified industry
            if industry:
                for item in self.combined_data:
                    if item["type"] == "solution" and "industries" in item:
                        for ind in item["industries"]:
                            if industry.lower() in ind.lower():
                                item_copy = item.copy()
                                item_copy["relevance_score"] = 5
                                item_copy["recommendation_type"] = "Recommended Solution"
                                results.append(item_copy)
                                break
            
            # Next, find products for the specified problem type
            if problem_type:
                for item in self.combined_data:
                    if item["type"] == "product" and "categories" in item:
                        for category in item["categories"]:
                            if problem_type.lower() in category.lower():
                                item_copy = item.copy()
                                item_copy["relevance_score"] = 4
                                item_copy["recommendation_type"] = "Suggested Product"
                                results.append(item_copy)
                                break
            
            # Adjust scores based on building type if specified
            if building_type and results:
                for result in results:
                    if "description" in result and building_type.lower() in result["description"].lower():
                        result["relevance_score"] += 2
            
            # Add technical documents if we have solutions or products
            if results:
                product_ids = [r["id"] for r in results if r["type"] == "product"]
                solution_ids = [r["id"] for r in results if r["type"] == "solution"]
                
                for item in self.combined_data:
                    if item["type"] == "technical_document":
                        related_to_result = False
                        
                        if "relatedProducts" in item:
                            for pid in item["relatedProducts"]:
                                if pid in product_ids:
                                    related_to_result = True
                                    break
                        
                        if not related_to_result and "relatedSolutions" in item:
                            for sid in item["relatedSolutions"]:
                                if sid in solution_ids:
                                    related_to_result = True
                                    break
                        
                        if related_to_result:
                            item_copy = item.copy()
                            item_copy["relevance_score"] = 3
                            item_copy["recommendation_type"] = "Helpful Resource"
                            results.append(item_copy)
            
            # Sort by relevance score (descending)
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            # Remove duplicates
            unique_results = []
            unique_ids = set()
            
            for item in results:
                if item["id"] not in unique_ids:
                    unique_ids.add(item["id"])
                    unique_results.append(item)
            
            return unique_results[:limit]
            
        except Exception as e:
            logging.error(f"Error during guided search: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    search_engine = WayfinderSearchEngine()
    
    # Perform a search
    results = search_engine.search("smoke control commercial building")
    print(f"Found {len(results)} results:")
    for result in results:
        print(f"- {result['title']} ({result['type']}) - Score: {result['relevance_score']}")
