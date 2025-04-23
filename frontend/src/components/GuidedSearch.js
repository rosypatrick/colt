import React, { useState, useEffect } from 'react';
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
        projectSize: '',
        application: '',
        glazing: '',
        useType: '',
        cvValue: '',
        uValue: '',
        acousticsValue: ''
    });
    
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

GuidedSearch.propTypes = {
    onSearch: PropTypes.func.isRequired,
    apiClient: PropTypes.object.isRequired
};

export default GuidedSearch;
