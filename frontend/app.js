// Mock API for demo purposes
const API = {
    search: (query) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                const results = MOCK_DATA.filter(item => 
                    item.title.toLowerCase().includes(query.toLowerCase()) ||
                    item.description.toLowerCase().includes(query.toLowerCase())
                );
                resolve(results);
            }, 500);
        });
    },
    
    guidedSearch: (params) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                let results = MOCK_DATA;
                
                if (params.industry) {
                    results = results.filter(item => {
                        if (item.type === 'solution' && item.industries) {
                            return item.industries.some(ind => ind.toLowerCase() === params.industry.toLowerCase());
                        }
                        return false;
                    });
                }
                
                if (params.problemType) {
                    const problemTypeResults = MOCK_DATA.filter(item => {
                        if (item.type === 'product' && item.categories) {
                            return item.categories.some(cat => cat.toLowerCase() === params.problemType.toLowerCase());
                        }
                        return false;
                    });
                    
                    problemTypeResults.forEach(item => {
                        item.recommendationType = 'Suggested Product';
                    });
                    
                    results = [...results, ...problemTypeResults];
                }
                
                results.forEach(item => {
                    if (!item.recommendationType) {
                        if (item.type === 'solution') {
                            item.recommendationType = 'Recommended Solution';
                        } else if (item.type === 'product') {
                            item.recommendationType = 'Suggested Product';
                        } else if (item.type === 'technical_document') {
                            item.recommendationType = 'Helpful Resource';
                        }
                    }
                });
                
                const uniqueResults = [];
                const ids = new Set();
                results.forEach(item => {
                    if (!ids.has(item.id)) {
                        ids.add(item.id);
                        uniqueResults.push(item);
                    }
                });
                
                resolve(uniqueResults);
            }, 800);
        });
    },
    
    getRelated: (itemId) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                const item = MOCK_DATA.find(i => i.id === itemId);
                if (!item) {
                    resolve([]);
                    return;
                }
                
                let relatedIds = [];
                
                if (item.type === 'product') {
                    MOCK_DATA.forEach(i => {
                        if (i.type === 'solution' && i.relatedProducts && i.relatedProducts.includes(item.id)) {
                            relatedIds.push(i.id);
                        }
                    });
                    
                    const categories = item.categories || [];
                    MOCK_DATA.forEach(i => {
                        if (i.type === 'product' && i.id !== item.id && i.categories) {
                            for (const cat of categories) {
                                if (i.categories.includes(cat)) {
                                    relatedIds.push(i.id);
                                    break;
                                }
                            }
                        }
                    });
                }
                
                if (item.type === 'solution') {
                    relatedIds = [...(item.relatedProducts || [])];
                }
                
                const related = relatedIds
                    .map(id => MOCK_DATA.find(i => i.id === id))
                    .filter(Boolean);
                
                const technicalDocs = MOCK_DATA.filter(i => 
                    i.type === 'technical_document' && 
                    ((i.relatedProducts && i.relatedProducts.includes(item.id)) ||
                     (i.relatedSolutions && i.relatedSolutions.includes(item.id)))
                );
                
                resolve([...related, ...technicalDocs]);
            }, 600);
        });
    }
};

// Mock data for demo
const MOCK_DATA = [
    {
        id: 'p1',
        type: 'product',
        title: 'Industrial Exhaust Fan Series 500',
        description: 'Heavy-duty exhaust fans designed for smoke extraction in industrial environments.',
        specifications: {
            'Temperature Rating': '400°C for 2 hours',
            'Airflow': 'Up to 45,000 m³/h',
        },
        categories: ['Smoke Control', 'Ventilation', 'Industrial'],
        url: 'http://colt.info/gb/en/products/smoke-control-ventilation/exhaust-fans'
    },
    {
        id: 'p2',
        type: 'product',
        title: 'EcoVent Air Handling Unit',
        description: 'Energy-efficient air handling units for commercial buildings.',
        specifications: {
            'Airflow': '1,000 - 25,000 m³/h',
            'Heat Recovery Efficiency': 'Up to 85%',
        },
        categories: ['Climate Control', 'Energy Efficiency', 'Commercial'],
        url: 'http://colt.info/gb/en/products/climate-control/air-handling-units'
    },
    {
        id: 'p3',
        type: 'product',
        title: 'SkyLite Natural Ventilator',
        description: 'Roof-mounted natural ventilators for day-to-day ventilation and smoke control.',
        specifications: {
            'Aerodynamic Free Area': '1.0 - 6.0 m²',
            'Installation': 'Roof-mounted',
        },
        categories: ['Smoke Control', 'Natural Ventilation', 'Sustainable'],
        url: 'http://colt.info/gb/en/products/smoke-control-ventilation/natural-ventilators'
    },
    {
        id: 's1',
        type: 'solution',
        title: 'Smoke Control for Commercial Buildings',
        description: 'Comprehensive smoke control solutions for office buildings, shopping centers, and multi-purpose commercial spaces.',
        industries: ['Commercial Real Estate', 'Retail', 'Office Buildings'],
        relatedProducts: ['p1', 'p3'],
        url: 'http://colt.info/gb/en/solutions/commercial-buildings'
    },
    {
        id: 's2',
        type: 'solution',
        title: 'Climate Control for Industrial Facilities',
        description: 'Energy-efficient climate control solutions for manufacturing plants, warehouses, and industrial facilities.',
        industries: ['Manufacturing', 'Logistics', 'Warehousing'],
        relatedProducts: ['p1', 'p2'],
        url: 'http://colt.info/gb/en/solutions/industrial-facilities'
    },
    {
        id: 'd1',
        type: 'technical_document',
        title: 'Guide to Smoke Control Regulations in Commercial Buildings',
        description: 'Comprehensive guide to regulatory requirements for smoke control systems.',
        docType: 'pdf',
        relatedProducts: ['p1', 'p3'],
        relatedSolutions: ['s1'],
        url: 'http://colt.info/gb/en/technical/whitepapers/smoke-control-regulations'
    },
    {
        id: 'd2',
        type: 'technical_document',
        title: 'Case Study: Energy Optimization in Manufacturing',
        description: 'Learn how a manufacturing facility reduced energy consumption by 35%.',
        docType: 'pdf',
        relatedProducts: ['p2'],
        relatedSolutions: ['s2'],
        url: 'http://colt.info/gb/en/technical/case-studies/manufacturing-climate-control'
    }
];

// React Components
const Header = () => (
    <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
            <div className="flex items-center">
                <div className="mr-4 w-20 h-10 bg-gray-300 flex items-center justify-center text-gray-700 font-bold">COLT</div>
                <h1 className="text-xl font-bold text-gray-800">Wayfinder</h1>
            </div>
            <nav>
                <ul className="flex space-x-6">
                    <li><a href="#" className="text-gray-600 hover:text-blue-500">Products</a></li>
                    <li><a href="#" className="text-gray-600 hover:text-blue-500">Solutions</a></li>
                    <li><a href="#" className="text-gray-600 hover:text-blue-500">Resources</a></li>
                </ul>
            </nav>
        </div>
    </header>
);

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
        <div className="my-6">
            <form onSubmit={handleSubmit} className="search-box flex items-center bg-white rounded-full overflow-hidden px-4 py-2">
                <input
                    type="text"
                    placeholder="Search for products, solutions, or documentation..."
                    className="flex-grow outline-none px-2 py-1"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className="ml-2 colt-btn rounded-full w-10 h-10 flex items-center justify-center">
                    <i className="fas fa-search"></i>
                </button>
            </form>
        </div>
    );
};

// Guided Search Component
const GuidedSearch = ({ onSearch }) => {
    const [industry, setIndustry] = React.useState('');
    const [problemType, setProblemType] = React.useState('');
    const [buildingType, setBuildingType] = React.useState('');
    const [step, setStep] = React.useState(1);
    
    const industries = ['Commercial Real Estate', 'Manufacturing', 'Retail', 'Warehousing'];
    const problemTypes = ['Smoke Control', 'Climate Control', 'Ventilation', 'Energy Efficiency'];
    const buildingTypes = ['Office Building', 'Factory', 'Warehouse', 'Shopping Center'];
    
    const handleNextStep = () => setStep(step + 1);
    const handlePrevStep = () => setStep(step - 1);
    
    const handleSearch = () => {
        onSearch({
            industry,
            problemType,
            buildingType
        });
    };
    
    return (
        <div className="bg-white rounded-lg shadow-lg p-6 my-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Find the Right Solution</h2>
            <p className="text-gray-600 mb-6">Tell us about your project, and we'll guide you to the best Colt solutions.</p>
            
            {step === 1 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">What industry are you in?</h3>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                        {industries.map(ind => (
                            <button
                                key={ind}
                                className={`p-3 rounded-lg border transition-all ${industry === ind ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                                onClick={() => setIndustry(ind)}
                            >
                                {ind}
                            </button>
                        ))}
                    </div>
                    <div className="flex justify-end mt-4">
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleNextStep}
                            disabled={!industry}
                        >
                            Next <i className="fas fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>
            )}
            
            {step === 2 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">What problem are you trying to solve?</h3>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                        {problemTypes.map(type => (
                            <button
                                key={type}
                                className={`p-3 rounded-lg border transition-all ${problemType === type ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                                onClick={() => setProblemType(type)}
                            >
                                {type}
                            </button>
                        ))}
                    </div>
                    <div className="flex justify-between mt-4">
                        <button 
                            className="border border-gray-300 py-2 px-4 rounded-lg text-gray-600 hover:bg-gray-50"
                            onClick={handlePrevStep}
                        >
                            <i className="fas fa-arrow-left mr-2"></i> Back
                        </button>
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleNextStep}
                            disabled={!problemType}
                        >
                            Next <i className="fas fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>
            )}
            
            {step === 3 && (
                <div className="wayfinder-step">
                    <h3 className="text-lg font-semibold mb-3">What type of building?</h3>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                        {buildingTypes.map(type => (
                            <button
                                key={type}
                                className={`p-3 rounded-lg border transition-all ${buildingType === type ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                                onClick={() => setBuildingType(type)}
                            >
                                {type}
                            </button>
                        ))}
                    </div>
                    <div className="flex justify-between mt-4">
                        <button 
                            className="border border-gray-300 py-2 px-4 rounded-lg text-gray-600 hover:bg-gray-50"
                            onClick={handlePrevStep}
                        >
                            <i className="fas fa-arrow-left mr-2"></i> Back
                        </button>
                        <button 
                            className="colt-btn py-2 px-4 rounded-lg"
                            onClick={handleSearch}
                            disabled={!buildingType}
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
    
    const toggleExpand = () => {
        setExpanded(!expanded);
        if (!expanded && !relatedItems.length && !loadingRelated) {
            loadRelatedItems();
        }
    };
    
    const loadRelatedItems = async () => {
        setLoadingRelated(true);
        try {
            const related = await API.getRelated(item.id);
            setRelatedItems(related);
        } finally {
            setLoadingRelated(false);
        }
    };
    
    return (
        <div className="solution-card bg-white rounded-lg shadow-lg overflow-hidden mb-6">
            <div className="p-6">
                {item.recommendationType && (
                    <div className="mb-2">
                        <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                            {item.recommendationType}
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
                    <a 
                        href={item.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="colt-btn py-2 px-4 rounded-lg"
                    >
                        View Details
                    </a>
                </div>
            </div>
            
            {expanded && (
                <div className="p-6 border-t border-gray-200">
                    {item.type === 'product' && item.specifications && (
                        <div className="mb-6">
                            <h4 className="text-lg font-semibold mb-2">Specifications</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {Object.entries(item.specifications).map(([key, value]) => (
                                    <div key={key} className="border-b border-gray-100 pb-2">
                                        <span className="text-gray-500">{key}:</span> <span className="font-medium">{value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                    
                    <div>
                        <h4 className="text-lg font-semibold mb-2">Related Items</h4>
                        {loadingRelated ? (
                            <p className="text-gray-500">Loading related items...</p>
                        ) : relatedItems.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {relatedItems.map(related => (
                                    <div key={related.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                                        <h5 className="font-medium mb-2">{related.title}</h5>
                                        <p className="text-sm text-gray-500 mb-2">{related.type === 'product' ? 'Product' : related.type === 'solution' ? 'Solution' : 'Document'}</p>
                                        <a href={related.url} className="text-blue-500 hover:underline text-sm">
                                            View Details
                                        </a>
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
const Hero = () => (
    <div className="colt-gradient text-white py-12 px-4">
        <div className="container mx-auto">
            <div className="max-w-3xl">
                <h1 className="text-4xl font-bold mb-4">Find the Perfect Colt Solution for Your Building</h1>
                <p className="text-xl mb-6">Our intelligent wayfinder helps you navigate Colt's comprehensive range of smoke control, ventilation, and climate control solutions.</p>
                <div className="flex space-x-4">
                    <a href="#guided-search" className="colt-btn py-3 px-6 rounded-lg">
                        Start Guided Search
                    </a>
                    <a href="#product-catalog" className="bg-transparent border-2 border-white py-3 px-6 rounded-lg hover:bg-white hover:text-gray-800 transition-colors">
                        Browse Products
                    </a>
                </div>
            </div>
        </div>
    </div>
);

// Main App Component
const App = () => {
    const [searchResults, setSearchResults] = React.useState([]);
    const [searching, setSearching] = React.useState(false);
    const [searchPerformed, setSearchPerformed] = React.useState(false);
    
    const handleSearch = async (query) => {
        setSearching(true);
        setSearchPerformed(true);
        try {
            const results = await API.search(query);
            setSearchResults(results);
        } finally {
            setSearching(false);
        }
    };
    
    const handleGuidedSearch = async (params) => {
        setSearching(true);
        setSearchPerformed(true);
        try {
            const results = await API.guidedSearch(params);
            setSearchResults(results);
        } finally {
            setSearching(false);
        }
    };
    
    return (
        <div className="min-h-screen flex flex-col">
            <Header />
            <Hero />
            
            <main className="container mx-auto px-4 py-8 flex-grow">
                <div className="flex flex-col md:flex-row md:space-x-8">
                    <div className="md:w-2/3">
                        <Search onSearch={handleSearch} />
                        
                        {searchPerformed && (
                            <div className="my-6">
                                {searching ? (
                                    <div className="flex justify-center items-center py-12">
                                        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                                    </div>
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
                    
                    <div className="md:w-1/3" id="guided-search">
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
                        <p>© 2025 Colt International. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

// Render the App
ReactDOM.render(<App />, document.getElementById('app'));
