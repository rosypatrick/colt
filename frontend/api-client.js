/**
 * Colt Wayfinder API Client
 * 
 * This module provides functions for interacting with the Colt Wayfinder API.
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Search for content based on a text query
 * 
 * @param {string} query - The search query
 * @param {number} limit - Maximum number of results to return
 * @returns {Promise<Object>} Search results
 */
async function search(query, limit = 10) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}&limit=${limit}`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Search failed:', error);
        throw error;
    }
}

/**
 * Perform a guided search based on user inputs
 * 
 * @param {Object} params - The search parameters
 * @param {string} params.industry - Industry filter
 * @param {string} params.problemType - Problem type filter
 * @param {string} params.buildingType - Building type filter
 * @param {number} limit - Maximum number of results to return
 * @returns {Promise<Object>} Search results
 */
async function guidedSearch(params, limit = 10) {
    try {
        const response = await fetch(`${API_BASE_URL}/guided-search?limit=${limit}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Guided search failed:', error);
        throw error;
    }
}

/**
 * Get content related to a specific item
 * 
 * @param {string} itemId - ID of the item to find related content for
 * @param {number} limit - Maximum number of related items to return
 * @returns {Promise<Object>} Related items
 */
async function getRelated(itemId, limit = 5) {
    try {
        const response = await fetch(`${API_BASE_URL}/related/${itemId}?limit=${limit}`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Failed to get related content:', error);
        throw error;
    }
}

/**
 * Get all available categories for filtering
 * 
 * @returns {Promise<Object>} Categories
 */
async function getCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Failed to get categories:', error);
        throw error;
    }
}

// Export the API functions
const API = {
    search,
    guidedSearch,
    getRelated,
    getCategories
};

// For use in non-module environments
if (typeof window !== 'undefined') {
    window.ColtWayfinderAPI = API;
}

// For use with ES modules
export default API;
