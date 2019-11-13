from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import os

# GOOGLE_APPLICATION_CREDENTIALS - /path/to/serviceaccountcreds.json
creds = service_account.IDTokenCredentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"], target_audience=os.environ["TARGET_AUDIENCE"]
)
authed_session = AuthorizedSession(creds)
response = authed_session.get(
    "https://art-test-two-dot-revolut-ds.appspot.com/add_task_app_engine"
)
print(response.status_code, response.content)
