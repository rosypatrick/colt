# Colt Wayfinder Tool - Render Deployment Guide

This guide walks through deploying the Colt Wayfinder Tool to Render.com for production use.

## Prerequisites

- A Render.com account
- Access to the Colt Wayfinder GitHub repository
- Database credentials (if using a managed database)

## Deployment Steps

### 1. Create a Web Service for the Backend

1. Log in to your Render account and go to the Dashboard
2. Click "New" and select "Web Service"
3. Connect your GitHub repository or paste the repository URL
4. Configure the service:
   - **Name**: `colt-wayfinder-api` (or your preferred name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`
   - **Environment**: Select "Python 3"
   - **Region**: Choose the region closest to your users
   - **Branch**: `main` (or your production branch)
   - **Plan**: Select appropriate plan (starts at $7/month)

5. Add the following environment variables:
   ```
   DATABASE_URL=[Your PostgreSQL connection string]
   RENDER_EXTERNAL_URL=${RENDER_EXTERNAL_URL}
   PRODUCTION=true
   ```

6. Click "Create Web Service"

### 2. Create a PostgreSQL Database (Optional)

If you need a managed database:

1. In your Render dashboard, click "New" and select "PostgreSQL"
2. Configure the database:
   - **Name**: `colt-wayfinder-db`
   - **PostgreSQL Version**: 14
   - **Region**: Same as your web service
   - **Plan**: Select appropriate plan

3. After creation, copy the "Internal Database URL" to use in your web service

4. Go back to your web service settings and update the `DATABASE_URL` environment variable with this URL

### 3. Deploy Static Frontend (Optional)

If your frontend is separate from the backend:

1. Click "New" and select "Static Site"
2. Connect your GitHub repository
3. Configure the static site:
   - **Name**: `colt-wayfinder-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **Branch**: `main` (or your production branch)

4. Add environment variables:
   ```
   REACT_APP_API_URL=https://[your-backend-url].onrender.com
   ```

5. Click "Create Static Site"

### 4. Initialize the Database (First Deployment Only)

After the first deployment:

1. Go to your web service in the Render dashboard
2. Click on "Shell" in the top navigation
3. Run the database initialization command:
   ```bash
   python -c "from app import init_db; init_db()"
   ```

4. Run the initial data scraping:
   ```bash
   python scraper.py
   ```

### 5. Configure Custom Domain (Optional)

1. Go to your web service or static site in the Render dashboard
2. Click on "Settings" and then "Custom Domain"
3. Add your domain and follow the verification steps

## Monitoring and Management

### Logs and Monitoring

- **View Logs**: Access logs from the "Logs" tab in your service dashboard
- **Metrics**: Basic metrics are available in the "Metrics" tab
- **Alerts**: Set up alerts in the "Alerts" tab for important events

### Scaling

1. To scale your application:
   - Go to your web service in the Render dashboard
   - Click "Settings" and then "Scaling"
   - Adjust the number of instances or upgrade your plan

### CI/CD Pipeline

Render automatically deploys when you push to the connected repository branch. You can:

1. Configure auto-deployment settings in "Settings" > "Deploy Hooks"
2. Set up preview environments for pull requests

## User Journey Implementation

The Render deployment includes all the updated form inputs with required and optional fields:

### Project Attributes Form

```html
<form class="project-attributes">
  <div class="form-group">
    <label for="industry">Industry <span class="required">*</span></label>
    <select id="industry" name="industry" required>
      <option value="">Select an industry</option>
      <option value="commercial">Commercial Real Estate</option>
      <option value="healthcare">Healthcare</option>
      <option value="education">Education</option>
      <option value="industrial">Industrial</option>
      <option value="retail">Retail</option>
      <option value="data-centers">Data Centers</option>
      <option value="other">Other</option>
    </select>
    <div id="other-industry-container" style="display:none">
      <input type="text" id="other-industry" name="other-industry" placeholder="Please specify">
    </div>
  </div>
  
  <div class="form-group">
    <label for="project-size">Size of Project</label>
    <div class="input-group">
      <input type="number" id="project-size" name="project-size" min="0" step="0.01">
      <select id="size-unit" name="size-unit">
        <option value="sqm">sq meters</option>
        <option value="sqft">sq feet</option>
      </select>
    </div>
    <small class="form-text">Optional</small>
  </div>
  
  <div class="form-group">
    <label for="application">Application <span class="required">*</span></label>
    <select id="application" name="application" required>
      <option value="">Select an application</option>
      <option value="roof">Roof</option>
      <option value="wall">Wall</option>
      <option value="ceiling">Ceiling</option>
      <option value="window">Window/glazing system</option>
      <option value="screen">Screens/partitions</option>
    </select>
  </div>
  
  <div class="form-group">
    <label for="glazing">Glazing Type</label>
    <select id="glazing" name="glazing">
      <option value="">Select a glazing type</option>
      <option value="single">Single glazed</option>
      <option value="double">Double glazed</option>
      <option value="triple">Triple glazed</option>
      <option value="fire">Fire-rated</option>
      <option value="acoustic">Acoustic</option>
      <option value="solar">Solar control</option>
      <option value="na">Not applicable</option>
    </select>
    <small class="form-text">Optional</small>
  </div>
  
  <div class="form-group">
    <label for="location">Usage Location <span class="required">*</span></label>
    <select id="location" name="location" required>
      <option value="">Select location</option>
      <option value="interior">Interior</option>
      <option value="exterior">Exterior</option>
      <option value="both">Both</option>
    </select>
  </div>
</form>
```

### Performance Attributes Form

```html
<form class="performance-attributes">
  <div class="form-group">
    <label for="cv-value">Cv Value</label>
    <div class="input-with-tooltip">
      <input type="number" id="cv-value" name="cv-value" min="0" step="0.01">
      <div class="tooltip">
        <i class="info-icon">i</i>
        <span class="tooltip-text">Coefficient of flow - how much air can flow through at a given pressure drop</span>
      </div>
    </div>
    <small class="form-text">Optional</small>
  </div>
  
  <div class="form-group">
    <label for="u-value">U-Value</label>
    <div class="input-with-tooltip">
      <input type="number" id="u-value" name="u-value" min="0" step="0.01">
      <div class="tooltip">
        <i class="info-icon">i</i>
        <span class="tooltip-text">Thermal transmittance - measure of heat transfer rate</span>
      </div>
    </div>
    <small class="form-text">Optional</small>
  </div>
  
  <div class="form-group">
    <label for="acoustics-value">Acoustics Value</label>
    <div class="input-with-tooltip">
      <input type="number" id="acoustics-value" name="acoustics-value" min="0" step="0.1">
      <div class="tooltip">
        <i class="info-icon">i</i>
        <span class="tooltip-text">Sound reduction index in dB</span>
      </div>
    </div>
    <small class="form-text">Optional</small>
  </div>
  
  <button type="submit" class="search-button">Find Solutions</button>
</form>
```

## Troubleshooting Common Issues

### Database Connection Issues

If you encounter database connection problems:

1. Verify your `DATABASE_URL` environment variable
2. Check if the database is running (in Render dashboard)
3. Try reconnecting by restarting your web service

### Static Assets Not Loading

If static assets aren't loading:

1. Check if your frontend build command is correct
2. Verify that asset paths are properly configured
3. Clear browser cache and reload

### Deployment Failures

If deployments fail:

1. Check the build logs for errors
2. Verify that all dependencies are correctly specified
3. Try a manual deployment from the dashboard

## Support and Resources

- **Render Documentation**: [https://render.com/docs](https://render.com/docs)
- **Support**: For Render-specific issues, contact Render support
- **Project Issues**: Report application-specific issues on the GitHub repository
