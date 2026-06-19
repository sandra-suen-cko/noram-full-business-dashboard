"""OAuth Desktop Flow authentication for Google Sheets API."""
import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_credentials():
    """Get valid credentials for Google Sheets API using OAuth Desktop Flow.

    On first run, opens browser for user authentication or prompts manual auth.
    Saves token.json for future runs.
    """
    creds = None

    # Load existing token if available
    if os.path.exists(os.getenv("GOOGLE_TOKEN_PATH", "secrets/token.json")):
        from google.oauth2.credentials import Credentials
        token_path = os.getenv("GOOGLE_TOKEN_PATH", "secrets/token.json")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GOOGLE_CREDENTIALS_PATH", "secrets/credentials.json"),
                SCOPES
            )

            # Try to open browser, fall back to manual auth if not available
            try:
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logger.warning(f"Could not open browser automatically: {e}")
                logger.info("Starting manual OAuth flow...")
                creds = flow.run_local_server(port=8080, open_browser=False)
                logger.info("Please visit http://localhost:8080 to authenticate")

        # Save token for future runs
        token_path = os.getenv("GOOGLE_TOKEN_PATH", "secrets/token.json")
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds
