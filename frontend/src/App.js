import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Search from './components/Search';
import GuidedSearch from './components/GuidedSearch';
import ResultCard from './components/ResultCard';
import Footer from './components/Footer';
import { LoadingSpinner, ErrorMessage } from './components/UIComponents';
import apiClient from '../api-client';

/**
 * Main App component for the Colt Wayfinder application
 * 
 * Orchestrates the application flow and manages the state
 */
const App = () => {
    const [searchResults, setSearchResults] = useState([]);
    const [searching, setSearching] = useState(false);
    const [searchPerformed, setSearchPerformed] = useState(false);
    const [error, setError] = useState(null);
    
    const handleSearch = async (query) => {
        setSearching(true);
        setSearchPerformed(true);
        setError(null);
        try {
            const data = await apiClient.search(query);
            // Add recommendation_type to each result
            const resultsWithTags = data.results.map((result, index) => ({
                ...result,
                recommendation_type: index === 0 ? 'Recommended' : 'Suggested'
            }));
            setSearchResults(resultsWithTags || []);
        } catch (err) {
            console.error('Search error:', err);
            setError('Failed to perform search. Please try again later.');
            setSearchResults([]);
        } finally {
            setSearching(false);
        }
    };
    
    const handleGuidedSearch = async (params) => {
        setSearching(true);
        setSearchPerformed(true);
        setError(null);
        try {
            const data = await apiClient.guidedSearch(params);
            // Add recommendation_type to each result
            const resultsWithTags = data.results.map((result, index) => ({
                ...result,
                recommendation_type: index === 0 ? 'Recommended' : 'Suggested'
            }));
            setSearchResults(resultsWithTags || []);
        } catch (err) {
            console.error('Guided search error:', err);
            setError('Failed to perform guided search. Please try again later.');
            setSearchResults([]);
        } finally {
            setSearching(false);
        }
    };
    
    return (
        <div className="min-h-screen flex flex-col">
            <Header />
            <Hero />
            
            <main className="container mx-auto px-4 py-8 flex-grow">
                {/* Search and Guided Search Section */}
                <div className="flex flex-col lg:flex-row lg:space-x-8 mb-8">
                    {/* Guided Search - Now on the left and larger */}
                    <div className="lg:w-3/5 order-2 lg:order-1 mt-6 lg:mt-0" id="guided-search">
                        <GuidedSearch 
                            onSearch={handleGuidedSearch} 
                            apiClient={apiClient} 
                        />
                    </div>
                    
                    {/* Search - Now on the right and smaller */}
                    <div className="lg:w-2/5 order-1 lg:order-2">
                        <Search onSearch={handleSearch} />
                        
                        {/* Not Sure Where to Start section - Moved under search bar */}
                        <div className="bg-white rounded-lg shadow-lg p-6 my-6">
                            <h3 className="text-xl font-bold text-gray-800 mb-3">Not Sure Where to Start?</h3>
                            <p className="text-gray-600 mb-4">
                                Talk to our experts for personalized advice on your specific building needs.
                            </p>
                            <a href="#" className="colt-btn py-2 px-4 rounded-lg inline-flex items-center">
                                <i className="fas fa-phone-alt mr-2"></i> Contact Us
                            </a>
                        </div>
                    </div>
                </div>
                
                {/* Search Results Section - Now below both components */}
                {error && <ErrorMessage message={error} />}
                
                {searchPerformed && (
                    <div className="my-6">
                        {searching ? (
                            <LoadingSpinner />
                        ) : (
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                                    Search Results ({searchResults.length})
                                </h2>
                                {searchResults.length > 0 ? (
                                    <div className="space-y-6">
                                        {searchResults.map(item => (
                                            <ResultCard 
                                                key={item.id} 
                                                item={item} 
                                                apiClient={apiClient} 
                                                showRelatedItems={true}
                                            />
                                        ))}
                                    </div>
                                ) : (
                                    <div className="bg-white rounded-lg shadow-lg p-6 text-center">
                                        <i className="fas fa-search text-4xl text-gray-400 mb-4"></i>
                                        <h3 className="text-xl font-bold text-gray-800 mb-2">No results found</h3>
                                        <p className="text-gray-600">
                                            Try adjusting your search terms or use the guided search.
                                        </p>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </main>
            
            <Footer />
        </div>
    );
};

export default App;
