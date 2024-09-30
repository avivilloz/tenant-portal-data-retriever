#!/usr/bin/env python3

import sys

"""
Tenant Portal Data Retriever

This script serves as the entry point for the tenant portal data retriever application.

Usage:
    ./tenant_portal_data_retriever.py <tenant_portal> <username> <password>
"""

from src.main import main
from src.logger import logger

if __name__ == "__main__":
    logger.info("Starting Tenant Portal Data Retriever")
    if len(sys.argv) != 4:
        logger.error(
            "Usage: python tenant_portal_data_retriever.py <tenant_portal> <username> <password>"
        )
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    logger.info("Tenant Portal Data Retriever finished")
