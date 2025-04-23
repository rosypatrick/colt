import React from 'react';

/**
 * Footer component for the Colt Wayfinder application
 * 
 * Displays the site footer with links and company information
 */
const Footer = () => {
    return (
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
                    <p>© {new Date().getFullYear()} Colt International. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
