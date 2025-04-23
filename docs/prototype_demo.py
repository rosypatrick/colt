"""
Colt Wayfinder Tool - Simple Prototype Demo

A minimal prototype showing the enhanced project and performance attributes.
"""

import http.server
import socketserver
import json
import webbrowser
import threading
import os
from urllib.parse import parse_qs, urlparse

# Sample data with enhanced attributes
SAMPLE_DATA = [
    {
        "id": "p1",
        "title": "Industrial Exhaust Fan Series 500",
        "description": "Heavy-duty exhaust fans designed for smoke extraction in industrial environments.",
        "specifications": {
            "Cv Value": "0.65 (High)",
            "U-Value": "2.4 W/m²K (Basic)",
            "Acoustics": "32 dB (Medium)"
        },
        "projectAttributes": {
            "Application": "Roof",
            "Size": "Medium (500-2000 m²)",
            "Glazing": "Not Applicable",
            "UseType": "Exterior"
        }
    },
    {
        "id": "p2",
        "title": "EcoVent Air Handling Unit",
        "description": "Energy-efficient air handling units for commercial buildings.",
        "specifications": {
            "Cv Value": "0.55 (Medium)",
            "U-Value": "0.9 W/m²K (Good)",
            "Acoustics": "25 dB (Low)"
        },
        "projectAttributes": {
            "Application": "Wall",
            "Size": "Large (2000-10000 m²)",
            "Glazing": "Double Glazed",
            "UseType": "Interior"
        }
    },
    {
        "id": "p3",
        "title": "SkyLite Natural Ventilator",
        "description": "Roof-mounted natural ventilators for day-to-day ventilation and smoke control.",
        "specifications": {
            "Cv Value": "0.35 (Low)",
            "U-Value": "1.7 W/m²K (Standard)",
            "Acoustics": "45 dB (High)"
        },
        "projectAttributes": {
            "Application": "Window/Glazing System",
            "Size": "Small (< 500 m²)",
            "Glazing": "Single Glazed",
            "UseType": "Exterior"
        }
    }
]

# Categories for new attributes
CATEGORIES = {
    "projectSizes": ["Small (< 500 m²)", "Medium (500-2000 m²)", "Large (2000-10000 m²)", "Extra Large (> 10000 m²)"],
    "applications": ["Roof", "Wall", "Ceiling", "Window/Glazing System", "Screens/Partitions"],
    "glazingTypes": ["Single Glazed", "Double Glazed", "Triple Glazed", "Not Applicable"],
    "useTypes": ["Interior", "Exterior"],
    "cvValues": ["Low (< 0.4)", "Medium (0.4-0.6)", "High (> 0.6)", "Not Specified"],
    "uValues": ["Excellent (< 0.8 W/m²K)", "Good (0.8-1.2 W/m²K)", "Standard (1.2-2.0 W/m²K)", "Basic (> 2.0 W/m²K)"],
    "acousticsValues": ["Low (< 30 dB)", "Medium (30-40 dB)", "High (> 40 dB)", "Not Specified"]
}

# Simple HTML template for the prototype
HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Colt Wayfinder Prototype</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">
    <style>
        body { background-color: #f5f7fa; }
        .attribute-pill {
            background-color: #e9f5ff; color: #0066cc; border-radius: 999px;
            padding: 0.25rem 0.75rem; font-size: 0.75rem; margin-right: 0.5rem; margin-bottom: 0.5rem;
            display: inline-block;
        }
    </style>
</head>
<body>
    <header class="bg-blue-900 text-white shadow-md">
        <div class="container mx-auto px-4 py-4">
            <h1 class="text-2xl font-bold">Colt Wayfinder Prototype</h1>
            <p class="text-sm">Demonstrating new project and performance attributes</p>
        </div>
    </header>

    <main class="container mx-auto p-4">
        <div class="flex flex-col md:flex-row gap-6">
            <!-- Search Panel -->
            <div class="md:w-1/3">
                <div class="bg-white rounded-lg shadow p-4">
                    <h2 class="text-xl font-bold mb-4">Product Finder</h2>
                    
                    <div class="mb-6">
                        <h3 class="font-semibold mb-2 text-blue-800">Project Attributes</h3>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">Project Size</label>
                            <select id="project-size" class="w-full p-2 border rounded">
                                <option value="">Any size</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">Application</label>
                            <select id="application" class="w-full p-2 border rounded">
                                <option value="">Any application</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">Glazing</label>
                            <select id="glazing" class="w-full p-2 border rounded">
                                <option value="">Any glazing</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">Interior/Exterior</label>
                            <select id="use-type" class="w-full p-2 border rounded">
                                <option value="">Either</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="mb-6">
                        <h3 class="font-semibold mb-2 text-blue-800">Performance Attributes</h3>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">
                                Cv Value
                                <span class="text-xs text-gray-500">(air flow capacity)</span>
                            </label>
                            <select id="cv-value" class="w-full p-2 border rounded">
                                <option value="">Any Cv value</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">
                                U-Value
                                <span class="text-xs text-gray-500">(thermal transmittance)</span>
                            </label>
                            <select id="u-value" class="w-full p-2 border rounded">
                                <option value="">Any U-value</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="block text-sm font-medium mb-1">
                                Acoustics
                                <span class="text-xs text-gray-500">(sound reduction)</span>
                            </label>
                            <select id="acoustics-value" class="w-full p-2 border rounded">
                                <option value="">Any acoustics value</option>
                            </select>
                        </div>
                    </div>
                    
                    <button id="search-btn" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                        Find Products
                    </button>
                </div>
            </div>
            
            <!-- Results -->
            <div class="md:w-2/3">
                <h2 class="text-xl font-bold mb-4">Results</h2>
                <div id="loading" class="hidden text-center p-4">
                    <div class="inline-block animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
                    <p>Searching...</p>
                </div>
                <div id="results"></div>
            </div>
        </div>
    </main>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize filters
        let filters = {
            projectSize: '',
            application: '',
            glazing: '',
            useType: '',
            cvValue: '',
            uValue: '',
            acousticsValue: ''
        };
        
        // Populate select elements
        fetch('/api/categories')
            .then(response => response.json())
            .then(data => {
                populateSelect('project-size', data.projectSizes);
                populateSelect('application', data.applications);
                populateSelect('glazing', data.glazingTypes);
                populateSelect('use-type', data.useTypes);
                populateSelect('cv-value', data.cvValues);
                populateSelect('u-value', data.uValues);
                populateSelect('acoustics-value', data.acousticsValues);
            });
        
        function populateSelect(id, options) {
            const select = document.getElementById(id);
            options.forEach(option => {
                const el = document.createElement('option');
                el.value = option;
                el.textContent = option;
                select.appendChild(el);
            });
        }
        
        // Setup event listeners
        document.getElementById('project-size').addEventListener('change', function() {
            filters.projectSize = this.value;
        });
        
        document.getElementById('application').addEventListener('change', function() {
            filters.application = this.value;
        });
        
        document.getElementById('glazing').addEventListener('change', function() {
            filters.glazing = this.value;
        });
        
        document.getElementById('use-type').addEventListener('change', function() {
            filters.useType = this.value;
        });
        
        document.getElementById('cv-value').addEventListener('change', function() {
            filters.cvValue = this.value;
        });
        
        document.getElementById('u-value').addEventListener('change', function() {
            filters.uValue = this.value;
        });
        
        document.getElementById('acoustics-value').addEventListener('change', function() {
            filters.acousticsValue = this.value;
        });
        
        // Load initial products
        fetch('/api/products')
            .then(response => response.json())
            .then(displayResults);
        
        // Search button
        document.getElementById('search-btn').addEventListener('click', function() {
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('results').innerHTML = '';
            
            fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(filters)
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').classList.add('hidden');
                    displayResults(data);
                });
        });
        
        // Display results
        function displayResults(products) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            
            if (products.length === 0) {
                resultsDiv.innerHTML = '<div class="bg-white p-4 rounded shadow text-center">No products match your criteria</div>';
                return;
            }
            
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'bg-white rounded-lg shadow mb-4 overflow-hidden';
                
                let matchedCriteria = [];
                if (filters.projectSize && product.projectAttributes.Size === filters.projectSize) 
                    matchedCriteria.push(`Size: ${filters.projectSize}`);
                if (filters.application && product.projectAttributes.Application === filters.application)
                    matchedCriteria.push(`Application: ${filters.application}`);
                if (filters.glazing && product.projectAttributes.Glazing === filters.glazing)
                    matchedCriteria.push(`Glazing: ${filters.glazing}`);
                if (filters.useType && product.projectAttributes.UseType === filters.useType)
                    matchedCriteria.push(`Use: ${filters.useType}`);
                
                if (filters.cvValue && product.specifications['Cv Value'] && product.specifications['Cv Value'].includes(filters.cvValue.split(' ')[0]))
                    matchedCriteria.push(`Cv Value: ${filters.cvValue}`);
                if (filters.uValue && product.specifications['U-Value'] && product.specifications['U-Value'].includes(filters.uValue.split(' ')[0]))
                    matchedCriteria.push(`U-Value: ${filters.uValue}`);
                if (filters.acousticsValue && product.specifications['Acoustics'] && product.specifications['Acoustics'].includes(filters.acousticsValue.split(' ')[0]))
                    matchedCriteria.push(`Acoustics: ${filters.acousticsValue}`);
                
                let html = `
                    <div class="border-b p-4">
                        <h3 class="text-lg font-bold">${product.title}</h3>
                        <p class="text-gray-600 text-sm">${product.description}</p>
                `;
                
                if (matchedCriteria.length > 0) {
                    html += '<div class="mt-2"><h4 class="text-sm font-medium text-gray-500">Matching Criteria:</h4><div>';
                    matchedCriteria.forEach(criteria => {
                        html += `<span class="attribute-pill">${criteria}</span>`;
                    });
                    html += '</div></div>';
                }
                
                html += `
                        <button class="toggle-details mt-2 text-blue-600 hover:text-blue-800 text-sm">
                            Show Details
                        </button>
                    </div>
                    <div class="details p-4 hidden">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <h4 class="font-bold text-blue-800 mb-2">Project Attributes</h4>
                                <table class="w-full text-sm">
                `;
                
                Object.entries(product.projectAttributes).forEach(([key, value]) => {
                    html += `
                        <tr>
                            <td class="py-1 text-gray-600">${key}:</td>
                            <td class="py-1 font-medium">${value}</td>
                        </tr>
                    `;
                });
                
                html += `
                                </table>
                            </div>
                            <div>
                                <h4 class="font-bold text-blue-800 mb-2">Performance</h4>
                                <table class="w-full text-sm">
                `;
                
                Object.entries(product.specifications).forEach(([key, value]) => {
                    html += `
                        <tr>
                            <td class="py-1 text-gray-600">${key}:</td>
                            <td class="py-1 font-medium">${value}</td>
                        </tr>
                    `;
                });
                
                html += `
                                </table>
                            </div>
                        </div>
                    </div>
                `;
                
                card.innerHTML = html;
                
                // Toggle details
                const toggleBtn = card.querySelector('.toggle-details');
                const details = card.querySelector('.details');
                
                toggleBtn.addEventListener('click', function() {
                    const isHidden = details.classList.toggle('hidden');
                    this.textContent = isHidden ? 'Show Details' : 'Hide Details';
                });
                
                resultsDiv.appendChild(card);
            });
        }
    });
    </script>
</body>
</html>"""

class ColtWayfinderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
            return
        
        elif path == "/api/categories":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(CATEGORIES).encode())
            return
        
        elif path == "/api/products":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(SAMPLE_DATA).encode())
            return
        
        # Default 404 handler
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        if self.path == "/api/search":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            filters = json.loads(post_data.decode())
            
            # Filter products based on the criteria
            results = []
            for product in SAMPLE_DATA:
                match = True
                
                # Project attributes
                if filters.get("projectSize") and product["projectAttributes"]["Size"] != filters["projectSize"]:
                    match = False
                if filters.get("application") and product["projectAttributes"]["Application"] != filters["application"]:
                    match = False
                if filters.get("glazing") and product["projectAttributes"]["Glazing"] != filters["glazing"]:
                    match = False
                if filters.get("useType") and product["projectAttributes"]["UseType"] != filters["useType"]:
                    match = False
                
                # Performance attributes - check if string contains value (partial match)
                if filters.get("cvValue") and (not filters["cvValue"].split(" ")[0] in product["specifications"]["Cv Value"]):
                    match = False
                if filters.get("uValue") and (not filters["uValue"].split(" ")[0] in product["specifications"]["U-Value"]):
                    match = False
                if filters.get("acousticsValue") and (not filters["acousticsValue"].split(" ")[0] in product["specifications"]["Acoustics"]):
                    match = False
                
                if match:
                    results.append(product)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
            return
        
        # Default 404 handler
        self.send_response(404)
        self.end_headers()

def run_server(port=8000):
    """Run the prototype demo server."""
    with socketserver.TCPServer(("", port), ColtWayfinderHandler) as httpd:
        print(f"Colt Wayfinder Prototype Demo running at http://localhost:{port}")
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
