# Tenant Portal Data Retriever

This application retrieves tenant data from various tenant portals and stores it in a local SQLite database.

## Features

- Supports multiple tenant portals (currently implemented: ClickPay)
- Retrieves tenant email and phone number
- Stores data in a local SQLite database
- Logs operations for debugging and monitoring

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/avivilloz/tenant-portal-data-retriever.git
   cd tenant-portal-data-retriever
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line with the following arguments:

```
python tenant_portal_data_retriever.py <tenant_portal> <username> <password>
```

## Output

The script will:
1. Log in to the specified tenant portal
2. Retrieve the tenant's email and phone number
3. Store this information in a local SQLite database (`db/tenant_data.db`)
4. Print the retrieved information to the console
5. Log all operations to `logs/tenant_portal_retriever.log`

## Configuration

- You can change log level in `src/config.py` file.