"""
Process financial statements and load into database
"""

import sys
from pathlib import Path
from database import FinancialDatabase
from pdf_parser import FinancialStatementParser, load_from_csv
from config import FINANCIALS_DIR


def process_pdf(pdf_path, db):
    """Process a single PDF file"""
    parser = FinancialStatementParser()

    # Parse the PDF
    result = parser.parse_pdf(pdf_path)

    if not result:
        print(f"Failed to process {pdf_path}")
        return False

    # Add to database
    statement_id = db.add_financial_statement(
        location_code=result['location_code'],
        year=result['year'],
        month=result['month'],
        file_name=result['file_name']
    )

    if not statement_id:
        print(f"Failed to add statement to database")
        return False

    # Add P&L data
    for line_item, amount in result['pnl_data'].items():
        db.add_pnl_data(statement_id, line_item, amount)

    # Mark as processed
    db.mark_statement_processed(statement_id)

    print(f"✓ Successfully processed {result['file_name']}")
    return True


def process_csv(csv_path, db):
    """Process a manual entry CSV file"""
    result = load_from_csv(csv_path)

    if not result:
        print(f"Failed to process {csv_path}")
        return False

    # Add to database
    statement_id = db.add_financial_statement(
        location_code=result['location_code'],
        year=result['year'],
        month=result['month'],
        file_name=result['file_name']
    )

    if not statement_id:
        print(f"Failed to add statement to database")
        return False

    # Add P&L data
    for line_item, amount in result['pnl_data'].items():
        db.add_pnl_data(statement_id, line_item, amount)

    # Mark as processed
    db.mark_statement_processed(statement_id)

    print(f"✓ Successfully processed {result['file_name']}")
    return True


def process_all_financials():
    """Process all financial statements in the financials directory"""
    db = FinancialDatabase()

    print("=" * 60)
    print("Processing Financial Statements")
    print("=" * 60)

    # Find all PDF files
    pdf_files = list(FINANCIALS_DIR.glob("*.pdf"))
    csv_files = list(FINANCIALS_DIR.glob("manual_entry_*.csv"))

    if not pdf_files and not csv_files:
        print(f"\nNo files found in {FINANCIALS_DIR}")
        print("Please add PDF files with format: YYYY-MM_LocationCode.pdf")
        return

    total_files = len(pdf_files) + len(csv_files)
    processed = 0
    failed = 0

    # Process PDFs
    for pdf_file in pdf_files:
        print(f"\n[{processed + failed + 1}/{total_files}]")
        if process_pdf(pdf_file, db):
            processed += 1
        else:
            failed += 1

    # Process CSVs
    for csv_file in csv_files:
        print(f"\n[{processed + failed + 1}/{total_files}]")
        if process_csv(csv_file, db):
            processed += 1
        else:
            failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Processing Complete!")
    print(f"  Processed: {processed}")
    print(f"  Failed: {failed}")
    print(f"  Total: {total_files}")
    print("=" * 60)

    # Show database stats
    stats = db.get_summary_stats()
    if not stats.empty:
        print(f"\nDatabase Summary:")
        print(f"  Total locations with data: {stats['total_locations'].iloc[0]}")
        print(f"  Total statements: {stats['total_statements'].iloc[0]}")
        print(f"  Date range: {stats['earliest_date'].iloc[0]} to {stats['latest_date'].iloc[0]}")

    db.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process specific file
        file_path = Path(sys.argv[1])
        db = FinancialDatabase()

        if file_path.suffix == '.pdf':
            process_pdf(file_path, db)
        elif file_path.suffix == '.csv':
            process_csv(file_path, db)
        else:
            print("Unsupported file type. Use .pdf or .csv")

        db.close()
    else:
        # Process all files in financials directory
        process_all_financials()
