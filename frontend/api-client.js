/**
 * Colt Wayfinder API Client
 * 
 * This module provides a client for interacting with the Colt Wayfinder API.
 */

class WayfinderApiClient {
    constructor(baseUrl = null) {
        // Dynamically determine the API URL based on the environment
        if (!baseUrl) {
            // Check if we're in Codespaces (GitHub's domain)
            const isCodespaces = typeof window !== 'undefined' && 
                window.location.hostname.includes('github.dev');
            
            if (isCodespaces) {
                // In Codespaces, use the same hostname but with port 8000
                const hostname = window.location.hostname;
                // Extract the subdomain part before the first dot
                const subdomainParts = hostname.split('.');
                const portPart = subdomainParts[0];
                
                // Replace the port number in the subdomain (e.g., from -3000 to -8000)
                const backendPortPart = portPart.replace(/-\d+$/, '-8000');
                
                // Reconstruct the hostname with the backend port
                const backendHostname = hostname.replace(portPart, backendPortPart);
                
                this.baseUrl = `https://${backendHostname}`;
                console.log(`Detected Codespaces environment, using API URL: ${this.baseUrl}`);
            } else {
                // Default for local development
                this.baseUrl = 'http://localhost:8000';
                console.log(`Using default API URL: ${this.baseUrl}`);
            }
        } else {
            this.baseUrl = baseUrl;
        }
    }

    /**
     * Search for content based on a query string
     * 
     * @param {string} query - The search query
     * @param {number} limit - Maximum number of results to return
     * @returns {Promise<Object>} Search results
     */
    async search(query, limit = 10) {
        try {
            const response = await fetch(`${this.baseUrl}/search?q=${encodeURIComponent(query)}&limit=${limit}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Search failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Search error:', error);
            throw error;
        }
    }

    /**
     * Perform a guided search based on user parameters
     * 
     * @param {Object} params - The guided search parameters
     * @param {number} limit - Maximum number of results to return
     * @returns {Promise<Object>} Search results
     */
    async guidedSearch(params, limit = 10) {
        try {
            const response = await fetch(`${this.baseUrl}/guided-search?limit=${limit}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(params),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Guided search failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Guided search error:', error);
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
    async getRelated(itemId, limit = 5) {
        try {
            const response = await fetch(`${this.baseUrl}/related/${itemId}?limit=${limit}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to get related content');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Get related error:', error);
            throw error;
        }
    }

    /**
     * Get all available categories for filtering
     * 
     * @returns {Promise<Object>} Categories
     */
    async getCategories() {
        try {
            console.log(`Fetching categories from: ${this.baseUrl}/categories`);
            const response = await fetch(`${this.baseUrl}/categories`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to get categories');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Get categories error:', error);
            throw error;
        }
    }
}

// Create and export a default instance
const apiClient = new WayfinderApiClient();

// Export the API functions
const API = {
    search: apiClient.search.bind(apiClient),
    guidedSearch: apiClient.guidedSearch.bind(apiClient),
    getRelated: apiClient.getRelated.bind(apiClient),
    getCategories: apiClient.getCategories.bind(apiClient)
};

// For use in non-module environments
if (typeof window !== 'undefined') {
    window.ColtWayfinderAPI = API;
}

// For use with ES modules
export default API;
