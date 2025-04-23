"""
Colt Wayfinder Search Engine

This module implements the search functionality for the Colt wayfinder tool,
using basic text matching and keyword-based search.
"""

import os
import json
import logging
import re
import glob
from pathlib import Path
import math
from collections import Counter

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
        self.index = {}  # Simple inverted index
        
        # Load data
        self.load_data()
        
        # Create search index
        self.create_index()

    def load_data(self):
        """Load the scraped data from markdown files."""
        try:
            # Check if the data directory exists
            if not os.path.exists(self.data_directory):
                logging.error(f"Data directory {self.data_directory} does not exist")
                self.load_sample_data()
                return
                
            # Find all markdown files in the data directory and its subdirectories
            md_files = glob.glob(os.path.join(self.data_directory, "**/*.md"), recursive=True)
            
            if not md_files:
                logging.warning(f"No markdown files found in {self.data_directory}")
                self.load_sample_data()
                return
                
            logging.info(f"Found {len(md_files)} markdown files")
            
            # Process each markdown file
            for md_file in md_files:
                try:
                    product_data = self.parse_markdown_file(md_file)
                    if product_data:
                        if product_data.get('type') == 'product':
                            self.products.append(product_data)
                        elif product_data.get('type') == 'solution':
                            self.solutions.append(product_data)
                        elif product_data.get('type') == 'technical_document':
                            self.technical_docs.append(product_data)
                        else:
                            # Default to product if not specified
                            product_data['type'] = 'product'
                            self.products.append(product_data)
                except Exception as e:
                    logging.error(f"Error processing file {md_file}: {str(e)}")
            
            logging.info(f"Loaded {len(self.products)} products, {len(self.solutions)} solutions, and {len(self.technical_docs)} technical documents")
            
            # If no data was loaded, use sample data
            if not self.products and not self.solutions and not self.technical_docs:
                logging.warning("No valid data loaded from markdown files, using sample data")
                self.load_sample_data()
        
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            # Fall back to sample data
            self.load_sample_data()
    
    def parse_markdown_file(self, file_path):
        """Parse a markdown file and extract product information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the product name (first heading)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else Path(file_path).stem
            
            # Extract the category
            category_match = re.search(r'\*\*Category:\*\* (.+)', content)
            category = category_match.group(1) if category_match else None
            
            # Extract the description
            description = ""
            desc_section = re.search(r'## Description\s+(.*?)(?=##|\Z)', content, re.DOTALL)
            if desc_section:
                description = desc_section.group(1).strip()
                
                # Filter out unwanted boilerplate text
                unwanted_patterns = [
                    r'We use cookies on our website colt\.info/gb/en\. Some of these cookies are essential.*?ventilation solutions ever since\.',
                    r'Climate Control ExpertsColt pioneered natural ventilation.*?factory solutions to diverse building types\.',
                    r'Louvre ExpertsColt has been manufacturing.*?whilst maintaining rain defence\.',
                    r'Smoke Control System Maintenance ExpertsWith decades of experience.*?compliance, and reliability\.',
                    r'Colt UKExplore our Resources area for downloads.*?to support your projects\.',
                    r'ColtColt was founded by Jack O\'Hea in 1931.*?ventilation solutions ever since\.'
                ]
                
                for pattern in unwanted_patterns:
                    description = re.sub(pattern, '', description, flags=re.DOTALL)
                
                # Remove any remaining cookie fragments
                cookie_fragments = [
                    "We use cookies on our website colt.info/gb/en.",
                    "Some of these cookies are essential while others help us to improve our website",
                    "Please note, that if you do not accept functional and analytical cookies",
                    "For more information about the cookies we use please view our Privacy Policy.",
                    "Colt pioneered natural ventilation in the 1930s",
                    "with over 85 years of climate control experience",
                    "making us the longest-standing company in the field",
                    "We've expanded from factory solutions to diverse building types",
                    "Colt has been manufacturing and installing external solutions",
                    "for almost two decades",
                    "We are experts in screening and ventilation louvre panels",
                    "screening whilst maintaining rain defence",
                    "With decades of experience in smoke control system maintenance",
                    "Colt is a trusted leader in the field",
                    "We've refined our expertise across various building types",
                    "ensuring safety, compliance, and reliability",
                    "Explore our Resources area for downloads",
                    "knowledge articles, case studies, and additional design services",
                    "Access expert insights and tools to support your projects",
                    "Colt was founded by Jack O'Hea in 1931",
                    "has been pioneering ventilation solutions ever since"
                ]
                
                for fragment in cookie_fragments:
                    description = description.replace(fragment, '')
                
                # Clean up excessive whitespace
                description = re.sub(r'\n{3,}', '\n\n', description)
                description = description.strip()
            
            # Extract features
            features = []
            features_section = re.search(r'## Features\s+(.*?)(?=##|\Z)', content, re.DOTALL)
            if features_section:
                features_text = features_section.group(1)
                feature_items = re.findall(r'- (.+)', features_text)
                features = [item.strip() for item in feature_items]
            
            # Extract specifications
            specifications = {}
            specs_section = re.search(r'## Specifications\s+(.*?)(?=##|\Z)', content, re.DOTALL)
            if specs_section:
                specs_text = specs_section.group(1)
                spec_items = re.findall(r'\*\*(.+?):\*\* (.+)', specs_text)
                specifications = {item[0].strip(): item[1].strip() for item in spec_items}
            
            # Extract URL from metadata
            url_match = re.search(r'url: (.+)', content)
            url = url_match.group(1) if url_match else None
            
            # Extract type from metadata
            type_match = re.search(r'type: (.+)', content)
            item_type = type_match.group(1) if type_match else 'product'
            
            # Create a unique ID based on the filename
            item_id = Path(file_path).stem
            
            # Extract image URLs
            image_urls = []
            image_matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
            if image_matches:
                image_urls = image_matches
            
            # Create the product data dictionary
            product_data = {
                'id': item_id,
                'title': title,
                'description': description,
                'type': item_type,
                'url': url,
                'image_urls': image_urls[:3] if image_urls else [],  # Limit to first 3 images
            }
            
            # Add category as a list for consistency with the search function
            if category:
                product_data['categories'] = [category]
            
            # Add features if available
            if features:
                product_data['features'] = features
            
            # Add specifications if available
            if specifications:
                product_data['specifications'] = specifications
            
            return product_data
            
        except Exception as e:
            logging.error(f"Error parsing markdown file {file_path}: {str(e)}")
            return None
    
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
                "description": "Energy-efficient air handling units for commercial buildings. Features heat recovery, variable speed fans, and advanced filtration for optimal indoor air quality.",
                "specifications": {
                    "Airflow": "1,000 - 25,000 m³/h",
                    "Heat Recovery Efficiency": "Up to 85%",
                    "Filtration": "F7/ISO ePM1 60%",
                    "Controls": "Integrated BMS compatibility"
                },
                "categories": ["Climate Control", "Ventilation", "Commercial"]
            },
            {
                "id": "p3",
                "url": "http://colt.info/gb/en/products/smoke-control-ventilation/roof-ventilators",
                "title": "SkyLite Natural Ventilator",
                "description": "Roof-mounted natural ventilators for day-to-day ventilation and smoke control. Aerodynamic design maximizes airflow while preventing rain ingress.",
                "specifications": {
                    "Aerodynamic Free Area": "0.5 - 3.0 m²",
                    "Installation": "Roof-mounted",
                    "Operation": "Pneumatic, electric, or manual",
                    "Certification": "EN 12101-2"
                },
                "categories": ["Smoke Control", "Ventilation", "Natural Ventilation"]
            }
        ]
        
        # Sample solutions
        self.solutions = [
            {
                "id": "s1",
                "url": "http://colt.info/gb/en/solutions/commercial-buildings",
                "title": "Smoke Control for Commercial Buildings",
                "description": "Comprehensive smoke control solutions for office buildings, shopping centers, and public facilities. Our systems ensure safe evacuation routes and assist firefighting operations in case of emergency.",
                "key_benefits": [
                    "Compliant with building regulations",
                    "Integrated with fire alarm systems",
                    "Customizable for different building layouts",
                    "Regular maintenance and testing available"
                ],
                "industries": ["Commercial Real Estate", "Retail", "Office Buildings"],
                "relatedProducts": ["p1", "p3"]
            },
            {
                "id": "s2",
                "url": "http://colt.info/gb/en/solutions/industrial-facilities",
                "title": "Climate Control for Industrial Facilities",
                "description": "Energy-efficient climate control solutions for manufacturing plants, warehouses, and industrial facilities. Our systems maintain optimal working conditions while reducing energy consumption.",
                "key_benefits": [
                    "Reduced energy costs",
                    "Improved worker comfort and productivity",
                    "Customized for specific industrial processes",
                    "Integration with building management systems"
                ],
                "industries": ["Manufacturing", "Logistics", "Warehousing"],
                "relatedProducts": ["p2"]
            }
        ]
        
        # Sample technical documents
        self.technical_docs = [
            {
                "id": "td1",
                "url": "http://colt.info/gb/en/technical/case-studies/manufacturing-climate-control",
                "title": "Case Study: Climate Control in Manufacturing Facility",
                "description": "This case study examines the implementation of Colt's climate control solutions in a large manufacturing facility, resulting in 30% energy savings and improved working conditions.",
                "type": "technical_document",
                "docType": "pdf",
                "relatedProducts": ["p2"],
                "relatedSolutions": ["s2"]
            }
        ]
    
    def create_index(self):
        """Create a simple inverted index for search."""
        try:
            # Combine all data for unified search
            self.combined_data = self.products + self.solutions + self.technical_docs
            
            if not self.combined_data:
                logging.warning("No data available for creating index")
                return
            
            # Create inverted index
            for idx, item in enumerate(self.combined_data):
                # Extract all text content
                text = f"{item['title']} {item['description']}"
                
                # Add categories if available
                if 'categories' in item:
                    text += " " + " ".join(item['categories'])
                
                # Add specifications if available
                if 'specifications' in item:
                    for key, value in item['specifications'].items():
                        text += f" {key} {value}"
                
                # Add features if available
                if 'features' in item:
                    text += " " + " ".join(item['features'])
                
                # Add industries if available
                if 'industries' in item:
                    text += " " + " ".join(item["industries"])
                
                # Tokenize and normalize
                tokens = self._tokenize(text)
                
                # Add to inverted index
                for token in tokens:
                    if token not in self.index:
                        self.index[token] = []
                    if idx not in self.index[token]:
                        self.index[token].append(idx)
            
            logging.info(f"Created search index with {len(self.index)} terms")
            
        except Exception as e:
            logging.error(f"Error creating index: {str(e)}")
    
    def _tokenize(self, text):
        """Tokenize and normalize text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and replace with spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into tokens and remove empty tokens
        tokens = [token for token in text.split() if token]
        
        return tokens
    
    def _clean_result_text(self, text):
        """
        Clean text in search results to remove unwanted fragments.
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return text
            
        # Remove specific problematic fragments
        unwanted_fragments = [
            "We use cookies on our website colt.info/gb/en. , , . . . and . , . , . , . . Colt was founded by Jack O'Hea in 1931 and has been",
            "We use cookies on our website colt.info/gb/en.",
            ", , . . . and. , . , . , . . Colt was founded by Jack O'Hea in 1931 and has been",
            ", , . . . and . , . , . , . . Colt was founded by Jack O'Hea in 1931 and has been",
            "Colt was founded by Jack O'Hea in 1931 and has been",
            "Jack O'Hea in 1931",
            "pioneering ventilation solutions ever since",
            ", , . . . and. , . , . , . .",
            ", , . . . and . , . , . , . .",
            "AboutColt",
            "Climate Control Experts",
            "Louvre Experts",
            "Smoke Control System Maintenance Experts"
        ]
        
        for fragment in unwanted_fragments:
            text = text.replace(fragment, "")
        
        # Use regex to remove cookie notice and related text with any variations
        cookie_patterns = [
            r'We use cookies on our website colt\.info/gb/en\.[^.]*?Jack O\'Hea in 1931[^.]*?',
            r'We use cookies on our website[^.]*?',
            r'Some of these cookies are essential[^.]*?',
            r'Please note, that if you do not accept[^.]*?',
            r'For more information about the cookies[^.]*?',
            r'Colt was founded by Jack O\'Hea[^.]*?',
            r', , \. \. \. and\.? , \. , \. , \. \. '
        ]
        
        for pattern in cookie_patterns:
            text = re.sub(pattern, '', text)
        
        # Clean up excessive punctuation and whitespace
        text = re.sub(r'[,\.]{2,}', '', text)  # Remove repeated commas and periods
        text = re.sub(r'\s+', ' ', text)       # Replace multiple spaces with a single space
        text = text.strip()
        
        return text
    
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
        try:
            if not self.combined_data or not self.index:
                logging.warning("Search engine not properly initialized")
                return []
            
            # Tokenize query
            query_tokens = self._tokenize(query)
            
            if not query_tokens:
                return []
            
            # Find matching documents
            matching_docs = {}
            for token in query_tokens:
                if token in self.index:
                    for doc_idx in self.index[token]:
                        if doc_idx not in matching_docs:
                            matching_docs[doc_idx] = 0
                        matching_docs[doc_idx] += 1
            
            # Calculate relevance scores (simple TF)
            results = []
            for doc_idx, count in matching_docs.items():
                item = self.combined_data[doc_idx]
                
                # Filter by type if specified
                if result_type and item['type'] != result_type:
                    continue
                
                # Add relevance score to the item
                result_item = item.copy()
                result_item['relevance_score'] = count / len(query_tokens)
                
                # Filter out any remaining instances of unwanted text in the description
                if 'description' in result_item and result_item['description']:
                    # Clean the description text
                    result_item['description'] = self._clean_result_text(result_item['description'])
                
                # Also clean the title if needed
                if 'title' in result_item and result_item['title']:
                    result_item['title'] = self._clean_result_text(result_item['title'])
                
                # Skip results with empty descriptions after cleaning
                if 'description' in result_item and not result_item['description'].strip():
                    continue
                
                results.append(result_item)
            
            # Sort by relevance score (descending)
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return results[:limit]
            
        except Exception as e:
            logging.error(f"Error during search: {str(e)}")
            return []
    
    def filter_by_category(self, results, category):
        """Filter results by category."""
        filtered_results = []
        for item in results:
            if 'categories' in item and category in item['categories']:
                filtered_results.append(item)
        return filtered_results
    
    def get_related_content(self, item_id, limit=5):
        """Find content related to a specific item."""
        try:
            # Find the target item
            target_item = None
            for item in self.combined_data:
                if item['id'] == item_id:
                    target_item = item
                    break
            
            if not target_item:
                logging.warning(f"Item with ID {item_id} not found")
                return []
            
            if target_item['type'] == 'product':
                # For a product, find related solutions and other products in the same category
                search_terms = f"{target_item['title']} {target_item['description']}"
                if 'categories' in target_item:
                    search_terms += " " + " ".join(target_item['categories'])
                
                results = self.search(search_terms, limit=limit+1)
                # Remove the original item from results
                results = [r for r in results if r["id"] != item_id]
                return results[:limit]
                
            elif target_item['type'] == 'solution':
                # For a solution, find related products and other solutions
                search_terms = f"{target_item['title']} {target_item['description']}"
                if 'industries' in target_item:
                    search_terms += " " + " ".join(target_item["industries"])
                
                results = self.search(search_terms, limit=limit+1)
                # Remove the original item from results
                results = [r for r in results if r["id"] != item_id]
                return results[:limit]
            
            return []
            
        except Exception as e:
            logging.error(f"Error getting related content: {str(e)}")
            return []
    
    def guided_search(self, industry=None, problem_type=None, building_type=None, project_size=None, application=None, glazing=None, use_type=None, cv_value=None, u_value=None, acoustics_value=None, limit=10):
        """
        Perform guided search based on user inputs about their needs.
        
        Args:
            industry (str, optional): Industry the user is in
            problem_type (str, optional): Type of problem they're trying to solve
            building_type (str, optional): Type of building they're working with
            project_size (str, optional): Size of the project
            application (str, optional): Application area (roof, wall, etc.)
            glazing (str, optional): Type of glazing used
            use_type (str, optional): Interior or exterior use
            cv_value (str, optional): Cv value requirement
            u_value (str, optional): U-value requirement
            acoustics_value (str, optional): Acoustics value requirement
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
        if project_size:
            search_terms.append(project_size)
        if application:
            search_terms.append(application)
        if glazing:
            search_terms.append(glazing)
        if use_type:
            search_terms.append(use_type)
        if cv_value:
            search_terms.append(f"Cv Value {cv_value}")
        if u_value:
            search_terms.append(f"U-Value {u_value}")
        if acoustics_value:
            search_terms.append(f"Acoustics {acoustics_value}")
        
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
