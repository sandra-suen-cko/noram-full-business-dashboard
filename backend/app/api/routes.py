"""REST API routes for NORAM Business Dashboard."""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.api.models import AnalyticsResponse, MetadataResponse, HealthResponse, ErrorDetail
from app.sheets.client import SheetsClient
from app.sheets.parser import parse_analytics_data
from app.cache.memory_cache import MemoryCache
from app.config import SHEET_CONFIG
from app.errors.handlers import handle_sheets_error, handle_generic_error

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")

# Initialize services
sheets_client = SheetsClient()
cache = MemoryCache(ttl_minutes=SHEET_CONFIG["refresh_interval_minutes"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="NORAM Business Dashboard backend is running"
    )


@router.get("/analytics/frontbook", response_model=AnalyticsResponse)
async def get_frontbook_analytics():
    """Fetch Frontbook analytics data."""
    return await get_domain_analytics("frontbook")


@router.get("/analytics/backbook", response_model=AnalyticsResponse)
async def get_backbook_analytics():
    """Fetch Backbook analytics data."""
    return await get_domain_analytics("backbook")


async def get_domain_analytics(domain: str) -> AnalyticsResponse:
    """Fetch analytics data for a specific domain."""
    cache_key = f"analytics_{domain}"

    # Check cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        domain_config = SHEET_CONFIG["domains"].get(domain)
        if not domain_config:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown domain: {domain}"
            )

        # Fetch from Sheets
        raw_data = sheets_client.fetch_range(
            domain_config["tab_name"],
            domain_config["range"]
        )

        if not raw_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for {domain}"
            )

        # Parse data
        parsed_data, errors = parse_analytics_data(raw_data, domain)

        # Extract columns from headers
        columns = raw_data[0] if raw_data else []

        # Build response
        response = AnalyticsResponse(
            domain=domain,
            data=parsed_data,
            errors=[ErrorDetail(**err) for err in errors],
            columns=columns,
            last_updated=datetime.utcnow().isoformat()
        )

        # Cache the response
        cache.set(cache_key, response)

        return response

    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error fetching {domain} analytics: {error}", exc_info=True)
        raise handle_generic_error(error)


@router.get("/analytics/metadata", response_model=MetadataResponse)
async def get_metadata():
    """Get metadata about available metrics and columns."""
    try:
        domains_config = SHEET_CONFIG["domains"]

        frontbook_metrics = [
            {
                "name": m["name"],
                "display_name": m["display_name"],
                "unit": m["unit"],
                "decimals": m["decimals"]
            }
            for m in domains_config["frontbook"]["metrics"]
        ]

        backbook_metrics = [
            {
                "name": m["name"],
                "display_name": m["display_name"],
                "unit": m["unit"],
                "decimals": m["decimals"]
            }
            for m in domains_config["backbook"]["metrics"]
        ]

        return MetadataResponse(
            frontbook={
                "metrics": frontbook_metrics,
                "columns": [m["name"] for m in frontbook_metrics]
            },
            backbook={
                "metrics": backbook_metrics,
                "columns": [m["name"] for m in backbook_metrics]
            }
        )

    except Exception as error:
        logger.error(f"Error fetching metadata: {error}", exc_info=True)
        raise handle_generic_error(error)


@router.post("/cache/clear")
async def clear_cache():
    """Clear the analytics cache (for testing/debugging)."""
    cache.clear()
    return {"status": "success", "message": "Cache cleared"}


@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    return cache.get_stats()
