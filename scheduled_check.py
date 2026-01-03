"""
Scheduled weekly check for missing financial statements
Run this weekly to identify which locations haven't submitted statements
"""

from datetime import datetime, timedelta
from database import FinancialDatabase
from config import LOCATIONS
import pandas as pd


def check_missing_statements(months_back=3):
    """
    Check for missing financial statements
    Args:
        months_back: How many months to check (default: 3)
    """
    db = FinancialDatabase()

    print("=" * 80)
    print("Mason's Famous Lobsters - Missing Statements Report")
    print("=" * 80)
    print(f"Checking last {months_back} months")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Get all data
    all_data = db.get_all_data()

    # Generate expected months
    today = datetime.now()
    expected_periods = []
    for i in range(months_back):
        date = today - timedelta(days=30*i)
        expected_periods.append((date.year, date.month))

    missing_reports = []

    # Check each location
    for location_code, location_info in LOCATIONS.items():
        # Skip "Coming soon" locations
        if location_info['status'] == 'Coming soon':
            continue

        location_name = location_info['name']

        # Get statements for this location
        location_data = all_data[all_data['location_code'] == location_code]

        # Check each expected period
        for year, month in expected_periods:
            period_data = location_data[
                (location_data['year'] == year) &
                (location_data['month'] == month)
            ]

            if period_data.empty:
                missing_reports.append({
                    'location_code': location_code,
                    'location_name': location_name,
                    'region': location_info['region'],
                    'year': year,
                    'month': month,
                    'period': f"{year}-{month:02d}"
                })

    if missing_reports:
        df = pd.DataFrame(missing_reports)

        print(f"\n⚠ MISSING STATEMENTS: {len(missing_reports)}")
        print("\nBy Period:")
        print(df.groupby('period').size().to_string())

        print("\nBy Location:")
        print(df.groupby(['location_code', 'location_name']).size().reset_index(name='missing_count').to_string(index=False))

        print("\nBy Region:")
        print(df.groupby('region').size().to_string())

        print("\nDetailed List:")
        print(df[['period', 'location_code', 'location_name', 'region']].to_string(index=False))

        # Save to CSV
        report_file = f"missing_statements_report_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(report_file, index=False)
        print(f"\n✓ Report saved to: {report_file}")

    else:
        print("\n✓ All locations have submitted statements for the checked periods!")

    # Show summary stats
    print("\n" + "=" * 80)
    stats = db.get_summary_stats()
    if not stats.empty:
        print("Database Summary:")
        print(f"  Total locations with data: {stats['total_locations'].iloc[0]}")
        print(f"  Total statements: {stats['total_statements'].iloc[0]}")
        print(f"  Date range: {stats['earliest_date'].iloc[0]} to {stats['latest_date'].iloc[0]}")
    print("=" * 80)

    db.close()

    return missing_reports


if __name__ == "__main__":
    import sys

    months = 3
    if len(sys.argv) > 1:
        months = int(sys.argv[1])

    check_missing_statements(months)
