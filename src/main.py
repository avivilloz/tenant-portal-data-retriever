import sys
from .portals.clickpay import ClickPayPortal
from .database import Database
from .logger import logger


def main(portal_name, username, password):
    """
    Run the tenant portal data retriever.

    Usage: ./tenant_portal_data_retriever.py <tenant_portal> <username> <password>
    """
    portal_map = {
        "click_pay": ClickPayPortal,
        # Add other portals here in the future
    }

    if portal_name not in portal_map:
        logger.error(f"Unsupported portal: {portal_name}")
        return

    portal = portal_map[portal_name]()
    db = Database()

    try:
        tenant_data = portal.retrieve_data(username, password)
        db.insert_tenant(tenant_data)
        logger.info("Tenant data successfully retrieved and saved to the database.")
        db.print_all_tenants()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
