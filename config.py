import os

REPORTS_FOLDER = os.getenv("REPORTS_FOLDER", "reports")
API_URL = os.getenv("API_URL", "")  # if you still want GitHub API listing
ML_AVAILABLE = True  # toggled in ml_models if import fails
