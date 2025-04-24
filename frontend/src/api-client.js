/**
 * API client for the Colt Wayfinder application
 * 
 * Handles all communication with the backend API
 */

// Dynamically determine the API base URL based on the environment
const getApiBaseUrl = () => {
    // Check if we're running in GitHub Codespaces
    const isCodespaces = window.location.hostname.includes('.github.dev') || 
                          window.location.hostname.includes('.preview.app.github.dev');
    
    if (isCodespaces) {
        // In Codespaces, we need to modify the URL to point to the backend port
        // Convert frontend URL like https://user-codespace-name-3000.preview.app.github.dev/
        // to backend URL like https://user-codespace-name-8000.preview.app.github.dev/
        const currentUrl = window.location.origin;
        // Replace the port number in the URL (e.g., -3000 to -8000)
        const backendUrl = currentUrl.replace(/-3000\./g, '-8000.');
        return `${backendUrl}`;
    }
    
    // For local development, use the relative path which will be handled by the webpack proxy
    return '/api';
};

const API_BASE_URL = getApiBaseUrl();

/**
 * Handles API errors and provides consistent error messages
 * @param {Response} response - The fetch response object
 * @returns {Promise} - Resolves with the response data or rejects with an error
 */
const handleResponse = async (response) => {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `Error: ${response.status} ${response.statusText}`;
        throw new Error(errorMessage);
    }
    return response.json();
};

/**
 * API client object with methods for each API endpoint
 */
const apiClient = {
    /**
     * Perform a keyword search
     * @param {string} query - Search query
     * @param {number} limit - Maximum number of results to return
     * @returns {Promise<Object>} - Search results
     */
    search: async (query, limit = 10) => {
        if (typeof query === 'object') {
            // Handle object query (from guided search)
            return apiClient.guidedSearch(query, limit);
        }
        
        const url = `${API_BASE_URL}/search?q=${encodeURIComponent(query)}&limit=${limit}`;
        const response = await fetch(url);
        return handleResponse(response);
    },
    
    /**
     * Perform a guided search based on user-selected parameters
     * @param {Object} params - Guided search parameters
     * @param {number} limit - Maximum number of results to return
     * @returns {Promise<Object>} - Search results
     */
    guidedSearch: async (params, limit = 10) => {
        const queryParams = new URLSearchParams();
        
        // Map frontend parameter names to backend parameter names
        const paramMapping = {
            industry: 'industry',
            problemType: 'problem_type',
            buildingType: 'building_type',
            projectSize: 'project_size',
            application: 'application',
            glazing: 'glazing_type',
            useType: 'use_type',
            cvValue: 'cv_value',
            uValue: 'u_value',
            acousticsValue: 'acoustics_value'
        };
        
        // Add parameters to query string
        Object.entries(params).forEach(([key, value]) => {
            if (value && paramMapping[key]) {
                queryParams.append(paramMapping[key], value);
            }
        });
        
        // Add limit parameter
        queryParams.append('limit', limit);
        
        const url = `${API_BASE_URL}/guided-search?${queryParams.toString()}`;
        const response = await fetch(url);
        return handleResponse(response);
    },
    
    /**
     * Get related content for a specific item
     * @param {string} itemId - ID of the item to get related content for
     * @param {number} limit - Maximum number of related items to return
     * @returns {Promise<Object>} - Related items
     */
    getRelated: async (itemId, limit = 5) => {
        const url = `${API_BASE_URL}/related/${encodeURIComponent(itemId)}?limit=${limit}`;
        const response = await fetch(url);
        return handleResponse(response);
    },
    
    /**
     * Get categories and other metadata for guided search
     * @returns {Promise<Object>} - Categories and metadata
     */
    getCategories: async () => {
        const url = `${API_BASE_URL}/categories`;
        const response = await fetch(url);
        return handleResponse(response);
    }
};

export default apiClient;
