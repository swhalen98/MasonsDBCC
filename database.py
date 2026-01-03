"""
Database management for financial statements
"""

import duckdb
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import DATABASE_PATH, LOCATIONS, PNL_LINE_ITEMS


class FinancialDatabase:
    """Manages the DuckDB database for financial statements"""

    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()

    def initialize_database(self):
        """Create tables if they don't exist"""
        self.conn = duckdb.connect(str(self.db_path))

        # Locations table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                location_code VARCHAR PRIMARY KEY,
                location_name VARCHAR NOT NULL,
                city VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                region VARCHAR NOT NULL
            )
        """)

        # Financial statements table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS financial_statements (
                id INTEGER PRIMARY KEY,
                location_code VARCHAR NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                period_date DATE NOT NULL,
                file_name VARCHAR NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (location_code) REFERENCES locations(location_code),
                UNIQUE(location_code, year, month)
            )
        """)

        # P&L line items table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS pnl_data (
                id INTEGER PRIMARY KEY,
                statement_id INTEGER NOT NULL,
                line_item VARCHAR NOT NULL,
                amount DECIMAL(15, 2),
                FOREIGN KEY (statement_id) REFERENCES financial_statements(id),
                UNIQUE(statement_id, line_item)
            )
        """)

        # Populate locations
        self._populate_locations()

    def _populate_locations(self):
        """Insert or update location data"""
        for code, info in LOCATIONS.items():
            self.conn.execute("""
                INSERT INTO locations (location_code, location_name, city, status, region)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (location_code)
                DO UPDATE SET
                    location_name = EXCLUDED.location_name,
                    city = EXCLUDED.city,
                    status = EXCLUDED.status,
                    region = EXCLUDED.region
            """, [code, info["name"], info["city"], info["status"], info["region"]])

    def add_financial_statement(self, location_code, year, month, file_name):
        """Add a new financial statement record"""
        period_date = datetime(year, month, 1).date()

        try:
            result = self.conn.execute("""
                INSERT INTO financial_statements
                (location_code, year, month, period_date, file_name, processed)
                VALUES (?, ?, ?, ?, ?, FALSE)
                RETURNING id
            """, [location_code, year, month, period_date, file_name])

            statement_id = result.fetchone()[0]
            return statement_id
        except Exception as e:
            print(f"Error adding statement: {e}")
            return None

    def add_pnl_data(self, statement_id, line_item, amount):
        """Add P&L line item data"""
        try:
            self.conn.execute("""
                INSERT INTO pnl_data (statement_id, line_item, amount)
                VALUES (?, ?, ?)
                ON CONFLICT (statement_id, line_item)
                DO UPDATE SET amount = EXCLUDED.amount
            """, [statement_id, line_item, amount])
        except Exception as e:
            print(f"Error adding P&L data: {e}")

    def mark_statement_processed(self, statement_id):
        """Mark a statement as processed"""
        self.conn.execute("""
            UPDATE financial_statements
            SET processed = TRUE
            WHERE id = ?
        """, [statement_id])

    def get_all_data(self):
        """Get all financial data with location info"""
        query = """
            SELECT
                l.location_code,
                l.location_name,
                l.city,
                l.region,
                l.status,
                fs.year,
                fs.month,
                fs.period_date,
                p.line_item,
                p.amount
            FROM locations l
            LEFT JOIN financial_statements fs ON l.location_code = fs.location_code
            LEFT JOIN pnl_data p ON fs.id = p.statement_id
            WHERE fs.processed = TRUE OR fs.id IS NULL
            ORDER BY fs.year DESC, fs.month DESC, l.location_name, p.line_item
        """
        return self.conn.execute(query).df()

    def get_data_by_location(self, location_code):
        """Get financial data for a specific location"""
        query = """
            SELECT
                fs.year,
                fs.month,
                fs.period_date,
                p.line_item,
                p.amount
            FROM financial_statements fs
            JOIN pnl_data p ON fs.id = p.statement_id
            WHERE fs.location_code = ? AND fs.processed = TRUE
            ORDER BY fs.year DESC, fs.month DESC, p.line_item
        """
        return self.conn.execute(query, [location_code]).df()

    def get_data_by_region(self, region):
        """Get aggregated financial data for a region"""
        query = """
            SELECT
                fs.year,
                fs.month,
                p.line_item,
                SUM(p.amount) as amount
            FROM locations l
            JOIN financial_statements fs ON l.location_code = fs.location_code
            JOIN pnl_data p ON fs.id = p.statement_id
            WHERE l.region = ? AND fs.processed = TRUE
            GROUP BY fs.year, fs.month, p.line_item
            ORDER BY fs.year DESC, fs.month DESC, p.line_item
        """
        return self.conn.execute(query, [region]).df()

    def get_consolidated_data(self):
        """Get consolidated financial data across all locations"""
        query = """
            SELECT
                fs.year,
                fs.month,
                p.line_item,
                SUM(p.amount) as amount,
                COUNT(DISTINCT fs.location_code) as location_count
            FROM financial_statements fs
            JOIN pnl_data p ON fs.id = p.statement_id
            WHERE fs.processed = TRUE
            GROUP BY fs.year, fs.month, p.line_item
            ORDER BY fs.year DESC, fs.month DESC, p.line_item
        """
        return self.conn.execute(query).df()

    def get_summary_stats(self):
        """Get summary statistics"""
        return self.conn.execute("""
            SELECT
                COUNT(DISTINCT location_code) as total_locations,
                COUNT(*) as total_statements,
                MIN(period_date) as earliest_date,
                MAX(period_date) as latest_date
            FROM financial_statements
            WHERE processed = TRUE
        """).df()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# Initialize database on import
if __name__ == "__main__":
    db = FinancialDatabase()
    print("Database initialized successfully")
    print(db.get_summary_stats())
    db.close()
