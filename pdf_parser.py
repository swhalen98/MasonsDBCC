"""
PDF Parser for financial statements
Extracts P&L data from PDF files
"""

import re
import pdfplumber
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import PNL_LINE_ITEMS, BALANCE_SHEET_ITEMS, CASH_FLOW_ITEMS, LOCATIONS


class FinancialStatementParser:
    """Parses financial statement PDFs and extracts financial data"""

    def __init__(self):
        self.pnl_items = PNL_LINE_ITEMS
        self.balance_sheet_items = BALANCE_SHEET_ITEMS
        self.cash_flow_items = CASH_FLOW_ITEMS

    def parse_filename(self, filename):
        """
        Parse filename to extract date, location, and statement type
        Expected formats:
            YYYY-MM_LocationCode.pdf (all statements)
            YYYY-MM_LocationCode_ALL.pdf (all statements, explicit)
            YYYY-MM_LocationCode_IS.pdf (income statement only)
            YYYY-MM_LocationCode_BS.pdf (balance sheet only)
            YYYY-MM_LocationCode_CF.pdf (cash flow only)
        Returns: (year, month, location_code, statement_type) or None if invalid
        """
        # Pattern with optional statement type suffix
        pattern = r'(\d{4})-(\d{2})_([A-Z0-9]+)(?:_(IS|BS|CF|ALL))?\.pdf'
        match = re.match(pattern, filename)

        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            location_code = match.group(3)
            statement_type = match.group(4) or 'ALL'  # Default to ALL if not specified

            # Validate location code
            if location_code in LOCATIONS:
                return year, month, location_code, statement_type
            else:
                print(f"Warning: Unknown location code '{location_code}' in {filename}")
                return None
        else:
            print(f"Warning: Invalid filename format: {filename}")
            print("Expected formats:")
            print("  YYYY-MM_LocationCode.pdf (e.g., 2026-01_ANN.pdf)")
            print("  YYYY-MM_LocationCode_IS.pdf (income statement)")
            print("  YYYY-MM_LocationCode_BS.pdf (balance sheet)")
            print("  YYYY-MM_LocationCode_CF.pdf (cash flow)")
            return None

    def extract_text_from_pdf(self, pdf_path):
        """Extract all text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return None
        return text

    def extract_tables_from_pdf(self, pdf_path):
        """Extract tables from PDF"""
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
        except Exception as e:
            print(f"Error extracting tables from {pdf_path}: {e}")
            return None
        return tables

    def parse_amount(self, amount_str):
        """
        Parse monetary amount from string
        Handles formats like: $1,234.56, (1,234.56), -1,234.56
        """
        if not amount_str or pd.isna(amount_str):
            return None

        # Convert to string and clean
        amount_str = str(amount_str).strip()

        # Check for parentheses (negative number in accounting)
        is_negative = False
        if '(' in amount_str and ')' in amount_str:
            is_negative = True
            amount_str = amount_str.replace('(', '').replace(')', '')

        # Remove currency symbols and commas
        amount_str = re.sub(r'[$,\s]', '', amount_str)

        # Try to convert to float
        try:
            amount = float(amount_str)
            return -amount if is_negative else amount
        except ValueError:
            return None

    def extract_statement_data(self, text, tables, line_items):
        """
        Generic method to extract financial statement line items and amounts
        Returns: dict of {line_item: amount}
        """
        data = {}

        # Method 1: Try to extract from tables first
        if tables:
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                for _, row in df.iterrows():
                    for line_item in line_items:
                        # Check each cell for the line item name
                        for cell in row:
                            if cell and isinstance(cell, str):
                                if line_item.lower() in cell.lower():
                                    # Look for amount in the same row
                                    for value in row:
                                        amount = self.parse_amount(value)
                                        if amount is not None:
                                            data[line_item] = amount
                                            break
                                    break

        # Method 2: Parse from text using regex
        if not data and text:
            lines = text.split('\n')
            for line in lines:
                for line_item in line_items:
                    # Look for line item followed by amount
                    if line_item.lower() in line.lower():
                        # Extract numbers from the line
                        amounts = re.findall(r'[\$\(]?[\d,]+\.?\d*[\)]?', line)
                        if amounts:
                            # Take the last amount on the line (usually the total)
                            amount = self.parse_amount(amounts[-1])
                            if amount is not None:
                                data[line_item] = amount

        return data

    def extract_pnl_data(self, text, tables=None):
        """Extract P&L/Income Statement data"""
        return self.extract_statement_data(text, tables, self.pnl_items)

    def extract_balance_sheet_data(self, text, tables=None):
        """Extract Balance Sheet data"""
        return self.extract_statement_data(text, tables, self.balance_sheet_items)

    def extract_cash_flow_data(self, text, tables=None):
        """Extract Cash Flow Statement data"""
        return self.extract_statement_data(text, tables, self.cash_flow_items)

    def parse_pdf(self, pdf_path):
        """
        Main parsing function
        Returns: dict with metadata and all extracted statement data or None if failed
        """
        pdf_path = Path(pdf_path)

        # Parse filename
        file_info = self.parse_filename(pdf_path.name)
        if not file_info:
            return None

        year, month, location_code, statement_type = file_info

        print(f"Processing: {pdf_path.name}")
        print(f"  Location: {LOCATIONS[location_code]['name']}")
        print(f"  Period: {year}-{month:02d}")
        print(f"  Statement Type: {statement_type}")

        # Extract text and tables
        text = self.extract_text_from_pdf(pdf_path)
        tables = self.extract_tables_from_pdf(pdf_path)

        if not text and not tables:
            print(f"  Error: Could not extract any data from PDF")
            return None

        # Extract data based on statement type
        pnl_data = {}
        balance_sheet_data = {}
        cash_flow_data = {}

        if statement_type in ['ALL', 'IS']:
            pnl_data = self.extract_pnl_data(text, tables)
            if pnl_data:
                print(f"  Extracted {len(pnl_data)} P&L line items")
            else:
                print(f"  Warning: No P&L line items found.")

        if statement_type in ['ALL', 'BS']:
            balance_sheet_data = self.extract_balance_sheet_data(text, tables)
            if balance_sheet_data:
                print(f"  Extracted {len(balance_sheet_data)} Balance Sheet line items")
            else:
                print(f"  Warning: No Balance Sheet line items found.")

        if statement_type in ['ALL', 'CF']:
            cash_flow_data = self.extract_cash_flow_data(text, tables)
            if cash_flow_data:
                print(f"  Extracted {len(cash_flow_data)} Cash Flow line items")
            else:
                print(f"  Warning: No Cash Flow line items found.")

        result = {
            'year': year,
            'month': month,
            'location_code': location_code,
            'statement_type': statement_type,
            'file_name': pdf_path.name,
            'pnl_data': pnl_data,
            'balance_sheet_data': balance_sheet_data,
            'cash_flow_data': cash_flow_data
        }

        return result


# Manual data entry helper for when PDFs can't be parsed automatically
def create_manual_entry_template(location_code, year, month):
    """
    Create a CSV template for manual data entry
    """
    df = pd.DataFrame({
        'line_item': PNL_LINE_ITEMS,
        'amount': [0.0] * len(PNL_LINE_ITEMS)
    })

    filename = f"manual_entry_{year}-{month:02d}_{location_code}.csv"
    df.to_csv(filename, index=False)
    print(f"Created manual entry template: {filename}")
    print("Fill in the amounts and save. Then use load_from_csv() to import.")

    return filename


def load_from_csv(csv_path):
    """
    Load financial data from CSV template
    Returns: dict with metadata and P&L data
    """
    csv_path = Path(csv_path)

    # Parse filename
    pattern = r'manual_entry_(\d{4})-(\d{2})_([A-Z0-9]+)\.csv'
    match = re.match(pattern, csv_path.name)

    if not match:
        print(f"Invalid CSV filename format: {csv_path.name}")
        return None

    year = int(match.group(1))
    month = int(match.group(2))
    location_code = match.group(3)

    # Load CSV
    df = pd.read_csv(csv_path)
    pnl_data = dict(zip(df['line_item'], df['amount']))

    result = {
        'year': year,
        'month': month,
        'location_code': location_code,
        'file_name': csv_path.name,
        'pnl_data': pnl_data
    }

    return result


if __name__ == "__main__":
    # Test the parser
    parser = FinancialStatementParser()

    # Example: Create manual entry template
    create_manual_entry_template('ANN', 2026, 1)
