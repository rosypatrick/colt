import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Search component for the Colt Wayfinder application
 * 
 * Provides a search box for users to search for products and solutions
 */
const Search = ({ onSearch }) => {
    const [query, setQuery] = useState('');
    
    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };
    
    return (
        <div className="search-box bg-white rounded-lg shadow-md p-4 mb-6">
            <form onSubmit={handleSubmit} className="flex">
                <input
                    type="text"
                    placeholder="Search for products, solutions, or documentation..."
                    className="flex-grow px-4 py-2 rounded-l-lg border-2 border-gray-300 focus:outline-none focus:border-blue-500"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button 
                    type="submit" 
                    className="colt-btn px-6 py-2 rounded-r-lg"
                >
                    <i className="fas fa-search mr-2"></i> Search
                </button>
            </form>
        </div>
    );
};

Search.propTypes = {
    onSearch: PropTypes.func.isRequired
};

export default Search;
