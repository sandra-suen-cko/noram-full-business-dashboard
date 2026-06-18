# NORAM Business Dashboard - Backend

FastAPI backend serving as a stateless proxy to Google Sheets.

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

### 3. Google Sheets OAuth Setup

The first time you run the backend, it will open a browser window for OAuth authentication:

```bash
python -m uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for API documentation.

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/analytics/frontbook` - Fetch Frontbook analytics
- `GET /api/analytics/backbook` - Fetch Backbook analytics
- `GET /api/analytics/metadata` - Get available metrics metadata
- `POST /api/cache/clear` - Clear the cache
- `GET /api/cache/stats` - Get cache statistics

## Configuration

Sheet structure is defined in `app/config.py`. Update the `SHEET_CONFIG` dictionary to match your Google Sheet:
- Tab names
- Data ranges
- Metric definitions

## Running Tests

```bash
pytest -v --cov=app tests/
```

## Docker

```bash
docker build -t noram-backend .
docker run -p 8000:8000 noram-backend
```
