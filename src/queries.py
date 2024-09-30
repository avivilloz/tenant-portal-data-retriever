"""
This module contains SQL queries used in the application.
"""

CREATE_TENANTS_TABLE = """
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    phone TEXT
)
"""

INSERT_TENANT = """
INSERT INTO tenants (email, phone)
VALUES (?, ?)
"""

SELECT_ALL_TENANTS = """
SELECT * FROM tenants
"""
