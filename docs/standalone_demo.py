                // Populate all the advanced options
                const projectSizeSelect = document.getElementById('project-size');
                data.projectSizes.forEach(size => {
                    const option = document.createElement('option');
                    option.value = size;
                    option.textContent = size;
                    projectSizeSelect.appendChild(option);
                });
                
                const applicationSelect = document.getElementById('application');
                data.applications.forEach(app => {
                    const option = document.createElement('option');
                    option.value = app;
                    option.textContent = app;
                    applicationSelect.appendChild(option);
                });
                
                const glazingSelect = document.getElementById('glazing');
                data.glazingTypes.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    option.textContent = type;
                    glazingSelect.appendChild(option);
                });
                
                const useTypeSelect = document.getElementById('use-type');
                data.useTypes.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    option.textContent = type;
                    useTypeSelect.appendChild(option);
                });
                
                const cvValueSelect = document.getElementById('cv-value');
                data.cvValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = value;
                    cvValueSelect.appendChild(option);
                });
                
                const uValueSelect = document.getElementById('u-value');
                data.uValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = value;
                    uValueSelect.appendChild(option);
                });
                
                const acousticsValueSelect = document.getElementById('acoustics-value');
                data.acousticsValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = value;
                    acousticsValueSelect.appendChild(option);
                });                // Populate all the advanced options
                const projectSizeSelect = document.getElementById('project-size');
                data.projectSizes.forEach(size => {
                    const option = document.createElement('option');
                    option.value = size;
                    option.textContent = size;
                    projectSizeSelect.appendChild(option);
                });
                
                const applicationSelect = document.getElementById('application');
                data.applications.forEach(app => {
                    const option = document.createElement('option');
                    option.value = app;
                    option.textContent = app;
                    applicationSelect.appendChild(option);
                });
                
                const glazingSelect = document.getElementById('glazing');
                data.glazingTypes.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    option.textContent = type;
                    glazingSelect.appendChild(option);
                });
                
                const useTypeSelect = document.getElementById('use-type');
                data.useTypes.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    option.textContent = type;
                    useTypeSelect.appendChild(option);
                });
                
                const cvValueSelect = document.getElementById('cv-value');
                data.cvValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = value;
                    cvValueSelect.appendChild(option);
                });
                
                const uValueSelect = document.getElementById('u-value');
                data.uValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = value;
                    uValueSelect.appendChild(option);
                });
                
                const acousticsValueSelect = document.getElementById('acoustics-value');
                data.acousticsValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = value;
                    acousticsValueSelect.appendChild(option);
                });"""
Colt Wayfinder Tool - Standalone Demo

A completely self-contained demo of the Colt Wayfinder tool that doesn't require
any external dependencies beyond the Python standard library.
"""

import http.server
import socketserver
import json
import os
import webbrowser
import threading
import time
from urllib.parse import parse_qs, urlparse

# Sample data for the demo
SAMPLE_DATA = [
    {
        "id": "p1",
        "type": "product",
        "title": "Industrial Exhaust Fan Series 500",
        "description": "Heavy-duty exhaust fans designed for smoke extraction in industrial environments.",
        "specifications": {
            "Temperature Rating": "400°C for 2 hours",
            "Airflow": "Up to 45,000 m³/h",
            "Cv Value": "0.65 (High)",
            "U-Value": "2.4 W/m²K (Basic)",
            "Acoustics": "32 dB (Medium)"
        },
        "categories": ["Smoke Control", "Ventilation", "Industrial"],
        "projectAttributes": {
            "Application": "Roof",
            "Size": "Medium (500-2000 m²)",
            "Glazing": "Not Applicable",
            "UseType": "Exterior"
        },
        "url": "#product-p1"
    },
    {
        "id": "p2",
        "type": "product",
        "title": "EcoVent Air Handling Unit",
        "description": "Energy-efficient air handling units for commercial buildings.",
        "specifications": {
            "Airflow": "1,000 - 25,000 m³/h",
            "Heat Recovery": "Up to 85%",
            "Cv Value": "0.55 (Medium)",
            "U-Value": "0.9 W/m²K (Good)",
            "Acoustics": "25 dB (Low)"
        },
        "categories": ["Climate Control", "Energy Efficiency", "Commercial"],
        "projectAttributes": {
            "Application": "Wall",
            "Size": "Large (2000-10000 m²)",
            "Glazing": "Double Glazed",
            "UseType": "Interior"
        },
        "url": "#product-p2"
    },
    {
        "id": "p3",
        "type": "product",
        "title": "SkyLite Natural Ventilator",
        "description": "Roof-mounted natural ventilators for day-to-day ventilation and smoke control.",
        "specifications": {
            "Area": "1.0 - 6.0 m²",
            "Installation": "Roof-mounted",
            "Cv Value": "0.35 (Low)",
            "U-Value": "1.7 W/m²K (Standard)",
            "Acoustics": "45 dB (High)"
        },
        "categories": ["Smoke Control", "Natural Ventilation", "Sustainable"],
        "projectAttributes": {
            "Application": "Window/Glazing System",
            "Size": "Small (< 500 m²)",
            "Glazing": "Single Glazed",
            "UseType": "Exterior"
        },
        "url": "#product-p3"
    },
    {
        "id": "s1",
        "type": "solution",
        "title": "Smoke Control for Commercial Buildings",
        "description": "Comprehensive smoke control solutions for office buildings and commercial spaces.",
        "industries": ["Commercial Real Estate", "Retail", "Office Buildings"],
        "relatedProducts": ["p1", "p3"],
        "url": "#solution-s1"
    },
    {
        "id": "s2",
        "type": "solution",
        "title": "Climate Control for Industrial Facilities",
        "description": "Energy-efficient climate control solutions for manufacturing plants and warehouses.",
        "industries": ["Manufacturing", "Logistics", "Warehousing"],
        "relatedProducts": ["p1", "p2"],
        "url": "#solution-s2"
    }
]

# Categories for filtering
CATEGORIES = {
    "industries": [
        "Commercial Real Estate",
        "Manufacturing",
        "Retail",
        "Warehousing"
    ],
    "problemTypes": [
        "Smoke Control",
        "Climate Control",
        "Ventilation",
        "Energy Efficiency"
    ],
    "buildingTypes": [
        "Office Building",
        "Factory",
        "Warehouse",
        "Shopping Center"
    ],
    "projectSizes": [
        "Small (< 500 m²)",
        "Medium (500-2000 m²)",
        "Large (2000-10000 m²)",
        "Extra Large (> 10000 m²)"
    ],
    "applications": [
        "Roof",
        "Wall",
        "Ceiling",
        "Window/Glazing System",
        "Screens/Partitions"
    ],
    "glazingTypes": [
        "Single Glazed",
        "Double Glazed",
        "Triple Glazed",
        "Not Applicable"
    ],
    "useTypes": [
        "Interior",
        "Exterior"
    ],
    "cvValues": [
        "Low (< 0.4)",
        "Medium (0.4-0.6)",
        "High (> 0.6)",
        "Not Specified"
    ],
    "uValues": [
        "Excellent (< 0.8 W/m²K)",
        "Good (0.8-1.2 W/m²K)",
        "Standard (1.2-2.0 W/m²K)",
        "Basic (> 2.0 W/m²K)",
        "Not Specified"
    ],
    "acousticsValues": [
        "Low (< 30 dB)",
        "Medium (30-40 dB)",
        "High (> 40 dB)",
        "Not Specified"
    ]
}

# Simple HTML template for the demo
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Colt Wayfinder Demo</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {
            --colt-primary: #33334d;
            --colt-secondary: #0098db;
        }
        body { background-color: #f5f7fa; }
        .colt-gradient { background: linear-gradient(135deg, var(--colt-primary) 0%, var(--colt-secondary) 100%); }
        .colt-btn { background-color: var(--colt-secondary); color: white; }
        .category-pill {
            background-color: var(--colt-primary); color: white; border-radius: 999px;
            padding: 0.25rem 0.75rem; font-size: 0.75rem; margin-right: 0.5rem; margin-bottom: 0.5rem;
            display: inline-block;
        }
    </style>
</head>
<body>
    <header class="bg-white shadow-md">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center">
                <div class="mr-4 w-20 h-10 bg-gray-300 flex items-center justify-center text-gray-700 font-bold">COLT</div>
                <h1 class="text-xl font-bold text-gray-800">Wayfinder</h1>
            </div>
            <nav>
                <ul class="flex space-x-6">
                    <li><a href="#" class="text-gray-600 hover:text-blue-500">Products</a></li>
                    <li><a href="#" class="text-gray-600 hover:text-blue-500">Solutions</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="colt-gradient text-white py-12 px-4">
        <div class="container mx-auto">
            <div class="max-w-3xl">
                <h1 class="text-4xl font-bold mb-4">Find the Perfect Colt Solution for Your Building</h1>
                <p class="text-xl mb-6">Our intelligent wayfinder helps you navigate Colt's comprehensive range of smoke control, ventilation, and climate control solutions.</p>
                <div class="flex space-x-4">
                    <a href="#guided-search" class="colt-btn py-3 px-6 rounded-lg">
                        Start Guided Search
                    </a>
                    <a href="#product-catalog" class="bg-transparent border-2 border-white py-3 px-6 rounded-lg hover:bg-white hover:text-gray-800 transition-colors">
                        Browse Products
                    </a>
                </div>
            </div>
        </div>
    </div>

    <main class="container mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row md:space-x-8">
            <div class="md:w-2/3">
                <div class="my-6">
                    <form id="search-form" class="flex items-center bg-white rounded-full overflow-hidden px-4 py-2 shadow-md">
                        <input
                            type="text"
                            id="search-input"
                            placeholder="Search for products, solutions, or documentation..."
                            class="flex-grow outline-none px-2 py-1"
                        />
                        <button type="submit" class="ml-2 colt-btn rounded-full w-10 h-10 flex items-center justify-center">
                            <i class="fas fa-search"></i>
                        </button>
                    </form>
                </div>
                
                <div id="results-container" class="my-6">
                    <div id="loading" class="hidden flex justify-center items-center py-12">
                        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                    
                    <div id="results" class="hidden">
                        <h2 class="text-2xl font-bold text-gray-800 mb-4">Search Results (<span id="result-count">0</span>)</h2>
                        <div id="result-list"></div>
                    </div>
                    
                    <div id="no-results" class="hidden bg-white rounded-lg shadow-lg p-6 text-center">
                        <i class="fas fa-search text-4xl text-gray-400 mb-4"></i>
                        <h3 class="text-xl font-bold text-gray-800 mb-2">No results found</h3>
                        <p class="text-gray-600">
                            Try adjusting your search terms or use the guided search below.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="md:w-1/3" id="guided-search">
                <div class="bg-white rounded-lg shadow-lg p-6 my-6">
                    <h2 class="text-2xl font-bold text-gray-800 mb-4">Find the Right Solution</h2>
                    <p class="text-gray-600 mb-6">Tell us about your project, and we'll guide you to the best Colt solutions.</p>
                    
                    <div id="guided-step-1">
                        <h3 class="text-lg font-semibold mb-3">What industry are you in?</h3>
                        <div class="grid grid-cols-2 gap-3 mb-4" id="industry-options"></div>
                        <div class="flex justify-end mt-4">
                            <button id="industry-next" class="colt-btn py-2 px-4 rounded-lg" disabled>
                                Next <i class="fas fa-arrow-right ml-2"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div id="guided-step-2" class="hidden">
                        <h3 class="text-lg font-semibold mb-3">What problem are you trying to solve?</h3>
                        <div class="grid grid-cols-2 gap-3 mb-4" id="problem-options"></div>
                        <div class="flex justify-between mt-4">
                            <button id="problem-back" class="border border-gray-300 py-2 px-4 rounded-lg text-gray-600 hover:bg-gray-50">
                                <i class="fas fa-arrow-left mr-2"></i> Back
                            </button>
                            <button id="problem-next" class="colt-btn py-2 px-4 rounded-lg" disabled>
                                Next <i class="fas fa-arrow-right ml-2"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div id="guided-step-3" class="hidden">
                        <h3 class="text-lg font-semibold mb-3">What type of building?</h3>
                        <div class="grid grid-cols-2 gap-3 mb-4" id="building-options"></div>
                        
                        <div class="mt-6">
                            <button id="toggle-advanced" class="flex items-center text-blue-500 hover:text-blue-700 transition-colors">
                                <i class="fas fa-chevron-right mr-2" id="advanced-icon"></i>
                                Show Advanced Options
                            </button>
                        </div>
                        
                        <div id="advanced-options" class="mt-4 p-4 border border-gray-200 rounded-lg hidden">
                            <h4 class="font-semibold text-gray-700 mb-3">Project Attributes</h4>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">Project Size</label>
                                <select id="project-size" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select project size (optional)</option>
                                </select>
                            </div>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">Application</label>
                                <select id="application" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select application (optional)</option>
                                </select>
                            </div>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">Glazing</label>
                                <select id="glazing" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select glazing type (optional)</option>
                                </select>
                            </div>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">Interior or Exterior</label>
                                <select id="use-type" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select use type (optional)</option>
                                </select>
                            </div>
                            
                            <h4 class="font-semibold text-gray-700 mb-3 mt-6">Performance Attributes</h4>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">
                                    Cv Value
                                    <span class="ml-1 text-xs text-gray-500">(air flow capacity)</span>
                                </label>
                                <select id="cv-value" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select Cv value (optional)</option>
                                </select>
                            </div>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">
                                    U-Value
                                    <span class="ml-1 text-xs text-gray-500">(thermal transmittance)</span>
                                </label>
                                <select id="u-value" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select U-value (optional)</option>
                                </select>
                            </div>
                            
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">
                                    Acoustics Value
                                    <span class="ml-1 text-xs text-gray-500">(sound reduction)</span>
                                </label>
                                <select id="acoustics-value" class="w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Select acoustics value (optional)</option>
                                </select>
                            </div>
                        </div>
                        <div class="flex justify-between mt-4">
                            <button id="building-back" class="border border-gray-300 py-2 px-4 rounded-lg text-gray-600 hover:bg-gray-50">
                                <i class="fas fa-arrow-left mr-2"></i> Back
                            </button>
                            <button id="find-solutions" class="colt-btn py-2 px-4 rounded-lg" disabled>
                                Find Solutions <i class="fas fa-search ml-2"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        let selectedIndustry = '';
        let selectedProblem = '';
        let selectedBuilding = '';
        let selectedProjectSize = '';
        let selectedApplication = '';
        let selectedGlazing = '';
        let selectedUseType = '';
        let selectedCvValue = '';
        let selectedUValue = '';
        let selectedAcousticsValue = '';
        let showAdvancedOptions = false;
        
        // Initialize categories
        fetch('/api/categories')
            .then(response => response.json())
            .then(data => {
                // Populate industry options
                const industryOptions = document.getElementById('industry-options');
                data.industries.forEach(industry => {
                    const button = document.createElement('button');
                    button.className = 'p-3 rounded-lg border border-gray-200 hover:border-blue-300';
                    button.textContent = industry;
                    button.addEventListener('click', () => {
                        // Deselect all buttons
                        industryOptions.querySelectorAll('button').forEach(btn => {
                            btn.className = 'p-3 rounded-lg border border-gray-200 hover:border-blue-300';
                        });
                        
                        // Select this button
                        button.className = 'p-3 rounded-lg border border-blue-500 bg-blue-50';
                        selectedIndustry = industry;
                        document.getElementById('industry-next').disabled = false;
                    });
                    industryOptions.appendChild(button);
                });
                
                // Populate problem options
                const problemOptions = document.getElementById('problem-options');
                data.problemTypes.forEach(problem => {
                    const button = document.createElement('button');
                    button.className = 'p-3 rounded-lg border border-gray-200 hover:border-blue-300';
                    button.textContent = problem;
                    button.addEventListener('click', () => {
                        problemOptions.querySelectorAll('button').forEach(btn => {
                            btn.className = 'p-3 rounded-lg border border-gray-200 hover:border-blue-300';
                        });
                        button.className = 'p-3 rounded-lg border border-blue-500 bg-blue-50';
                        selectedProblem = problem;
                        document.getElementById('problem-next').disabled = false;
                    });
                    problemOptions.appendChild(button);
                });
                
                // Populate building options
                const buildingOptions = document.getElementById('building-options');
                data.buildingTypes.forEach(building => {
                    const button = document.createElement('button');
                    button.className = 'p-3 rounded-lg border border-gray-200 hover:border-blue-300';
                    button.textContent = building;
                    button.addEventListener('click', () => {
                        buildingOptions.querySelectorAll('button').forEach(btn => {
                            btn.className = 'p-3 rounded-lg border border-gray-200 hover:border-blue-300';
                        });
                        button.className = 'p-3 rounded-lg border border-blue-500 bg-blue-50';
                        selectedBuilding = building;
                        document.getElementById('find-solutions').disabled = false;
                    });
                    buildingOptions.appendChild(button);
                });
            });
        
        // Step navigation
        document.getElementById('industry-next').addEventListener('click', () => {
            document.getElementById('guided-step-1').classList.add('hidden');
            document.getElementById('guided-step-2').classList.remove('hidden');
        });
        
        document.getElementById('problem-back').addEventListener('click', () => {
            document.getElementById('guided-step-2').classList.add('hidden');
            document.getElementById('guided-step-1').classList.remove('hidden');
        });
        
        document.getElementById('problem-next').addEventListener('click', () => {
            document.getElementById('guided-step-2').classList.add('hidden');
            document.getElementById('guided-step-3').classList.remove('hidden');
        });
        
        document.getElementById('building-back').addEventListener('click', () => {
            document.getElementById('guided-step-3').classList.add('hidden');
            document.getElementById('guided-step-2').classList.remove('hidden');
        });
        
        // Search handlers
        document.getElementById('find-solutions').addEventListener('click', () => {
            const params = {
                industry: selectedIndustry,
                problemType: selectedProblem,
                buildingType: selectedBuilding
            };
            
            fetch('/api/guided-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            })
                .then(response => response.json())
                .then(data => displayResults(data.results));
        });
        
        document.getElementById('search-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('search-input').value.trim();
            if (query) {
                fetch(`/api/search?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => displayResults(data.results));
            }
        });
        
        function displayResults(results) {
            const resultList = document.getElementById('result-list');
            resultList.innerHTML = '';
            
            document.getElementById('loading').classList.add('hidden');
            
            if (results.length === 0) {
                document.getElementById('no-results').classList.remove('hidden');
                document.getElementById('results').classList.add('hidden');
                return;
            }
            
            document.getElementById('result-count').textContent = results.length;
            document.getElementById('results').classList.remove('hidden');
            document.getElementById('no-results').classList.add('hidden');
            
            results.forEach(item => {
                const card = document.createElement('div');
                card.className = 'bg-white rounded-lg shadow-lg overflow-hidden mb-6';
                
                let html = `
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">${item.title}</h3>
                        <p class="text-gray-600 mb-4">${item.description}</p>
                `;
                
                if (item.type === 'product' && item.categories) {
                    html += '<div class="mb-4">';
                    item.categories.forEach(cat => {
                        html += `<span class="category-pill">${cat}</span>`;
                    });
                    html += '</div>';
                }
                
                html += `
                        <div class="flex justify-between items-center mt-2">
                            <button class="toggle-details text-blue-500 hover:text-blue-700 font-medium flex items-center">
                                Show More <i class="fas fa-chevron-down ml-1"></i>
                            </button>
                            <a href="${item.url}" class="colt-btn py-2 px-4 rounded-lg">
                                View Details
                            </a>
                        </div>
                    </div>
                    
                    <div class="details p-6 border-t border-gray-200 hidden">
                `;
                
                if (item.type === 'product' && item.specifications) {
                    html += '<div class="mb-6"><h4 class="text-lg font-semibold mb-2">Specifications</h4><div class="grid grid-cols-2 gap-4">';
                    
                    Object.entries(item.specifications).forEach(([key, value]) => {
                        html += `
                            <div class="border-b border-gray-100 pb-2">
                                <span class="text-gray-500">${key}:</span> <span class="font-medium">${value}</span>
                            </div>
                        `;
                    });
                    
                    html += '</div></div>';
                }
                
                html += '</div>';
                
                card.innerHTML = html;
                
                // Toggle details
                const toggleButton = card.querySelector('.toggle-details');
                const detailsSection = card.querySelector('.details');
                
                toggleButton.addEventListener('click', () => {
                    const isHidden = detailsSection.classList.toggle('hidden');
                    const icon = toggleButton.querySelector('i');
                    
                    if (isHidden) {
                        toggleButton.innerHTML = 'Show More <i class="fas fa-chevron-down ml-1"></i>';
                    } else {
                        toggleButton.innerHTML = 'Show Less <i class="fas fa-chevron-up ml-1"></i>';
                    }
                });
                
                resultList.appendChild(card);
            });
        }
    });
    </script>
</body>
</html>
"""

class ColtWayfinderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
            return
        
        elif path == "/api/search":
            query_params = parse_qs(urlparse(self.path).query)
            query = query_params.get("q", [""])[0].lower()
            
            results = []
            for item in SAMPLE_DATA:
                score = 0
                
                if query in item["title"].lower():
                    score += 3
                
                if query in item["description"].lower():
                    score += 2
                
                if "categories" in item:
                    for category in item["categories"]:
                        if query in category.lower():
                            score += 1
                
                if "industries" in item:
                    for industry in item["industries"]:
                        if query in industry.lower():
                            score += 1
                
                if score > 0:
                    result = item.copy()
                    result["relevance_score"] = score
                    results.append(result)
            
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"results": results, "total": len(results)}).encode())
            return
        
        elif path == "/api/categories":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(CATEGORIES).encode())
            return
        
        elif path.startswith("/api/related/"):
            item_id = path.split("/")[-1]
            
            # Find related items
            results = []
            for item in SAMPLE_DATA:
                if item["type"] == "solution" and "relatedProducts" in item and item_id in item["relatedProducts"]:
                    results.append(item)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"results": results, "total": len(results)}).encode())
            return
        
        # Default 404 handler
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        if self.path == "/api/guided-search":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode())
            
            industry = params.get("industry", "").lower()
            problem_type = params.get("problemType", "").lower()
            
            results = []
            
            # Find solutions for the specified industry
            if industry:
                for item in SAMPLE_DATA:
                    if item["type"] == "solution" and "industries" in item:
                        for ind in item["industries"]:
                            if industry.lower() in ind.lower():
                                result = item.copy()
                                result["recommendationType"] = "Recommended Solution"
                                results.append(result)
                                break
            
            # Find products for the specified problem type
            if problem_type:
                for item in SAMPLE_DATA:
                    if item["type"] == "product" and "categories" in item:
                        for category in item["categories"]:
                            if problem_type.lower() in category.lower():
                                result = item.copy()
                                result["recommendationType"] = "Suggested Product"
                                results.append(result)
                                break
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"results": results, "total": len(results)}).encode())
            return
        
        # Default 404 handler for other POST requests
        self.send_response(404)
        self.end_headers()

def run_server(port=8000):
    """Run the Colt Wayfinder demo server."""
    handler = ColtWayfinderHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Colt Wayfinder demo running at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Open browser automatically
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()

if __name__ == "__main__":
    run_server()
