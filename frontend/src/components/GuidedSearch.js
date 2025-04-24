import React, { useState, useEffect, useMemo } from 'react';
import PropTypes from 'prop-types';
import { LoadingSpinner, ErrorMessage } from './UIComponents';

/**
 * GuidedSearch component for the Colt Wayfinder application
 * 
 * Provides a step-by-step guided search experience for users
 */
const GuidedSearch = ({ onSearch, apiClient }) => {
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [categories, setCategories] = useState(null);
    const [params, setParams] = useState({
        industry: '',
        problemType: '',
        buildingType: '',
        productDimensions: '', 
        application: '',
        glazing: '',
        useType: '',
        cvValue: '',
        uValue: '',
        acousticsValue: ''
    });
    
    // Define relationships between industries and building types
    const industryBuildingTypeMap = {
        'Healthcare': ['Hospital', 'Medical Center', 'Clinic', 'Laboratory', 'Care Home'],
        'Commercial Real Estate': ['Office Building', 'Corporate Headquarters', 'Business Park'],
        'Manufacturing': ['Factory', 'Production Facility', 'Industrial Plant'],
        'Retail': ['Shopping Center', 'Retail Store', 'Mall', 'Supermarket'],
        'Logistics': ['Warehouse', 'Distribution Center', 'Logistics Hub'],
        'Warehousing': ['Warehouse', 'Storage Facility', 'Cold Storage'],
        // Default case for any industry not explicitly mapped
        'default': ['Office Building', 'Factory', 'Warehouse', 'Shopping Center', 'Hospital', 'Data Center']
    };
    
    // Define relationships between industries and problem types
    const industryProblemTypeMap = {
        'Healthcare': ['Smoke Control', 'Climate Control', 'Ventilation', 'Noise Reduction'],
        'Commercial Real Estate': ['Smoke Control', 'Climate Control', 'Ventilation', 'Energy Efficiency'],
        'Manufacturing': ['Smoke Control', 'Ventilation', 'Climate Control', 'Energy Efficiency'],
        'Retail': ['Climate Control', 'Ventilation', 'Energy Efficiency', 'Smoke Control'],
        'Logistics': ['Ventilation', 'Smoke Control', 'Climate Control'],
        'Warehousing': ['Ventilation', 'Smoke Control', 'Climate Control'],
        // Default case
        'default': ['Smoke Control', 'Climate Control', 'Ventilation', 'Energy Efficiency', 'Noise Reduction', 'Louvre']
    };
    
    // Fetch categories on component mount
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                setLoading(true);
                setError(null);
                const data = await apiClient.getCategories();
                setCategories(data);
            } catch (err) {
                setError('Failed to load categories. Please try again later.');
                console.error('Error fetching categories:', err);
            } finally {
                setLoading(false);
            }
        };
        
        fetchCategories();
    }, [apiClient]);
    
    // Filter building types based on selected industry
    const filteredBuildingTypes = useMemo(() => {
        if (!categories || !params.industry) {
            return categories?.buildingTypes || [];
        }
        
        // Get the building types for the selected industry, or use default if not found
        const relevantTypes = industryBuildingTypeMap[params.industry] || industryBuildingTypeMap.default;
        
        // Filter the available building types to only include relevant ones
        return categories.buildingTypes.filter(type => 
            relevantTypes.some(relevantType => 
                type.toLowerCase().includes(relevantType.toLowerCase())
            )
        );
    }, [categories, params.industry]);
    
    // Filter problem types based on selected industry
    const filteredProblemTypes = useMemo(() => {
        if (!categories || !params.industry) {
            return categories?.problemTypes || [];
        }
        
        // Get the problem types for the selected industry, or use default if not found
        const relevantTypes = industryProblemTypeMap[params.industry] || industryProblemTypeMap.default;
        
        // Filter the available problem types to only include relevant ones
        return categories.problemTypes.filter(type => 
            relevantTypes.some(relevantType => 
                type.toLowerCase().includes(relevantType.toLowerCase())
            )
        );
    }, [categories, params.industry]);
    
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
        
        // Map productDimensions back to projectSize for API compatibility
        if (filteredParams.productDimensions) {
            filteredParams.projectSize = filteredParams.productDimensions;
            delete filteredParams.productDimensions;
        }
        
        onSearch(filteredParams);
    };
    
    // Handle parameter change with validation
    const handleParamChange = (paramName, value) => {
        // Create a new params object
        const newParams = { ...params, [paramName]: value };
        
        // If changing industry, reset building type if it's not valid for the new industry
        if (paramName === 'industry') {
            const relevantTypes = industryBuildingTypeMap[value] || industryBuildingTypeMap.default;
            const isCurrentBuildingTypeValid = relevantTypes.some(type => 
                params.buildingType.toLowerCase().includes(type.toLowerCase())
            );
            
            if (params.buildingType && !isCurrentBuildingTypeValid) {
                newParams.buildingType = '';
            }
            
            // Also reset problem type if changing industry
            const relevantProblemTypes = industryProblemTypeMap[value] || industryProblemTypeMap.default;
            const isCurrentProblemTypeValid = relevantProblemTypes.some(type => 
                params.problemType.toLowerCase().includes(type.toLowerCase())
            );
            
            if (params.problemType && !isCurrentProblemTypeValid) {
                newParams.problemType = '';
            }
        }
        
        setParams(newParams);
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
                                onClick={() => handleParamChange('industry', industry)}
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
                        {filteredProblemTypes.map(problemType => (
                            <button
                                key={problemType}
                                className={`p-3 rounded-lg border-2 text-left ${
                                    params.problemType === problemType 
                                        ? 'border-blue-500 bg-blue-50' 
                                        : 'border-gray-300 hover:border-blue-300'
                                }`}
                                onClick={() => handleParamChange('problemType', problemType)}
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
                    <h3 className="text-lg font-semibold mb-3">Additional Details</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Building Type</label>
                            <select 
                                className="w-full p-2 border border-gray-300 rounded-md"
                                value={params.buildingType}
                                onChange={(e) => handleParamChange('buildingType', e.target.value)}
                            >
                                <option value="">Select building type</option>
                                {filteredBuildingTypes.map(type => (
                                    <option key={type} value={type}>{type}</option>
                                ))}
                            </select>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Product Dimensions</label>
                            <select 
                                className="w-full p-2 border border-gray-300 rounded-md"
                                value={params.productDimensions}
                                onChange={(e) => handleParamChange('productDimensions', e.target.value)}
                            >
                                <option value="">Select product dimensions</option>
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
                                onChange={(e) => handleParamChange('application', e.target.value)}
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
                                onChange={(e) => handleParamChange('glazing', e.target.value)}
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
                                onChange={(e) => handleParamChange('useType', e.target.value)}
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

GuidedSearch.propTypes = {
    onSearch: PropTypes.func.isRequired,
    apiClient: PropTypes.object.isRequired
};

export default GuidedSearch;
