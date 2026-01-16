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

# Location mapping (updated to match current store list)
LOCATIONS = {
    "ANN": {"name": "Annapolis #101", "city": "Annapolis, MD", "status": "Open", "region": "Mid-Atlantic"},
    "AAV": {"name": "Atlantic Avenue #122", "city": "Virginia Beach, VA", "status": "Open", "region": "Virginia"},
    "ARL": {"name": "Arlington #121", "city": "Arlington, VA", "status": "Open", "region": "Virginia"},
    "AUS": {"name": "Austin", "city": "Austin, TX", "status": "Open", "region": "Texas"},
    "BEL": {"name": "Belleair Bluffs #129", "city": "Belleair Bluffs, FL", "status": "Open", "region": "Southwest Florida"},
    "BVS": {"name": "Belvedere Square #103", "city": "Baltimore, MD", "status": "Open", "region": "Mid-Atlantic"},
    "CHS": {"name": "Charleston #106", "city": "Charleston, SC", "status": "Open", "region": "Carolinas"},
    "CLT": {"name": "Charlotte #136", "city": "Charlotte, NC", "status": "Open", "region": "Carolinas"},
    "COC": {"name": "Coconut Point #140", "city": "Estero, FL", "status": "Coming soon", "region": "Southwest Florida"},
    "COS": {"name": "Colorado Springs #137", "city": "Colorado Springs, CO", "status": "Open", "region": "Colorado"},
    "DAL": {"name": "Dallas #139", "city": "Dallas, TX", "status": "Open", "region": "Texas"},
    "DEN": {"name": "Denver #117", "city": "Denver, CO", "status": "Open", "region": "Colorado"},
    "DUP": {"name": "Dupont #110", "city": "Washington, DC", "status": "Open", "region": "Mid-Atlantic"},
    "EPR": {"name": "E Pratt #103", "city": "Baltimore, MD", "status": "Open", "region": "Mid-Atlantic"},
    "FAL": {"name": "Falls Church #135", "city": "Falls Church, VA", "status": "Open", "region": "Virginia"},
    "FER": {"name": "Fernandina #126", "city": "Fernandina Beach, FL", "status": "Open", "region": "Northeast Florida"},
    "FLO": {"name": "Florence", "city": "Florence, Italy", "status": "Coming soon", "region": "International-Europe"},
    "FTL": {"name": "Ft. Lauderdale", "city": "Ft. Lauderdale, FL", "status": "Open", "region": "Southwest Florida"},
    "FDC": {"name": "Ft. Myers/Daniel's Crossing #138", "city": "Ft. Myers, FL", "status": "Open", "region": "Southwest Florida"},
    "FDP": {"name": "Ft. Myers/Downtown #130", "city": "Ft. Myers, FL", "status": "Open", "region": "Southwest Florida"},
    "GAI": {"name": "Gaithersburg - Rosé 130", "city": "Gaithersburg, MD", "status": "Open", "region": "Mid-Atlantic"},
    "LON": {"name": "Long Branch #126", "city": "Long Branch, NJ", "status": "Open", "region": "Northeast"},
    "MID": {"name": "Midlothian #131", "city": "Midlothian, VA", "status": "Open", "region": "Virginia"},
    "MIT": {"name": "Milan - Via Torino", "city": "Milan, Italy", "status": "Open", "region": "International-Europe"},
    "MIV": {"name": "Milan - Via Vespucci", "city": "Milan, Italy", "status": "Open", "region": "International-Europe"},
    "MOA": {"name": "Mall Of America #113", "city": "Bloomington, MN", "status": "Open", "region": "Midwest"},
    "NAT": {"name": "National Harbor #104", "city": "National Harbor, MD", "status": "Open", "region": "Mid-Atlantic"},
    "PAN": {"name": "Panama City Beach #124", "city": "Panama City Beach, FL", "status": "Open", "region": "Northeast Florida"},
    "REH": {"name": "Rehoboth #102", "city": "Rehoboth Beach, DE", "status": "Open", "region": "Mid-Atlantic"},
    "RES": {"name": "Reston #105", "city": "Reston, VA", "status": "Open", "region": "Virginia"},
    "RID": {"name": "Ridgewood", "city": "Ridgewood, NJ", "status": "Open", "region": "Northeast"},
    "SAU": {"name": "Saucon Valley", "city": "Saucon Valley, PA", "status": "Open", "region": "Northeast"},
    "SCO": {"name": "Scottsdale #118", "city": "Scottsdale, AZ", "status": "Open", "region": "Arizona"},
    "SDV": {"name": "Shore Drive #116", "city": "Virginia Beach, VA", "status": "Open", "region": "Virginia"},
    "SPV": {"name": "Short Pump #137", "city": "Richmond, VA", "status": "Open", "region": "Virginia"},
    "SJF": {"name": "St. Johns Town Center #133", "city": "Jacksonville, FL", "status": "Open", "region": "Northeast Florida"},
    "WAL": {"name": "Waldorf", "city": "Waldorf, MD", "status": "Open", "region": "Mid-Atlantic"},
    "WES": {"name": "Western Market #114", "city": "Washington, DC", "status": "Open", "region": "Mid-Atlantic"},
    "WHA": {"name": "Wharf #125", "city": "Washington, DC", "status": "Open", "region": "Mid-Atlantic"},
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
