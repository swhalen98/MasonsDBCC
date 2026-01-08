"""
Configuration file for Mason's Famous Lobster P&L Dashboard
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
FINANCIALS_DIR = BASE_DIR / "financials"
DATABASE_PATH = BASE_DIR / "masons_financials.duckdb"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
FINANCIALS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Location mapping
LOCATIONS = {
    "ANN": {"name": "Annapolis", "city": "Annapolis, MD", "status": "Open", "region": "Mid-Atlantic"},
    "ARL": {"name": "Arlington – Village at Shirlington", "city": "Arlington, VA", "status": "Open", "region": "Virginia"},
    "AUS": {"name": "Austin", "city": "Austin, TX", "status": "Open", "region": "Texas"},
    "BEL": {"name": "Belleair Bluffs", "city": "Belleair Bluffs, FL", "status": "Open", "region": "Southwest Florida"},
    "BVS": {"name": "Belvedere Square", "city": "Baltimore, MD", "status": "Open", "region": "Mid-Atlantic"},
    "CAR": {"name": "Cary – Waverly Place", "city": "Cary, NC", "status": "Open", "region": "Carolinas"},
    "CHS": {"name": "Charleston", "city": "Charleston, SC", "status": "Open", "region": "Carolinas"},
    "CLT": {"name": "Charlotte", "city": "Charlotte, NC", "status": "Open", "region": "Carolinas"},
    "COS": {"name": "Colorado Springs", "city": "Colorado Springs, CO", "status": "Open", "region": "Colorado"},
    "DAL": {"name": "Dallas", "city": "Dallas, TX", "status": "Coming soon", "region": "Texas"},
    "DEN": {"name": "Denver", "city": "Denver, CO", "status": "Open", "region": "Colorado"},
    "DUP": {"name": "Dupont Circle", "city": "Washington, DC", "status": "Open", "region": "Mid-Atlantic"},
    "FAL": {"name": "Falls Church", "city": "Falls Church, VA", "status": "Open", "region": "Virginia"},
    "FER": {"name": "Fernandina Beach", "city": "Fernandina Beach, FL", "status": "Open", "region": "Florida"},
    "FMD": {"name": "Fort Myers – Downtown", "city": "Fort Myers, FL", "status": "Open", "region": "Southwest Florida"},
    "FMD2": {"name": "Fort Myers – Daniels Parkway", "city": "Fort Myers, FL", "status": "Coming soon", "region": "Southwest Florida"},
    "GAI": {"name": "Gaithersburg – Rio Lakefront", "city": "Gaithersburg, MD", "status": "Open", "region": "Mid-Atlantic"},
    "HAR": {"name": "Harborplace", "city": "Baltimore, MD", "status": "Open", "region": "Mid-Atlantic"},
    "LON": {"name": "Long Branch", "city": "Long Branch, NJ", "status": "Open", "region": "Northeast"},
    "MOA": {"name": "Mall of America", "city": "Bloomington, MN", "status": "Open", "region": "Midwest"},
    "MAR": {"name": "Marina Village", "city": "Fort Lauderdale, FL", "status": "Open", "region": "Florida"},
    "MID": {"name": "Midlothian", "city": "Midlothian, VA", "status": "Open", "region": "Virginia"},
    "MIL": {"name": "Milan", "city": "Milan, Italy", "status": "Open", "region": "International"},
    "NAT": {"name": "National Harbor", "city": "National Harbor, MD", "status": "Open", "region": "Mid-Atlantic"},
    "PAN": {"name": "Panama City Beach", "city": "Panama City Beach, FL", "status": "Open", "region": "Florida"},
    "REH": {"name": "Rehoboth Beach", "city": "Rehoboth Beach, DE", "status": "Open", "region": "Mid-Atlantic"},
    "RES": {"name": "Reston", "city": "Reston, VA", "status": "Open", "region": "Virginia"},
    "SCO": {"name": "Scottsdale", "city": "Scottsdale, AZ", "status": "Open", "region": "Arizona"},
    "COC": {"name": "Coconut Point", "city": "Estero, FL", "status": "Coming soon", "region": "Southwest Florida"},
    "FLO": {"name": "Florence", "city": "Florence, Italy", "status": "Coming soon", "region": "International"},
}

# Standard P&L line items to extract (Income Statement)
PNL_LINE_ITEMS = [
    "Total Revenue",
    "Food Sales",
    "Beverage Sales",
    "Cost of Goods Sold",
    "Gross Profit",
    "Labor",
    "Rent",
    "Utilities",
    "Marketing",
    "Insurance",
    "Repairs & Maintenance",
    "Supplies",
    "Other Operating Expenses",
    "Total Operating Expenses",
    "EBITDA",
    "Net Income",
]

# Balance Sheet line items to extract
BALANCE_SHEET_ITEMS = [
    # Assets
    "Cash",
    "Accounts Receivable",
    "Inventory",
    "Prepaid Expenses",
    "Total Current Assets",
    "Property & Equipment",
    "Accumulated Depreciation",
    "Net Property & Equipment",
    "Other Assets",
    "Total Assets",
    # Liabilities
    "Accounts Payable",
    "Accrued Expenses",
    "Short-term Debt",
    "Total Current Liabilities",
    "Long-term Debt",
    "Total Liabilities",
    # Equity
    "Owner's Equity",
    "Retained Earnings",
    "Total Equity",
    "Total Liabilities & Equity",
]

# Cash Flow line items to extract
CASH_FLOW_ITEMS = [
    # Operating Activities
    "Net Income",
    "Depreciation",
    "Changes in Working Capital",
    "Cash from Operations",
    # Investing Activities
    "Capital Expenditures",
    "Asset Sales",
    "Cash from Investing",
    # Financing Activities
    "Debt Proceeds",
    "Debt Payments",
    "Owner Distributions",
    "Cash from Financing",
    # Summary
    "Net Change in Cash",
    "Beginning Cash",
    "Ending Cash",
]

# Authentication (use environment variables in production)
DEFAULT_USERS = {
    "admin": os.getenv("ADMIN_PASSWORD", "changeme123"),  # Change this!
    "manager": os.getenv("MANAGER_PASSWORD", "changeme456"),  # Change this!
    "viewer": os.getenv("VIEWER_PASSWORD", "changeme789"),  # Change this!
}

# Dashboard settings
DASHBOARD_TITLE = "Mason's Famous Lobsters P&L"
DASHBOARD_PORT = int(os.getenv("PORT", 5000))
