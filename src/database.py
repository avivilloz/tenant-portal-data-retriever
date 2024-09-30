import sqlite3
from .queries import CREATE_TENANTS_TABLE, INSERT_TENANT, SELECT_ALL_TENANTS
from .logger import logger
from .config import DATABASE_PATH


class Database:
    """
    Handles database operations for tenant data."""

    def __init__(self):
        """Initialize Database and create tenants table if not exists."""
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.create_table()

    def create_table(self):
        """Create the tenants table if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute(CREATE_TENANTS_TABLE)
        self.conn.commit()

    def insert_tenant(self, tenant_data):
        """
        Insert tenant data into the database.

        :param tenant_data: Dictionary with tenant information
        """
        cursor = self.conn.cursor()
        cursor.execute(
            INSERT_TENANT,
            (
                tenant_data["email"],
                tenant_data["phone"],
            ),
        )
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def get_all_tenants(self):
        """Retrieve all tenants from the database."""
        cursor = self.conn.cursor()
        cursor.execute(SELECT_ALL_TENANTS)
        return cursor.fetchall()

    def print_all_tenants(self):
        """Print all tenants in the database."""
        tenants = self.get_all_tenants()
        if not tenants:
            logger.info("No tenants found in the database.")
        else:
            logger.info("Tenants in the database:")
            for tenant in tenants:
                logger.info(f"ID: {tenant[0]}, Email: {tenant[1]}, Phone: {tenant[2]}")
