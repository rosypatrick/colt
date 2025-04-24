/**
 * Colt Wayfinder API Client
 * 
 * This module provides a client for interacting with the Colt Wayfinder API.
 */

class WayfinderApiClient {
    constructor(baseUrl = null) {
        // Dynamically determine the API URL based on the environment
        if (!baseUrl) {
            // Enhanced Codespaces detection - check for various GitHub domains
            const isCodespaces = typeof window !== 'undefined' && 
                (window.location.hostname.includes('github.dev') || 
                 window.location.hostname.includes('github-dev.com') || 
                 window.location.hostname.includes('codespaces') ||
                 window.location.hostname.includes('githubpreview.dev') ||
                 window.location.hostname.includes('app.github.dev'));
            
            console.log(`Hostname detection: ${window.location.hostname}`);
            console.log(`Is Codespaces environment: ${isCodespaces}`);
            
            if (isCodespaces) {
                try {
                    // In Codespaces, each port gets its own subdomain
                    const hostname = window.location.hostname;
                    console.log(`Original hostname: ${hostname}`);
                    
                    // Extract the base part of the hostname (before .app.github.dev or similar)
                    const baseHostnameParts = hostname.split('.');
                    const domainSuffix = baseHostnameParts.slice(1).join('.');
                    
                    // Extract the project name and port from the first part
                    const firstPart = baseHostnameParts[0];
                    console.log(`First part of hostname: ${firstPart}`);
                    
                    // Check if the hostname follows the pattern with port at the end
                    const portMatch = firstPart.match(/-(\d+)$/);
                    if (portMatch) {
                        // Get the project name without the port suffix
                        const projectName = firstPart.substring(0, firstPart.lastIndexOf('-'));
                        console.log(`Project name: ${projectName}`);
                        
                        // Create a new hostname with port 8000
                        const backendHostname = `${projectName}-8000.${domainSuffix}`;
                        console.log(`Constructed backend hostname: ${backendHostname}`);
                        
                        this.baseUrl = `https://${backendHostname}`;
                    } else {
                        // If we can't determine the pattern, try a simple replacement
                        // This is a fallback approach
                        const backendHostname = hostname.replace('-3000', '-8000');
                        console.log(`Fallback backend hostname: ${backendHostname}`);
                        
                        this.baseUrl = `https://${backendHostname}`;
                    }
                    
                    console.log(`Detected Codespaces environment, using API URL: ${this.baseUrl}`);
                    
                    // Verify the backend URL is reachable
                    this.testBackendConnection();
                } catch (error) {
                    console.error('Error configuring Codespaces URL:', error);
                    // Fallback to a default URL
                    this.baseUrl = 'http://localhost:8000';
                    console.log(`Falling back to default API URL: ${this.baseUrl}`);
                }
            } else {
                // Default for local development
                this.baseUrl = 'http://localhost:8000';
                console.log(`Using default API URL: ${this.baseUrl}`);
            }
        } else {
            this.baseUrl = baseUrl;
            console.log(`Using provided API URL: ${this.baseUrl}`);
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

    // Test if the backend connection works
    async testBackendConnection() {
        try {
            console.log(`Testing connection to: ${this.baseUrl}`);
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
            
            const response = await fetch(`${this.baseUrl}/`, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                console.log('Backend connection successful');
            } else {
                console.warn(`Backend connection failed with status: ${response.status}`);
                // Don't change the URL yet, let the actual API calls fail naturally
            }
        } catch (error) {
            console.error('Backend connection test failed:', error);
            // If connection test fails, we could switch to an alternative URL here
            // but for now we'll keep the current URL and let the API calls handle errors
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
