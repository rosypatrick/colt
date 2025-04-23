import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { LoadingSpinner, ErrorMessage } from './UIComponents';

/**
 * ResultCard component for the Colt Wayfinder application
 * 
 * Displays a product or solution card with details and related items
 */
const ResultCard = ({ item, apiClient }) => {
    const [expanded, setExpanded] = useState(false);
    const [relatedItems, setRelatedItems] = useState([]);
    const [loadingRelated, setLoadingRelated] = useState(false);
    const [error, setError] = useState(null);
    
    const toggleExpand = () => {
        setExpanded(!expanded);
        if (!expanded && !relatedItems.length && !loadingRelated) {
            loadRelatedItems();
        }
    };
    
    const loadRelatedItems = async () => {
        setLoadingRelated(true);
        setError(null);
        try {
            const data = await apiClient.getRelated(item.id);
            setRelatedItems(data.results || []);
        } catch (err) {
            console.error('Error loading related items:', err);
            setError('Failed to load related items');
        } finally {
            setLoadingRelated(false);
        }
    };
    
    // Function to clean text and remove unwanted fragments
    const cleanText = (text) => {
        if (!text) return '';
        
        // List of unwanted text fragments to remove
        const unwantedFragments = [
            "We use cookies on our website colt.info/gb/en.",
            "colt.info/gb/en.",
            ", , . . . and . , . , . , . . Colt was founded by Jack O'Hea in 1931 and has been",
            ", , . . . and. , . , . , . . Colt was founded by Jack O'Hea in 1931 and has been",
            "Colt was founded by Jack O'Hea in 1931 and has been",
            "Jack O'Hea in 1931",
            "pioneering ventilation solutions ever since",
            ", , . . . and . , . , . , . .",
            ", , . . . and. , . , . , . ."
        ];
        
        // Remove each unwanted fragment
        let cleanedText = text;
        unwantedFragments.forEach(fragment => {
            cleanedText = cleanedText.replace(new RegExp(fragment.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '');
        });
        
        // Clean up excessive punctuation and whitespace
        cleanedText = cleanedText.replace(/[,\.]{2,}/g, ''); // Remove repeated commas and periods
        cleanedText = cleanedText.replace(/\s+/g, ' ');      // Replace multiple spaces with a single space
        
        return cleanedText.trim();
    };
    
    // Function to render image if available
    const renderImage = () => {
        if (item.image_urls && item.image_urls.length > 0) {
            return (
                <div className="mb-4">
                    <img 
                        src={item.image_urls[0]} 
                        alt={item.title} 
                        className="w-full h-48 object-cover rounded-t-lg"
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.style.display = 'none';
                        }}
                    />
                </div>
            );
        }
        return null;
    };
    
    // Clean the description text
    const cleanedDescription = cleanText(item.description);
    
    return (
        <div className="solution-card bg-white rounded-lg shadow-lg overflow-hidden mb-6">
            {renderImage()}
            <div className="p-6">
                {item.recommendation_type && (
                    <div className="mb-2">
                        <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                            {item.recommendation_type}
                        </span>
                    </div>
                )}
                <h3 className="text-xl font-bold text-gray-800 mb-2">{item.title}</h3>
                <p className="text-gray-600 mb-4">{cleanedDescription}</p>
                
                {item.type === 'product' && item.categories && (
                    <div className="mb-4">
                        {item.categories.map(cat => (
                            <span key={cat} className="category-pill">
                                {cat}
                            </span>
                        ))}
                    </div>
                )}
                
                <div className="flex justify-between items-center mt-2">
                    <button 
                        className="text-blue-500 hover:text-blue-700 font-medium flex items-center"
                        onClick={toggleExpand}
                    >
                        {expanded ? 'Show Less' : 'Show More'} 
                        <i className={`fas fa-chevron-${expanded ? 'up' : 'down'} ml-1`}></i>
                    </button>
                    {item.url && (
                        <a 
                            href={item.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="colt-btn py-2 px-4 rounded-lg"
                        >
                            View Details
                        </a>
                    )}
                </div>
            </div>
            
            {expanded && (
                <div className="p-6 border-t border-gray-200">
                    {item.type === 'product' && (
                        <>
                            {item.specifications && Object.keys(item.specifications).length > 0 && (
                                <div className="mb-6">
                                    <h4 className="text-lg font-semibold mb-2">Performance Specifications</h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {Object.entries(item.specifications).map(([key, value]) => (
                                            <div key={key} className="border-b border-gray-100 pb-2">
                                                <span className="text-gray-500">{key}:</span> <span className="font-medium">{value}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                            
                            {item.features && item.features.length > 0 && (
                                <div className="mb-6">
                                    <h4 className="text-lg font-semibold mb-2">Features</h4>
                                    <ul className="list-disc pl-5 space-y-1">
                                        {item.features.map((feature, index) => (
                                            <li key={index} className="text-gray-700">{feature}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </>
                    )}
                    
                    <div>
                        <h4 className="text-lg font-semibold mb-2">Related Items</h4>
                        {loadingRelated ? (
                            <LoadingSpinner />
                        ) : error ? (
                            <ErrorMessage message={error} />
                        ) : relatedItems.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {relatedItems.map(related => (
                                    <div key={related.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                                        <h5 className="font-medium mb-2">{related.title}</h5>
                                        <p className="text-sm text-gray-500 mb-2">
                                            {related.type === 'product' ? 'Product' : 
                                             related.type === 'solution' ? 'Solution' : 'Document'}
                                        </p>
                                        {related.url && (
                                            <a 
                                                href={related.url} 
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-500 hover:underline text-sm"
                                            >
                                                View Details
                                            </a>
                                        )}
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-gray-500">No related items found.</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

ResultCard.propTypes = {
    item: PropTypes.object.isRequired,
    apiClient: PropTypes.object.isRequired
};

export default ResultCard;
