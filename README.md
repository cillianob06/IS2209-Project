# 🐶 Dog  Dashboard - IS2209 Group 43

- Cillian O'Brien - 124378506
- Jack Foley - 124376473 
- Ronan Birdthistle - 124477074
- Donagh Murphy - 124422534

A Flask-based web service that integrates The Dog API and a PostgreSQL
database to deliver a dog image explorer with breed filtering,
favourites, and usage statistics.

Live URL: https://is2209-project.onrender.com/  
Repository: https://github.com/cillianob06/IS2209-Project



## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database (e.g. Supabase)
- Dog API key (https://thedogapi.com)

### Local Development

1. Clone the repository:
'''bash
git clone https://github.com/cillianob06/IS2209-Project
cd IS2209-Project
'''

2. Create and activate a virtual environment:
'''bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
'''

3. Install dependencies:
'''bash
pip install -r requirements.txt
'''

4. Copy '.env.example' to '.env' and fill in your values:
'''bash
cp .env.example .env
'''

5. Set up the database:
'''bash
python run_schema.py
'''

6. Run the application:
'''bash
python app.py
'''

The app will be available at 'http://localhost:5000'.



## Environment Variables

| Variable | Description |
|----------|-------------|
| 'DOG_API_KEY' | API key from thedogapi.com |
| 'DATABASE_URL' | PostgreSQL connection string |
| 'PORT' | Port to run the app on (default: 5000) |

Secrets are stored as environment variables and never committed to the
repository. GitHub Actions secrets are used in the CI/CD pipeline.



## Endpoints

| Endpoint | Description |
|----------|-------------|
| '/' | Main dashboard UI |
| '/random-dog' | Fetch a random dog image with breed info |
| '/breeds' | List all available breeds |
| '/stats-page' | Stats UI page |
| '/favourites-page' | Favourites UI page |
| '/status' | Service status — DB and API connectivity, uptime |
| '/health' | Health check — returns ok or degraded |



## CI/CD Overview

The pipeline is located in '.github/workflows/ci.yml' and triggers on
every push to master and on every pull request.

### **Pipeline steps:**
1. Install dependencies from 'requirements.txt'
2. Lint with 'ruff'
3. Run tests with 'pytest' and generate a coverage report
4. Build Docker image
5. Publish image to GitHub Container Registry (GHCR)

Deployment: Render automatically deploys on every push to master.



###  **Docker**

Build and run locally:

bash
docker build -t dog-dashboard .
docker run -p 5000:5000 --env-file .env dog-dashboard


The image is published automatically to GHCR on every push to master.



## Observability

- Structured logging via Python's 'logging' module
- '/status' endpoint reports DB connectivity, API status, uptime,
  and environment
- '/health' endpoint returns 'ok' or 'degraded' based on DB
  connectivity
- All DB errors are logged with 'logger.error'

## Resilience

- All external calls are wrapped in try/except blocks
- API failures return meaningful JSON error responses with appropriate
  HTTP status codes
- DB failures are caught and logged without crashing the application



## Demo Steps

1. Visit https://is2209-project.onrender.com/
2. Click **Get Random Dog** to fetch a random dog
3. Use the breed dropdown and **Search** to filter by breed —
   displays breed name, temperament, and lifespan
4. Click **Favourite** to save a dog, then **View Favourites** to
   see and manage saved dogs
5. Click **Stats** to view total requests and the top breeds
   leaderboard
6. Visit /status to see live DB and API connectivity diagnostics
7. Visit /health for the health check endpoint

