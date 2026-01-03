"""
PDF Parser for financial statements
Extracts P&L data from PDF files
"""

import re
import pdfplumber
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import PNL_LINE_ITEMS, LOCATIONS


class FinancialStatementParser:
    """Parses financial statement PDFs and extracts P&L data"""

    def __init__(self):
        self.line_items = PNL_LINE_ITEMS

    def parse_filename(self, filename):
        """
        Parse filename to extract date and location
        Expected format: YYYY-MM_LocationCode.pdf
        Returns: (year, month, location_code) or None if invalid
        """
        pattern = r'(\d{4})-(\d{2})_([A-Z0-9]+)\.pdf'
        match = re.match(pattern, filename)

        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            location_code = match.group(3)

            # Validate location code
            if location_code in LOCATIONS:
                return year, month, location_code
            else:
                print(f"Warning: Unknown location code '{location_code}' in {filename}")
                return None
        else:
            print(f"Warning: Invalid filename format: {filename}")
            print("Expected format: YYYY-MM_LocationCode.pdf (e.g., 2026-01_ANN.pdf)")
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

    def extract_pnl_data(self, text, tables=None):
        """
        Extract P&L line items and amounts from text and tables
        Returns: dict of {line_item: amount}
        """
        pnl_data = {}

        # Method 1: Try to extract from tables first
        if tables:
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                for _, row in df.iterrows():
                    for line_item in self.line_items:
                        # Check each cell for the line item name
                        for cell in row:
                            if cell and isinstance(cell, str):
                                if line_item.lower() in cell.lower():
                                    # Look for amount in the same row
                                    for value in row:
                                        amount = self.parse_amount(value)
                                        if amount is not None:
                                            pnl_data[line_item] = amount
                                            break
                                    break

        # Method 2: Parse from text using regex
        if not pnl_data and text:
            lines = text.split('\n')
            for line in lines:
                for line_item in self.line_items:
                    # Look for line item followed by amount
                    if line_item.lower() in line.lower():
                        # Extract numbers from the line
                        amounts = re.findall(r'[\$\(]?[\d,]+\.?\d*[\)]?', line)
                        if amounts:
                            # Take the last amount on the line (usually the total)
                            amount = self.parse_amount(amounts[-1])
                            if amount is not None:
                                pnl_data[line_item] = amount

        return pnl_data

    def parse_pdf(self, pdf_path):
        """
        Main parsing function
        Returns: dict with metadata and P&L data or None if failed
        """
        pdf_path = Path(pdf_path)

        # Parse filename
        file_info = self.parse_filename(pdf_path.name)
        if not file_info:
            return None

        year, month, location_code = file_info

        print(f"Processing: {pdf_path.name}")
        print(f"  Location: {LOCATIONS[location_code]['name']}")
        print(f"  Period: {year}-{month:02d}")

        # Extract text and tables
        text = self.extract_text_from_pdf(pdf_path)
        tables = self.extract_tables_from_pdf(pdf_path)

        if not text and not tables:
            print(f"  Error: Could not extract any data from PDF")
            return None

        # Extract P&L data
        pnl_data = self.extract_pnl_data(text, tables)

        if not pnl_data:
            print(f"  Warning: No P&L line items found. Manual review may be needed.")
            print(f"  Please check the PDF format and ensure it contains standard P&L items.")

        result = {
            'year': year,
            'month': month,
            'location_code': location_code,
            'file_name': pdf_path.name,
            'pnl_data': pnl_data
        }

        print(f"  Extracted {len(pnl_data)} line items")

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
