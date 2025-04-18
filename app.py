"""
Colt Wayfinder Tool - API Backend

This module provides the FastAPI backend for the Colt Wayfinder tool.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import logging
import uvicorn

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

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int

# API routes
@app.get("/")
async def root():
    return {"message": "Welcome to the Colt Wayfinder API"}

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
        results = search_engine.search(q, limit=limit)
        return {
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logging.error(f"Error during search: {str(e)}")
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
        results = search_engine.guided_search(
            industry=params.industry,
            problem_type=params.problemType,
            building_type=params.buildingType,
            limit=limit
        )
        return {
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logging.error(f"Error during guided search: {str(e)}")
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
        results = search_engine.get_related_content(item_id, limit=limit)
        return {
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logging.error(f"Error getting related content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get related content")

@app.get("/categories")
async def get_categories():
    """Get all available categories for filtering."""
    try:
        # This would normally come from a database
        categories = {
            "industries": [
                "Commercial Real Estate",
                "Manufacturing",
                "Retail",
                "Logistics",
                "Warehousing",
                "Healthcare"
            ],
            "problemTypes": [
                "Smoke Control",
                "Climate Control",
                "Ventilation",
                "Energy Efficiency",
                "Noise Reduction"
            ],
            "buildingTypes": [
                "Office Building",
                "Factory",
                "Warehouse",
                "Shopping Center",
                "Hospital",
                "Data Center"
            ]
        }
        return categories
    except Exception as e:
        logging.error(f"Error getting categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get categories")

# Mount static files for frontend
@app.on_event("startup")
async def startup_event():
    if not os.path.exists("frontend"):
        os.makedirs("frontend", exist_ok=True)
    logging.info("API started successfully")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Serve index.html for all other routes (SPA support)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if os.path.exists(os.path.join("frontend", full_path)):
        return FileResponse(os.path.join("frontend", full_path))
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
