import React from 'react';
import PropTypes from 'prop-types';

/**
 * Loading spinner component
 * 
 * Displays a spinning animation for loading states
 */
export const LoadingSpinner = () => {
    return (
        <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
    );
};

/**
 * Error message component
 * 
 * Displays an error message with appropriate styling
 */
export const ErrorMessage = ({ message }) => {
    return (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative my-4" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{message}</span>
        </div>
    );
};

ErrorMessage.propTypes = {
    message: PropTypes.string.isRequired
};
