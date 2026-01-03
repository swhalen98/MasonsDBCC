"""
Automated file monitoring and processing
Watches the financials directory for new files and processes them automatically
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import FinancialDatabase
from process_financials import process_pdf, process_csv
from config import FINANCIALS_DIR, LOGS_DIR
from datetime import datetime


class FinancialFileHandler(FileSystemEventHandler):
    """Handles new financial statement files"""

    def __init__(self):
        self.db = FinancialDatabase()
        self.processing = set()  # Track files being processed
        self.log_file = LOGS_DIR / f"auto_process_{datetime.now().strftime('%Y%m%d')}.log"

    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')

    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process PDF and CSV files
        if file_path.suffix not in ['.pdf', '.csv']:
            return

        # Avoid processing the same file multiple times
        if file_path in self.processing:
            return

        self.processing.add(file_path)

        # Wait a moment to ensure file is fully written
        time.sleep(2)

        self.log(f"New file detected: {file_path.name}")

        try:
            if file_path.suffix == '.pdf':
                success = process_pdf(file_path, self.db)
            elif file_path.name.startswith('manual_entry_') and file_path.suffix == '.csv':
                success = process_csv(file_path, self.db)
            else:
                self.log(f"Skipping non-financial file: {file_path.name}")
                self.processing.remove(file_path)
                return

            if success:
                self.log(f"✓ Successfully processed: {file_path.name}")
            else:
                self.log(f"✗ Failed to process: {file_path.name}")

        except Exception as e:
            self.log(f"✗ Error processing {file_path.name}: {e}")

        finally:
            self.processing.remove(file_path)

    def on_modified(self, event):
        """Handle file modifications (treat as new file)"""
        # Treat modifications as new uploads
        self.on_created(event)


def run_auto_processor():
    """Run the automated file processor"""
    print("=" * 60)
    print("Mason's Famous Lobsters - Automated Financial Processor")
    print("=" * 60)
    print(f"Monitoring directory: {FINANCIALS_DIR}")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    event_handler = FinancialFileHandler()
    observer = Observer()
    observer.schedule(event_handler, str(FINANCIALS_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping automated processor...")
        observer.stop()
        event_handler.db.close()

    observer.join()
    print("Automated processor stopped.")


if __name__ == "__main__":
    # Ensure financials directory exists
    FINANCIALS_DIR.mkdir(exist_ok=True)

    run_auto_processor()
