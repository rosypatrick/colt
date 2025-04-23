# Colt Wayfinder Tool - GitHub CodeSpaces Setup

This guide explains how to set up and run the Colt Wayfinder Tool in GitHub CodeSpaces, enabling cloud-based development without local installation.

## Opening in CodeSpaces

1. Navigate to the GitHub repository:
   ```
   https://github.com/your-username/colt-wayfinder
   ```

2. Click the green "Code" button, then select the "CodeSpaces" tab

3. Click "Create codespace on main" to launch a new CodeSpace

## Automatic Setup

The repository includes a devcontainer configuration that automatically:
- Installs Python 3.8+
- Installs Node.js 14+
- Sets up the virtual environment
- Installs required dependencies

Wait for the automatic setup to complete (this may take a few minutes).

## Manual Setup Steps

If any part of the automatic setup fails, you can run these commands in the terminal:

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Running the Application in CodeSpaces

1. Start the backend server:
   ```bash
   python app.py
   ```

2. The CodeSpaces interface will notify you that a service is running on port 8000. Click "Open in Browser" to view the application.

3. Alternatively, you can start the frontend development server separately:
   ```bash
   cd frontend
   npm start
   ```
   And open port 3000 when prompted.

## Data Collection (Optional)

To refresh the data from Colt's website:

```bash
python scraper.py
```

## Environment Variables

The CodeSpace is automatically configured with required environment variables. If needed, you can modify them:

1. Go to the repository settings
2. Navigate to Secrets > Codespaces
3. Add or update the necessary environment variables

## Development Workflow

1. Make your changes to the code
2. Test the changes in the CodeSpace environment
3. Commit and push your changes

## Port Forwarding

CodeSpaces automatically forwards these ports:
- 8000: Backend API
- 3000: Frontend development server

You can configure additional ports in the `.devcontainer/devcontainer.json` file.

## Extended User Input Forms

The Colt Wayfinder Tool in CodeSpaces includes the updated input forms with:

### Project Attributes
1. **Industry** (required)
   - Commercial Real Estate
   - Healthcare
   - Education
   - Industrial
   - Retail
   - Data Centers
   - Other (with text field)

2. **Size of Project** (optional)
   - Input field with unit selection (sq meters/sq feet)

3. **Application** (required)
   - Roof
   - Wall
   - Ceiling
   - Window/glazing system
   - Screens/partitions

4. **Glazing Type** (optional)
   - Single glazed
   - Double glazed
   - Triple glazed
   - Fire-rated
   - Acoustic
   - Solar control
   - Not applicable

5. **Usage Location** (required)
   - Interior
   - Exterior
   - Both

### Performance Attributes
1. **Cv Value** (optional)
   - Numeric input with tooltip: "Coefficient of flow - how much air moves through at given pressure"

2. **U-Value** (optional)
   - Numeric input with tooltip: "Thermal transmittance - heat transfer rate"

3. **Acoustics Value** (optional)
   - Numeric input with tooltip: "Sound reduction index in dB"

## Troubleshooting in CodeSpaces

If you encounter issues:

1. Try rebuilding the container:
   - Click on the green CodeSpaces button in the bottom left
   - Select "Rebuild Container"

2. Check the terminal for error messages

3. Verify that ports are being forwarded correctly:
   - View the "PORTS" tab in the bottom panel
   - Ensure ports 8000 and 3000 are listed and "public"

4. If database issues occur, reset the database:
   ```bash
   rm -f wayfinder.db
   python app.py --init-db
   ```

For additional assistance, file an issue on the GitHub repository.
