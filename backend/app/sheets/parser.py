"""Parse and validate data from Google Sheets."""
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

# Formula error patterns that indicate invalid data
ERROR_PATTERNS = ["#VALUE!", "#DIV/0!", "#N/A", "#NAME?", "#REF!", "#ERROR!"]


def is_error_cell(value: Any) -> bool:
    """Check if a cell value is a formula error."""
    if not isinstance(value, str):
        return False
    return any(pattern in value for pattern in ERROR_PATTERNS)


def parse_analytics_data(
    raw_data: List[List[Any]],
    domain: str,
    expected_columns: List[str] = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Parse raw 2D array from Sheets into structured format with error detection.

    Args:
        raw_data: 2D array from Sheets API
        domain: Domain name (frontbook/backbook) for logging
        expected_columns: Expected column names (optional validation)

    Returns:
        Tuple of (parsed_data, errors)
        - parsed_data: List of dicts with column headers as keys
        - errors: List of error dicts with row, column, and error message
    """
    parsed_data = []
    errors = []

    if not raw_data or len(raw_data) < 1:
        logger.warning(f"No data received for {domain}")
        return [], []

    headers = raw_data[0]

    # Validate headers
    if expected_columns:
        missing = set(expected_columns) - set(headers)
        if missing:
            logger.warning(f"Missing columns in {domain}: {missing}")
            errors.append({
                "row": 1,
                "column": "headers",
                "error": f"Missing expected columns: {missing}"
            })

    # Parse data rows
    for row_idx, row in enumerate(raw_data[1:], start=2):
        row_data = {}
        row_errors = []

        for col_idx, (header, value) in enumerate(zip(headers, row)):
            row_data[header] = value

            # Check for formula errors
            if is_error_cell(value):
                row_errors.append({
                    "row": row_idx,
                    "column": header,
                    "error": str(value)
                })

        if row_errors:
            errors.extend(row_errors)

        parsed_data.append(row_data)

    if errors:
        logger.warning(f"Found {len(errors)} formula errors in {domain}: {errors[:3]}")

    return parsed_data, errors
