# Colt Wayfinder Tool - Local Development Setup

This guide will help you set up the Colt Wayfinder Tool for local development.

## Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend development)
- Git

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/colt-wayfinder.git
   cd colt-wayfinder
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the frontend:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Running the Application Locally

1. Start the backend API server:
   ```bash
   python app.py
   ```

2. In a new terminal, start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Access the application in your browser at:
   ```
   http://localhost:3000
   ```

## Data Collection (Optional)

If you need to refresh the data from Colt's website:

```bash
python scraper.py
```

This will update the `scraped_data` directory with the latest product, solution, and technical documentation.

## Testing

Run the automated tests with:

```bash
pytest
```

## Project Structure

```
colt-wayfinder/
├── app.py                 # FastAPI backend application
├── scraper.py             # Web scraper for collecting data from Colt's website
├── search_engine.py       # Vector search implementation for the wayfinder
├── scraped_data/          # Directory for storing scraped data
├── frontend/              # Frontend React application
│   ├── public/            # Static assets
│   ├── src/               # React source code
│   │   ├── components/    # UI components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── contexts/      # React contexts
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── App.js         # Main React component
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── README.md              # Main documentation
```

## Custom User Journey Implementation

The form inputs have been updated to include these customer requirements:

### Project Attributes
1. **Industry** (required): Selection from predefined industry categories
2. **Size of Project** (optional): Input in square meters/feet
3. **Application** (required): Select from:
   - Roof
   - Wall
   - Ceiling
   - Window/glazing system
   - Screens/partitions
4. **Glazing Type** (optional): Selection field for glazing options
5. **Usage Location** (required): Interior or Exterior

### Performance Attributes
1. **Cv Value** (optional): Numeric input with explanation tooltip
2. **U-Value** (optional): Numeric input with explanation tooltip
3. **Acoustics Value** (optional): Numeric input with explanation tooltip

## Local Environment Configuration

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=sqlite:///./wayfinder.db
SCRAPER_TIMEOUT=60
API_KEY=your_development_api_key
```

## Troubleshooting

If you encounter any issues during local setup, check the following:

1. Ensure all dependencies are correctly installed
2. Verify that ports 8000 and 3000 are not in use by other applications
3. Check that the virtual environment is activated
4. Look for error messages in the terminal running the backend and frontend

For additional help, check the issues section on the GitHub repository or contact the development team.
