// Colt Wayfinder - Frontend Application

// Import the API client
const { API } = require('./api-client.js');

// Loading and Error components
const LoadingSpinner = () => {
    return (
        <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
    );
};

const ErrorMessage = ({ message }) => {
    return (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative my-4" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{message}</span>
        </div>
    );
};

// React Components
const Header = () => {
    return (
        <header className="colt-gradient text-white shadow-lg">
            <div className="container mx-auto px-4 py-4">
                <div className="flex flex-col md:flex-row justify-between items-center">
                    <div className="flex items-center mb-4 md:mb-0">
                        <h1 className="text-2xl font-bold">Colt Wayfinder</h1>
                    </div>
                    <nav>
                        <ul className="flex space-x-6">
                            <li><a href="#" className="hover:text-gray-300 transition">Products</a></li>
                            <li><a href="#" className="hover:text-gray-300 transition">Solutions</a></li>
                            <li><a href="#" className="hover:text-gray-300 transition">Resources</a></li>
                            <li><a href="#" className="hover:text-gray-300 transition">Contact</a></li>
                        </ul>
                    </nav>
                </div>
            </div>
        </header>
    );
};

// Search Component
const Search = ({ onSearch }) => {
    const [query, setQuery] = React.useState('');
    
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

// Guided Search Component
const GuidedSearch = ({ onSearch }) => {
    const [step, setStep] = React.useState(1);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);
    const [categories, setCategories] = React.useState(null);
    const [params, setParams] = React.useState({
        industry: '',
        problemType: '',
        buildingType: '',
        projectSize: '',
        application: '',
        glazing: '',
        useType: '',
        cvValue: '',
        uValue: '',
        acousticsValue: ''
    });
    
    // Fetch categories on component mount
    React.useEffect(() => {
        const fetchCategories = async () => {
            try {
                setLoading(true);
                setError(null);
                const data = await API.getCategories();
                setCategories(data);
            } catch (err) {
                setError('Failed to load categories. Please try again later.');
                console.error('Error fetching categories:', err);
            } finally {
                setLoading(false);
            }
        };
        
        fetchCategories();
    }, []);
    
    const handleNextStep = () => {
        setStep(prevStep => prevStep + 1);
    };
    
    const handlePrevStep = () => {
        setStep(prevStep => prevStep - 1);
    };
    
    const handleSearch = () => {
        // Filter out empty parameters
        const filteredParams = Object.fromEntries(
            Object.entries(params).filter(([_, value]) => value !== '')
        );
        
        onSearch(filteredParams);
    };
    
    if (loading) {
        return <LoadingSpinner />;
    }
    
    if (error) {
        return <ErrorMessage message={error} />;
    }
    
    if (!categories) {
        return null;
    }
    
    return (
        <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Find Your Perfect Solution</h2>
            <p className="text-gray-600 mb-6">
                Answer a few questions to help us recommend the best products and solutions for your needs.
            </p>
            
            {step === 1 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">What industry are you in?</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                        {categories.industries.map(industry => (
                            <button
                                key={industry}
                                className={`p-3 rounded-lg border-2 text-left ${
                                    params.industry === industry 
                                        ? 'border-blue-500 bg-blue-50' 
                                        : 'border-gray-300 hover:border-blue-300'
                                }`}
                                onClick={() => setParams({...params, industry})}
                            >
                                {industry}
                            </button>
                        ))}
                    </div>
                    <div className="flex justify-end mt-4">
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleNextStep}
                            disabled={!params.industry}
                        >
                            Next <i className="fas fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>
            )}
            
            {step === 2 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">What problem are you trying to solve?</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                        {categories.problemTypes.map(problemType => (
                            <button
                                key={problemType}
                                className={`p-3 rounded-lg border-2 text-left ${
                                    params.problemType === problemType 
                                        ? 'border-blue-500 bg-blue-50' 
                                        : 'border-gray-300 hover:border-blue-300'
                                }`}
                                onClick={() => setParams({...params, problemType})}
                            >
                                {problemType}
                            </button>
                        ))}
                    </div>
                    <div className="flex justify-between mt-4">
                        <button 
                            className="py-2 px-4 rounded-lg border border-gray-300 hover:bg-gray-100"
                            onClick={handlePrevStep}
                        >
                            <i className="fas fa-arrow-left mr-2"></i> Back
                        </button>
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleNextStep}
                            disabled={!params.problemType}
                        >
                            Next <i className="fas fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>
            )}
            
            {step === 3 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">What type of building is it for?</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                        {categories.buildingTypes.map(buildingType => (
                            <button
                                key={buildingType}
                                className={`p-3 rounded-lg border-2 text-left ${
                                    params.buildingType === buildingType 
                                        ? 'border-blue-500 bg-blue-50' 
                                        : 'border-gray-300 hover:border-blue-300'
                                }`}
                                onClick={() => setParams({...params, buildingType})}
                            >
                                {buildingType}
                            </button>
                        ))}
                    </div>
                    <div className="flex justify-between mt-4">
                        <button 
                            className="py-2 px-4 rounded-lg border border-gray-300 hover:bg-gray-100"
                            onClick={handlePrevStep}
                        >
                            <i className="fas fa-arrow-left mr-2"></i> Back
                        </button>
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleNextStep}
                            disabled={!params.buildingType}
                        >
                            Next <i className="fas fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>
            )}
            
            {step === 4 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">Additional Requirements (Optional)</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Project Size</label>
                            <select 
                                className="w-full p-2 border border-gray-300 rounded-md"
                                value={params.projectSize}
                                onChange={(e) => setParams({...params, projectSize: e.target.value})}
                            >
                                <option value="">Select project size</option>
                                {categories.projectSizes.map(size => (
                                    <option key={size} value={size}>{size}</option>
                                ))}
                            </select>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Application</label>
                            <select 
                                className="w-full p-2 border border-gray-300 rounded-md"
                                value={params.application}
                                onChange={(e) => setParams({...params, application: e.target.value})}
                            >
                                <option value="">Select application</option>
                                {categories.applications.map(app => (
                                    <option key={app} value={app}>{app}</option>
                                ))}
                            </select>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Glazing Type</label>
                            <select 
                                className="w-full p-2 border border-gray-300 rounded-md"
                                value={params.glazing}
                                onChange={(e) => setParams({...params, glazing: e.target.value})}
                            >
                                <option value="">Select glazing type</option>
                                {categories.glazingTypes.map(type => (
                                    <option key={type} value={type}>{type}</option>
                                ))}
                            </select>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Interior or Exterior</label>
                            <select 
                                className="w-full p-2 border border-gray-300 rounded-md"
                                value={params.useType}
                                onChange={(e) => setParams({...params, useType: e.target.value})}
                            >
                                <option value="">Select use type</option>
                                {categories.useTypes.map(type => (
                                    <option key={type} value={type}>{type}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                    
                    <div className="flex justify-between mt-4">
                        <button 
                            className="py-2 px-4 rounded-lg border border-gray-300 hover:bg-gray-100"
                            onClick={handlePrevStep}
                        >
                            <i className="fas fa-arrow-left mr-2"></i> Back
                        </button>
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleSearch}
                        >
                            Find Solutions <i className="fas fa-search ml-2"></i>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

// Result Card Component
const ResultCard = ({ item }) => {
    const [expanded, setExpanded] = React.useState(false);
    const [relatedItems, setRelatedItems] = React.useState([]);
    const [loadingRelated, setLoadingRelated] = React.useState(false);
    const [error, setError] = React.useState(null);
    
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
            const data = await API.getRelated(item.id);
            setRelatedItems(data.results || []);
        } catch (err) {
            console.error('Error loading related items:', err);
            setError('Failed to load related items');
        } finally {
            setLoadingRelated(false);
        }
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
                <p className="text-gray-600 mb-4">{item.description}</p>
                
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

// Hero Component
const Hero = () => {
    return (
        <div className="colt-gradient text-white py-12 px-4">
            <div className="container mx-auto">
                <div className="max-w-3xl">
                    <h1 className="text-4xl font-bold mb-4">Find the Perfect Colt Solution for Your Building</h1>
                    <p className="text-xl mb-6">Our intelligent wayfinder helps you navigate Colt's comprehensive range of smoke control, ventilation, and climate control solutions.</p>
                    <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                        <a href="#guided-search" className="colt-btn py-3 px-6 rounded-lg text-center">
                            Start Guided Search
                        </a>
                        <a href="#product-catalog" className="bg-transparent border-2 border-white py-3 px-6 rounded-lg hover:bg-white hover:text-gray-800 transition-colors text-center">
                            Browse Products
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Main App Component
const App = () => {
    const [searchResults, setSearchResults] = React.useState([]);
    const [searching, setSearching] = React.useState(false);
    const [searchPerformed, setSearchPerformed] = React.useState(false);
    const [error, setError] = React.useState(null);
    
    const handleSearch = async (query) => {
        setSearching(true);
        setSearchPerformed(true);
        setError(null);
        try {
            const data = await API.search(query);
            setSearchResults(data.results || []);
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
            const data = await API.guidedSearch(params);
            setSearchResults(data.results || []);
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
                <div className="flex flex-col lg:flex-row lg:space-x-8">
                    <div className="lg:w-2/3">
                        <Search onSearch={handleSearch} />
                        
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
                                            <div>
                                                {searchResults.map(item => (
                                                    <ResultCard key={item.id} item={item} />
                                                ))}
                                            </div>
                                        ) : (
                                            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
                                                <i className="fas fa-search text-4xl text-gray-400 mb-4"></i>
                                                <h3 className="text-xl font-bold text-gray-800 mb-2">No results found</h3>
                                                <p className="text-gray-600">
                                                    Try adjusting your search terms or use the guided search below.
                                                </p>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                    
                    <div className="lg:w-1/3" id="guided-search">
                        <GuidedSearch onSearch={handleGuidedSearch} />
                        
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
            </main>
            
            <footer className="bg-gray-800 text-white py-8">
                <div className="container mx-auto px-4">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        <div>
                            <h4 className="text-lg font-bold mb-4">About Colt</h4>
                            <p className="text-gray-400">
                                Pioneers in smoke control, ventilation and climate control solutions since 1931.
                            </p>
                        </div>
                        <div>
                            <h4 className="text-lg font-bold mb-4">Products</h4>
                            <ul className="space-y-2">
                                <li><a href="#" className="text-gray-400 hover:text-white">Smoke Control</a></li>
                                <li><a href="#" className="text-gray-400 hover:text-white">Ventilation</a></li>
                                <li><a href="#" className="text-gray-400 hover:text-white">Climate Control</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="text-lg font-bold mb-4">Support</h4>
                            <ul className="space-y-2">
                                <li><a href="#" className="text-gray-400 hover:text-white">Technical Support</a></li>
                                <li><a href="#" className="text-gray-400 hover:text-white">Documentation</a></li>
                                <li><a href="#" className="text-gray-400 hover:text-white">Contact Us</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="text-lg font-bold mb-4">Connect</h4>
                            <div className="flex space-x-4">
                                <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-linkedin"></i></a>
                                <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-twitter"></i></a>
                                <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-youtube"></i></a>
                            </div>
                        </div>
                    </div>
                    <div className="border-t border-gray-700 mt-8 pt-6 text-center text-gray-500">
                        <p> 2025 Colt International. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

// Render the App
ReactDOM.render(<App />, document.getElementById('app'));
