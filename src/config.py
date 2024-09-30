import os
import logging

CLICKPAY_BASE_URL = "https://www.clickpay.com"
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db")
DATABASE_PATH = os.path.join(DB_DIR, "tenant_data.db")
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = logging.INFO

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
