"""Error handling and custom exceptions."""
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class SheetsError(Exception):
    """Base exception for Sheets-related errors."""
    pass


class SheetNotFoundError(SheetsError):
    """Sheet tab not found."""
    pass


class InvalidDataError(SheetsError):
    """Data validation failed."""
    pass


def handle_sheets_error(error: SheetsError) -> HTTPException:
    """Convert SheetsError to HTTPException."""
    logger.error(f"Sheets error: {error}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(error)
    )


def handle_generic_error(error: Exception) -> HTTPException:
    """Convert generic exception to HTTPException."""
    logger.error(f"Unexpected error: {error}", exc_info=True)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred. Please try again later."
    )
