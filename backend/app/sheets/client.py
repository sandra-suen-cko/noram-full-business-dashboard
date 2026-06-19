"""Google Sheets API client wrapper."""
import logging
from typing import List, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.sheets.oauth import get_credentials
from app.config import SPREADSHEET_ID

logger = logging.getLogger(__name__)


class SheetsClient:
    """Wrapper for Google Sheets API interactions."""

    def __init__(self):
        self.creds = get_credentials()
        self.service = build("sheets", "v4", credentials=self.creds)
        self.spreadsheet_id = SPREADSHEET_ID

    def fetch_range(self, tab_name: str, range_notation: str) -> List[List[Any]]:
        """Fetch data from a specific tab and range.

        Args:
            tab_name: Name of the sheet tab (e.g., "Analytics Matrix - Frontbook")
            range_notation: Range in A1 notation (e.g., "A1:Z100")

        Returns:
            2D array of cell values

        Raises:
            HttpError: If API call fails
        """
        try:
            range_with_sheet = f"'{tab_name}'!{range_notation}"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_with_sheet
            ).execute()

            values = result.get("values", [])
            logger.info(f"Fetched {len(values)} rows from '{tab_name}'")
            return values

        except HttpError as error:
            logger.error(f"API error fetching from '{tab_name}': {error}")
            raise

    def get_sheet_metadata(self) -> dict:
        """Get metadata about the spreadsheet (sheet names, properties)."""
        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            return result
        except HttpError as error:
            logger.error(f"API error fetching metadata: {error}")
            raise
