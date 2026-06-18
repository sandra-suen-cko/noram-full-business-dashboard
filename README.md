# NORAM Business Dashboard (Project Arrakis)

High-availability, read-only visualization of NORAM sales performance from Google Sheets.

## Architecture

- **Backend:** FastAPI (Python) - Stateless proxy to Google Sheets with OAuth authentication
- **Frontend:** React + TypeScript + Vite - Interactive dashboard with Recharts visualization
- **Data Source:** Pre-calculated "Analytics Matrix" tabs in a single Google Sheet
- **State Management:** React Query (server state) + Zustand (local state)

## Quick Start

### Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

### With Docker Compose

```bash
docker-compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

## Configuration

- **Spreadsheet ID:** `1FCK4lgiQPuHvxc8KxIoxQsSucI-rPySVjovW2MXGjDA`
- **OAuth Credentials:** `backend/secrets/credentials.json` (first-time setup will prompt for auth)
- **Sheet Structure:** Defined in `backend/app/config.py` (source of truth)

## Implementation Phases

### Phase 1: ✅ Setup & Project Structure
- Directory scaffolding
- FastAPI & React initialization
- OAuth configuration
- Docker setup

### Phase 2: 🔄 Backend - Google Sheets Integration
- Complete Sheets client implementation
- Data parsing & error detection
- REST endpoints
- Caching & error handling

### Phase 3: ⏳ Frontend - UI & Visualization
- React components (Dashboard, Charts, Filters)
- Data fetching & caching
- Interactive filtering (isolated per domain)
- Error boundaries & loading states

### Phase 4: ⏳ Integration & Polish
- End-to-end testing
- Performance verification (< 2s load time)
- Documentation & deployment

## Key Features (MVP)

- ✅ OAuth Desktop Flow authentication
- ✅ Read from pre-calculated "Analytics Matrix" tabs
- ✅ Formula error detection (#VALUE!, #DIV/0!)
- ✅ In-memory caching (5-10 minutes)
- ✅ Graceful error handling & offline fallback
- ✅ Component-isolated filtering (Frontbook/Backbook)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/analytics/frontbook` | Frontbook analytics data |
| GET | `/api/analytics/backbook` | Backbook analytics data |
| GET | `/api/analytics/metadata` | Available metrics & columns |
| POST | `/api/cache/clear` | Clear cache |
| GET | `/api/cache/stats` | Cache statistics |

See `http://localhost:8000/docs` for interactive API documentation.

## Security & Maintenance

- **Access Control:** Service Account/OAuth auth. Cloudflare controls user access.
- **Configuration:** Sheet structure is hardcoded in `config.py`. Changes require redeployment.
- **Credentials:** Never committed to repository (.gitignore enforced)
- **Read-Only:** No write operations—visualization only

## Testing

```bash
# Backend
cd backend
pytest -v --cov=app

# Frontend
cd frontend
npm run test
```

## Documentation

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Implementation Plan](./IMPLEMENTATION_PLAN.md)

## Troubleshooting

**OAuth: "Redirect URI mismatch"**
- Ensure `http://localhost` is added as a redirect URI in Google Cloud Console

**Backend: "Module not found"**
- Activate Python venv: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**Frontend: API 404**
- Check backend is running on port 8000
- Verify `ALLOWED_ORIGINS` includes frontend URL in `.env`

## Next Steps

1. Update `config.py` with your actual Google Sheet tab names and data ranges
2. Test OAuth authentication (first run will prompt browser)
3. Verify data is fetched correctly from Sheets
4. Proceed with Phase 2: Frontend development