#!/usr/bin/env python3
import requests
import json
import time
from urllib.parse import urlencode
from datetime import datetime, timedelta

class DigimindFetcher:
    def __init__(self, cookies):
        self.base_url = "https://social.digimind.com/d/hc1/rest/reader/feed/reportasync"
        self.session = requests.Session()
        self.session.cookies.update(cookies)
        self.session.headers.update({
            'Referer': 'https://social.digimind.com/d/hc1/reader/home.do',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def generate_report(self, title, topic_id, start_date, end_date, num_mentions=0):
        report_config = {
            "title": title,
            "type": "CSV",
            "numberOfMention": num_mentions,
            "unselectedClusters": [],
            "filters": {
                "topicId": topic_id,
                "query": "",
                "facets": [
                    {"name": "ranking", "value": 0, "type": "option"},
                    {"name": "ranking", "value": 10, "type": "option"},
                    {"name": "trash", "value": "trashed:false", "type": "option"}
                ],
                "dateRangeType": "CUSTOM",
                "startDate": start_date,
                "endDate": end_date
            },
            "sample": False,
            "sampleSize": "1000"
        }
        
        params = {'reportFormJson': json.dumps(report_config)}
        response = self.session.get(f"{self.base_url}/generate.do", params=params)
        response.raise_for_status()
        return response

    def check_status(self):
        response = self.session.get(f"{self.base_url}/checkdownload")
        response.raise_for_status()
        return response.json()

    def download_report(self, output_file):
        response = self.session.get(f"{self.base_url}/download.do", stream=True)
        response.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_file

    def fetch(self, title, topic_id, start_date, end_date, output_file, num_mentions=0):
        print(f"Generating report: {title}")
        self.generate_report(title, topic_id, start_date, end_date, num_mentions)
        
        print("Waiting for report generation...")
        while True:
            time.sleep(2)
            status = self.check_status()
            state = status.get('status')
            progress = status.get('progression', 0)
            print(f"Status: {state} - Progress: {progress}%")
            
            if state == 'COMPLETED':
                break
            elif state == 'FAILED':
                raise Exception("Report generation failed")
        
        print(f"Downloading to {output_file}")
        self.download_report(output_file)
        print("Done!")

if __name__ == "__main__":
    # Configure your cookies here
    cookies = {
        'JSESSIONID': 'YOUR_SESSION_ID',
        'USERINFO': 'YOUR_USER_INFO_TOKEN',
        'SSOTOKEN': 'YOUR_SSO_TOKEN',
        'DSCLIENT': 'hc1',
        'TRACEINFO': 'YOUR_TRACE_INFO'
    }
    
    # Example usage
    fetcher = DigimindFetcher(cookies)
    
    # Last 7 days
    end_date = datetime.utcnow().replace(hour=22, minute=59, second=59, microsecond=999000)
    start_date = (end_date - timedelta(days=7)).replace(hour=22, minute=0, second=0, microsecond=0)
    
    fetcher.fetch(
        title="Onclusive Social - CriterIA",
        topic_id=1,
        start_date=start_date.isoformat().replace('+00:00', 'Z'),
        end_date=end_date.isoformat().replace('+00:00', 'Z'),
        output_file="report.csv",
        num_mentions=351452
    )
