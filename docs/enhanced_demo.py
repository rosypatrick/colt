"""
Colt Wayfinder Tool - Enhanced Standalone Demo (Simplified)

A simplified standalone demo showing the new project and performance attributes.
"""

import http.server
import socketserver
import json
import webbrowser
import threading
from urllib.parse import parse_qs, urlparse

# Sample data with enhanced attributes
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
        }
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
        }
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
        }
    }
]

# Categories including new attributes
CATEGORIES = {
    "industries": ["Commercial Real Estate", "Manufacturing", "Retail", "Warehousing"],
    "problemTypes": ["Smoke Control", "Climate Control", "Ventilation", "Energy Efficiency"],
    "buildingTypes": ["Office Building", "Factory", "Warehouse", "Shopping Center"],
    "projectSizes": ["Small (< 500 m²)", "Medium (500-2000 m²)", "Large (2000-10000 m²)", "Extra Large (> 10000 m²)"],
    "applications": ["Roof", "Wall", "Ceiling", "Window/Glazing System", "Screens/Partitions"],
    "glazingTypes": ["Single Glazed", "Double Glazed", "Triple Glazed", "Not Applicable"],
    "useTypes": ["Interior", "Exterior"],
    "cvValues": ["Low (< 0.4)", "Medium (0.4-0.6)", "High (> 0.6)", "Not Specified"],
    "uValues": ["Excellent (< 0.8 W/m²K)", "Good (0.8-1.2 W/m²K)", "Standard (1.2-2.0 W/m²K)", "Basic (> 2.0 W/m²K)"],
    "acousticsValues": ["Low (< 30 dB)", "Medium (30-40 dB)", "High (> 40 dB)", "Not Specified"]
}

class ColtWayfinderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("frontend/index.html", "rb") as f:
                self.wfile.write(f.read())
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
            
        elif path == "/api/search":
            query_params = parse_qs(urlparse(self.path).query)
            query = query_params.get("q", [""])[0].lower()
            
            results = []
            for item in SAMPLE_DATA:
                if query in item["title"].lower() or query in item["description"].lower():
                    results.append(item)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"results": results}).encode())
            return
            
        # Serve static files from frontend directory
        elif path.startswith("/frontend/"):
            try:
                with open(path[1:], "rb") as file:
                    self.send_response(200)
                    if path.endswith(".js"):
                        self.send_header("Content-type", "application/javascript")
                    elif path.endswith(".css"):
                        self.send_header("Content-type", "text/css")
                    else:
                        self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(file.read())
            except:
                self.send_response(404)
                self.end_headers()
            return
        
        # Default 404 handler
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        if self.path == "/api/guided-search":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode())
            
            # Filter products based on params
            results = []
            for product in SAMPLE_DATA:
                # Apply filters based on advanced parameters
                match = True
                
                # Project attributes filtering
                if params.get("projectSize") and product.get("projectAttributes", {}).get("Size") != params["projectSize"]:
                    match = False
                if params.get("application") and product.get("projectAttributes", {}).get("Application") != params["application"]:
                    match = False
                if params.get("glazing") and product.get("projectAttributes", {}).get("Glazing") != params["glazing"]:
                    match = False
                if params.get("useType") and product.get("projectAttributes", {}).get("UseType") != params["useType"]:
                    match = False
                
                # Performance attributes filtering
                if params.get("cvValue") and (not product.get("specifications", {}).get("Cv Value") or 
                                            params["cvValue"].split(" ")[0] not in product["specifications"]["Cv Value"]):
                    match = False
                if params.get("uValue") and (not product.get("specifications", {}).get("U-Value") or 
                                           params["uValue"].split(" ")[0] not in product["specifications"]["U-Value"]):
                    match = False
                if params.get("acousticsValue") and (not product.get("specifications", {}).get("Acoustics") or 
                                                  params["acousticsValue"].split(" ")[0] not in product["specifications"]["Acoustics"]):
                    match = False
                
                if match:
                    # Add applied filters for display
                    product_copy = product.copy()
                    product_copy["appliedFilters"] = []
                    
                    if params.get("projectSize") and product.get("projectAttributes", {}).get("Size") == params["projectSize"]:
                        product_copy["appliedFilters"].append(f"Size: {params['projectSize']}")
                    if params.get("application") and product.get("projectAttributes", {}).get("Application") == params["application"]:
                        product_copy["appliedFilters"].append(f"Application: {params['application']}")
                    if params.get("glazing") and product.get("projectAttributes", {}).get("Glazing") == params["glazing"]:
                        product_copy["appliedFilters"].append(f"Glazing: {params['glazing']}")
                    if params.get("useType") and product.get("projectAttributes", {}).get("UseType") == params["useType"]:
                        product_copy["appliedFilters"].append(f"Use: {params['useType']}")
                    if params.get("cvValue") and product.get("specifications", {}).get("Cv Value") and params["cvValue"].split(" ")[0] in product["specifications"]["Cv Value"]:
                        product_copy["appliedFilters"].append(f"Cv Value: {params['cvValue']}")
                    if params.get("uValue") and product.get("specifications", {}).get("U-Value") and params["uValue"].split(" ")[0] in product["specifications"]["U-Value"]:
                        product_copy["appliedFilters"].append(f"U-Value: {params['uValue']}")
                    if params.get("acousticsValue") and product.get("specifications", {}).get("Acoustics") and params["acousticsValue"].split(" ")[0] in product["specifications"]["Acoustics"]:
                        product_copy["appliedFilters"].append(f"Acoustics: {params['acousticsValue']}")
                    
                    product_copy["recommendationType"] = "Matched Product"
                    results.append(product_copy)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"results": results}).encode())
            return
        
        # Default 404 handler for other POST requests
        self.send_response(404)
        self.end_headers()

def create_index_html():
    """Create a simplified index.html file with the new attributes UI"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Colt Wayfinder Enhanced Demo</title>
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
        .attribute-pill {
            background-color: #e9f5ff; color: #0066cc; border-radius: 999px;
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
        </div>
    </header>

    <div class="colt-gradient text-white py-12 px-4">
        <div class="container mx-auto">
            <div class="max-w-3xl">
                <h1 class="text-4xl font-bold mb-4">Find the Perfect Colt Solution</h1>
                <p class="text-xl mb-6">Now with enhanced project and performance attributes!</p>
            </div>
        </div>
    </div>

    <main class="container mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row md:space-x-8">
            <div class="md:w-1/3" id="guided-search">
                <div class="bg-white rounded-lg shadow-lg p-6 my-6">
                    <h2 class="text-2xl font-bold text-gray-800 mb-4">Find the Right Solution</h2>
                    
                    <div class="mb-6">
                        <h3 class="text-lg font-semibold mb-3">Project Attributes</h3>
                        
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
                        
                        <h3 class="text-lg font-semibold mb-3 mt-6">Performance Attributes</h3>
                        
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
                        
                        <div class="mt-6">
                            <button id="search-btn" class="w-full colt-btn py-2 px-4 rounded-lg">
                                Find Solutions <i class="fas fa-search ml-2"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="md:w-2/3">
                <div id="results-container" class="my-6">
                    <div id="loading" class="hidden flex justify-center items-center py-12">
                        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                    
                    <div id="results">
                        <h2 class="text-2xl font-bold text-gray-800 mb-4">Products</h2>
                        <div id="result-list" class="grid grid-cols-1 gap-6"></div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        let selectedProjectSize = '';
        let selectedApplication = '';
        let selectedGlazing = '';
        let selectedUseType = '';
        let selectedCvValue = '';
        let selectedUValue = '';
        let selectedAcousticsValue = '';
        
        // Populate selects from API
        fetch('/api/categories')
            .then(response => response.json())
            .then(data => {
                // Populate all the dropdowns with the category data
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
        
        // Setup select event listeners
        document.getElementById('project-size').addEventListener('change', function() {
            selectedProjectSize = this.value;
        });
        
        document.getElementById('application').addEventListener('change', function() {
            selectedApplication = this.value;
        });
        
        document.getElementById('glazing').addEventListener('change', function() {
            selectedGlazing = this.value;
        });
        
        document.getElementById('use-type').addEventListener('change', function() {
            selectedUseType = this.value;
        });
        
        document.getElementById('cv-value').addEventListener('change', function() {
            selectedCvValue = this.value;
        });
        
        document.getElementById('u-value').addEventListener('change', function() {
            selectedUValue = this.value;
        });
        
        document.getElementById('acoustics-value').addEventListener('change', function() {
            selectedAcousticsValue = this.value;
        });
        
        // Load products on page load
        fetch('/api/products')
            .then(response => response.json())
            .then(products => {
                displayResults(products);
            });
        
        // Search button handler
        document.getElementById('search-btn').addEventListener('click', function() {
            document.getElementById('loading').classList.remove('hidden');
            
            const params = {
                projectSize: selectedProjectSize,
                application: selectedApplication,
                glazing: selectedGlazing,
                useType: selectedUseType,
                cvValue: selectedCvValue,
                uValue: selectedUValue,
                acousticsValue: selectedAcousticsValue
            };
            
            fetch('/api/guided-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').classList.add('hidden');
                    displayResults(data.results);
                });
        });
        
        // Display results function
        function displayResults(results) {
            const resultList = document.getElementById('result-list');
            resultList.innerHTML = '';
            
            results.forEach(item => {
                const card = document.createElement('div');
                card.className = 'bg-white rounded-lg shadow-lg overflow-hidden';
                
                let html = `
                    <div class="p-6">
                        ${item.recommendationType ? `<div class="mb-2"><span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">${item.recommendationType}</span></div>` : ''}
                        <h3 class="text-xl font-bold text-gray-800 mb-2">${item.title}</h3>
                        <p class="text-gray-600 mb-4">${item.description}</p>
                `;
                
                if (item.categories) {
                    html += '<div class="mb-4">';
                    item.categories.forEach(cat => {
                        html += `<span class="category-pill">${cat}</span>`;
                    });
                    html += '</div>';
                }
                
                if (item.appliedFilters && item.appliedFilters.length > 0) {
                    html += '<div class="mb-4"><h4 class="text-sm font-medium text-gray-500 mb-2">Matching Criteria:</h4><div>';
                    item.appliedFilters.forEach(filter => {
                        html += `<span class="attribute-pill">${filter}</span>`;
                    });
                    html += '</div></div>';
                }
                
                html += `
                        <div class="mt-4">
                            <button class="toggle-details w-full text-blue-500 hover:text-blue-700 font-medium flex items-center justify-center">
                                <span>Show Details</span> <i class="fas fa-chevron-down ml-1"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="details p-6 border-t border-gray-200 hidden">
                `;
                
                // Project Attributes
                if (item.projectAttributes) {
                    html += '<div class="mb-6"><h4 class="text-lg font-semibold mb-2">Project Attributes</h4>';
                    
                    for (const [key, value] of Object.entries(item.projectAttributes)) {
                        html += `
                            <div class="border-b border-gray-100 py-2">
                                <span class="text-gray-500">${key}:</span> <span class="font-medium">${value}</span>
                            </div>
                        `;
                    }
                    
                    html += '</div>';
                }
                
                // Specifications
                if (item.specifications) {
                    html += '<div class="mb-6"><h4 class="text-lg font-semibold mb-2">Specifications</h4>';
                    
                    for (const [key, value] of Object.entries(item.specifications)) {
                        html += `
                            <div class="border-b border-gray-100 py-2">
                                <span class="text-gray-500">${key}:</span> <span class="font-medium">${value}</span>
                            </div>
                        `;
                    }
                    
                    html += '</div>';
                }
                
                html += '</div>';
                
                card.innerHTML = html;
                
                // Setup toggle details
                const toggleBtn = card.querySelector('.toggle-details');
                const details = card.querySelector('.details');
                
                toggleBtn.addEventListener('click', () => {
                    const isHidden = details.classList.toggle('hidden');
                    toggleBtn.querySelector('span').textContent = isHidden ? 'Show Details' : 'Hide Details';
                    toggleBtn.querySelector('i').className = isHidden ? 'fas fa-chevron-down ml-1' : 'fas fa-chevron-up ml-1';
                });
                
                resultList.appendChild(card);
            });
        }
    });
    </script>
</body>
</html>"""
    
    import os
    os.makedirs("frontend", exist_ok=True)
    with open("frontend/index.html", "w", encoding="utf-8") as f:
        f.write(html)

def run_server(port=8000):
    """Run the Colt Wayfinder demo server."""
    create_index_html()
    
    with socketserver.TCPServer(("", port), ColtWayfinderHandler) as httpd:
        print(f"Colt Wayfinder Enhanced Demo running at http://localhost:{port}")
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
