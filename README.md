# Colt Wayfinder Tool

A demonstration of an intelligent wayfinder tool for Colt's smoke control, ventilation, and climate control products and solutions.

## Overview

The Colt Wayfinder Tool helps users easily navigate Colt's product offerings and find the perfect solutions for their specific building needs. Key features include:

- **Intelligent Search**: Find products, solutions, and technical documentation through a powerful search engine
- **Guided Journey**: Answer a few simple questions about your industry, problem, and building type to get tailored recommendations
- **Related Content**: Discover related products, solutions, and resources to make informed decisions
- **Technical Specifications**: Access detailed specifications for all products
- **Mobile-Friendly Interface**: Consistent experience across all devices

## Project Structure

```
colt-wayfinder/
├── app.py                 # FastAPI backend application
├── scraper.py             # Web scraper for collecting data from Colt's website
├── search_engine.py       # Vector search implementation for the wayfinder
├── scraped_data/          # Directory for storing scraped data
├── frontend/              # Frontend React application
│   ├── index.html         # Main HTML file
│   ├── app.js             # React application code
│   └── api-client.js      # JavaScript client for the API
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+ (optional, for development)
- Git

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/colt-wayfinder.git
   cd colt-wayfinder
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure the `frontend` directory exists:
   ```
   mkdir -p frontend
   ```

### Running the Demo

#### 1. Data Collection (Optional)

To scrape data from Colt's website (optional, as sample data is included):

```
python scraper.py
```

This will populate the `scraped_data` directory with product, solution, and technical documentation data.

#### 2. Start the API Server

```
python app.py
```

The API will be available at http://localhost:8000. It also serves the frontend static files.

#### 3. Access the Demo

Open your browser and navigate to:

```
http://localhost:8000
```

## API Routes

- `GET /search?q={query}&limit={limit}` - Search for content based on a text query
- `POST /guided-search` - Perform a guided search based on industry, problem type, and building type
- `GET /related/{item_id}?limit={limit}` - Get content related to a specific item
- `GET /categories` - Get all available categories for filtering

## Demo Scenarios

### Scenario 1: Building Manager Seeking Smoke Control Solutions
1. Use the guided search feature
2. Select "Commercial Real Estate" as the industry
3. Select "Smoke Control" as the problem type
4. Select "Office Building" as the building type
5. Explore the recommended solutions
6. Click "Show More" to see detailed specifications and related products

### Scenario 2: HVAC Contractor Looking for Technical Specifications
1. Use the search box at the top of the page
2. Search for "exhaust fan"
3. Click on the Industrial Exhaust Fan Series 500 result
4. Expand the details to view the technical specifications
5. Explore related products and solutions

### Scenario 3: Architect Researching Climate Control Options
1. Use the guided search feature
2. Select "Commercial Real Estate" as the industry
3. Select "Climate Control" as the problem type
4. Select "Shopping Center" as the building type
5. Explore the recommended solutions
6. Check out related technical documentation and case studies

## Future Enhancements

- **3D Visualization**: Add interactive 3D models of products and installations
- **AR Mode**: Use Augmented Reality to visualize products in real spaces
- **Saved Projects**: Allow users to save configurations and product selections
- **Integration with BIM**: Connect with Building Information Modeling software
- **Product Configurator**: Interactive tool to customize products for specific needs
- **Advanced Filtering**: More detailed filtering options for specific requirements
- **Multi-language Support**: Expand to support all languages Colt operates in

## License

This project is a demonstration and is not licensed for commercial use.
