#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from fetch_selenium import DigimindSeleniumFetcher

def main():
    # Credenciales desde env vars
    EMAIL = os.getenv("DIGIMIND_EMAIL", "cristobal.callejon@gmail.com")
    PASSWORD = os.getenv("DIGIMIND_PASSWORD")
    
    if not PASSWORD:
        print("ERROR: Set DIGIMIND_PASSWORD environment variable")
        print("Example: export DIGIMIND_PASSWORD='your_password'")
        return
    
    # Crear fetcher con context manager (cierra automáticamente el navegador)
    with DigimindSeleniumFetcher(EMAIL, PASSWORD, headless=False) as fetcher:
        # Today
        end_date = datetime.utcnow().replace(hour=22, minute=59, second=59, microsecond=999000)
        start_date = end_date.replace(hour=23, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        fetcher.fetch(
            title="test-all-today",
            topic_id=1,
            start_date=start_date.isoformat().replace('+00:00', '.000Z'),
            end_date=end_date.isoformat().replace('+00:00', '.999Z'),
            output_file="report_today.xlsx",
            num_mentions=38345,
            date_range_type="TODAY"
        )

if __name__ == "__main__":
    main()

