"""
Colt Wayfinder Tool - API Backend

This module provides the FastAPI backend for the Colt Wayfinder tool.
"""

from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import logging
import uvicorn
import time
import re

# Import our modules
from search_engine import WayfinderSearchEngine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

# Initialize FastAPI app
app = FastAPI(
    title="Colt Wayfinder API",
    description="API for the Colt Wayfinder tool",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine
search_engine = WayfinderSearchEngine()

# Define API models
class GuidedSearchParams(BaseModel):
    industry: Optional[str] = None
    problemType: Optional[str] = None
    buildingType: Optional[str] = None
    projectSize: Optional[str] = None
    application: Optional[str] = None
    glazing: Optional[str] = None
    useType: Optional[str] = None
    cvValue: Optional[str] = None
    uValue: Optional[str] = None
    acousticsValue: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int

# Middleware for request timing and logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Request to {request.url.path} completed in {process_time:.4f}s")
    return response

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

# API routes
@app.get("/")
async def root():
    return {"message": "Welcome to the Colt Wayfinder API"}

def clean_search_results(results):
    """Clean search results to remove any unwanted text fragments."""
    if not results:
        return results
        
    for result in results:
        if 'description' in result and result['description']:
            # Remove specific problematic text patterns
            unwanted_patterns = [
                r'colt\.info/gb/en\.[^"]*?Jack O\'Hea in 1931[^"]*?',
                r'We use cookies[^"]*?',
                r', , \. \. \. and[^"]*?',
                r'Colt was founded by Jack O\'Hea[^"]*?',
                r'Jack O\'Hea in 1931[^"]*?'
            ]
            
            for pattern in unwanted_patterns:
                result['description'] = re.sub(pattern, '', result['description'])
            
            # Clean up any excessive punctuation or whitespace
            result['description'] = re.sub(r'[,\.]{2,}', '', result['description'])
            result['description'] = re.sub(r'\s+', ' ', result['description'])
            result['description'] = result['description'].strip()
    
    return results

@app.get("/search", response_model=SearchResponse)
async def search(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)):
    """
    Search for content based on a query string.
    
    Args:
        q: The search query
        limit: Maximum number of results to return
    
    Returns:
        Search results matching the query
    """
    try:
        logging.info(f"Search request with query: '{q}', limit: {limit}")
        results = search_engine.search(q, limit=limit)
        
        # Clean results before returning them
        cleaned_results = clean_search_results(results)
        
        return {
            "results": cleaned_results,
            "total": len(cleaned_results)
        }
    except Exception as e:
        logging.error(f"Error during search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Search failed")

@app.post("/guided-search", response_model=SearchResponse)
async def guided_search(params: GuidedSearchParams, limit: int = Query(10, ge=1, le=50)):
    """
    Perform a guided search based on industry, problem type, and building type.
    
    Args:
        params: The guided search parameters
        limit: Maximum number of results to return
    
    Returns:
        Curated search results based on the parameters
    """
    try:
        logging.info(f"Guided search request with params: {params.dict(exclude_none=True)}, limit: {limit}")
        results = search_engine.guided_search(
            industry=params.industry,
            problem_type=params.problemType,
            building_type=params.buildingType,
            project_size=params.projectSize,
            application=params.application,
            glazing=params.glazing,
            use_type=params.useType,
            cv_value=params.cvValue,
            u_value=params.uValue,
            acoustics_value=params.acousticsValue,
            limit=limit
        )
        
        # Clean results before returning them
        cleaned_results = clean_search_results(results)
        
        return {
            "results": cleaned_results,
            "total": len(cleaned_results)
        }
    except Exception as e:
        logging.error(f"Error during guided search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Guided search failed")

@app.get("/related/{item_id}", response_model=SearchResponse)
async def get_related(item_id: str, limit: int = Query(5, ge=1, le=20)):
    """
    Get content related to a specific item.
    
    Args:
        item_id: ID of the item to find related content for
        limit: Maximum number of related items to return
    
    Returns:
        Related items
    """
    try:
        logging.info(f"Related content request for item: '{item_id}', limit: {limit}")
        results = search_engine.get_related_content(item_id, limit=limit)
        
        # Clean results before returning them
        cleaned_results = clean_search_results(results)
        
        return {
            "results": cleaned_results,
            "total": len(cleaned_results)
        }
    except Exception as e:
        logging.error(f"Error getting related content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get related content")

@app.get("/categories")
async def get_categories():
    """Get all available categories for filtering."""
    try:
        # Extract unique categories from the products
        categories = set()
        industries = set()
        problem_types = set()
        building_types = set()
        
        for product in search_engine.products:
            if 'categories' in product:
                for category in product['categories']:
                    categories.add(category)
        
        for solution in search_engine.solutions:
            if 'industries' in solution:
                for industry in solution['industries']:
                    industries.add(industry)
        
        # If we don't have enough data from the scraped content, add some defaults
        if len(categories) < 3:
            categories.update([
                "Smoke Control",
                "Climate Control",
                "Ventilation",
                "Energy Efficiency",
                "Noise Reduction",
                "Louvre"
            ])
        
        if len(industries) < 3:
            industries.update([
                "Commercial Real Estate",
                "Manufacturing",
                "Retail",
                "Logistics",
                "Warehousing",
                "Healthcare"
            ])
        
        # Add default building types
        building_types.update([
            "Office Building",
            "Factory",
            "Warehouse",
            "Shopping Center",
            "Hospital",
            "Data Center"
        ])
        
        # Create the categories response
        # Normalize category names and remove duplicates
        normalized_categories = set()
        for category in categories:
            # Convert to title case for consistency
            normalized = category.title()
            # Handle specific cases
            if normalized == "Smoke-Control":
                normalized = "Smoke Control"
            normalized_categories.add(normalized)
        
        category_response = {
            "industries": sorted(list(industries)),
            "problemTypes": sorted(list(normalized_categories)),
            "buildingTypes": sorted(list(building_types)),
            "projectSizes": [
                "Product dimensions not relevant",
                "Custom dimensions required",
                "Standard dimensions acceptable"
            ],
            "applications": [
                "Roof",
                "Wall",
                "Ceiling",
                "Window/Glazing System",
                "Screens/Partitions"
            ],
            "glazingTypes": [
                "Polycarbonate",
                "Glass",
                "Mixed (Polycarbonate & Glass)",
                "None/Not Applicable"
            ],
            "useTypes": [
                "Interior",
                "Exterior"
            ],
            "cvValues": [
                "Low (< 0.4)",
                "Medium (0.4-0.6)",
                "High (> 0.6)",
                "Not Specified"
            ],
            "uValues": [
                "Excellent (< 0.8 W/m²K)",
                "Good (0.8-1.2 W/m²K)",
                "Standard (1.2-2.0 W/m²K)",
                "Basic (> 2.0 W/m²K)",
                "Not Specified"
            ],
            "acousticsValues": [
                "Low (< 30 dB)",
                "Medium (30-40 dB)",
                "High (> 40 dB)",
                "Not Specified"
            ]
        }
        
        return category_response
    except Exception as e:
        logging.error(f"Error getting categories: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get categories")

# Mount static files for frontend
@app.on_event("startup")
async def startup_event():
    if not os.path.exists("frontend"):
        os.makedirs("frontend", exist_ok=True)
    logging.info("API started successfully")
    logging.info(f"Loaded {len(search_engine.products)} products, {len(search_engine.solutions)} solutions, and {len(search_engine.technical_docs)} technical documents")

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

# Serve index.html for all other routes (SPA support)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if os.path.exists(os.path.join("frontend/dist", full_path)):
        return FileResponse(os.path.join("frontend/dist", full_path))
    return FileResponse("frontend/dist/index.html")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
