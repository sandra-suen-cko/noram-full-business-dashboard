"""Configuration for NORAM Business Dashboard - Source of Truth for Sheet Structure."""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets Configuration
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "1FCK4lgiQPuHvxc8KxIoxQsSucI-rPySVjovW2MXGjDA")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "secrets/credentials.json")
GOOGLE_TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH", "secrets/token.json")

# Cache Configuration
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "5"))

# Server Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# Sheet Structure - Source of Truth (hardcoded configuration per PRD)
# Any changes to Sheet tab names or structure requires code update + redeployment
SHEET_CONFIG = {
    "spreadsheet_id": SPREADSHEET_ID,
    "refresh_interval_minutes": CACHE_TTL_MINUTES,
    "domains": {
        "frontbook": {
            "tab_name": "Analytics Matrix - Frontbook",
            "range": "A1:Z100",  # Adjust based on your actual data range
            "header_row": 1,
            "date_column": "A",
            "metrics": [
                {
                    "name": "conversion_rate",
                    "display_name": "Conversion Rate",
                    "unit": "%",
                    "decimals": 2
                },
                {
                    "name": "aov",
                    "display_name": "Average Order Value",
                    "unit": "$",
                    "decimals": 2
                },
                {
                    "name": "sessions",
                    "display_name": "Sessions",
                    "unit": "",
                    "decimals": 0
                },
                {
                    "name": "orders",
                    "display_name": "Orders",
                    "unit": "",
                    "decimals": 0
                }
            ]
        },
        "backbook": {
            "tab_name": "Analytics Matrix - Backbook",
            "range": "A1:Z100",  # Adjust based on your actual data range
            "header_row": 1,
            "date_column": "A",
            "metrics": [
                {
                    "name": "churn_rate",
                    "display_name": "Churn Rate",
                    "unit": "%",
                    "decimals": 2
                },
                {
                    "name": "ltv",
                    "display_name": "Lifetime Value",
                    "unit": "$",
                    "decimals": 2
                },
                {
                    "name": "retention",
                    "display_name": "Retention Rate",
                    "unit": "%",
                    "decimals": 2
                }
            ]
        }
    }
}
