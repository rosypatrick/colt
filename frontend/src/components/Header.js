import React from 'react';

/**
 * Header component for the Colt Wayfinder application
 * 
 * Displays the main navigation header with logo and menu items
 */
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

export default Header;
