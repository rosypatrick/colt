import React from 'react';

/**
 * Hero component for the Colt Wayfinder application
 * 
 * Displays the main hero section with call-to-action buttons
 */
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

export default Hero;
