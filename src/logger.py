import logging
import os
from .config import LOGS_DIR, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=os.path.join(LOGS_DIR, "tenant_portal_retriever.log"),
)

logger = logging.getLogger("tenant_portal_retriever")
