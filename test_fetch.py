#!/usr/bin/env python3
from fetch_report import DigimindFetcher

# Cookies from your browser session
cookies = {
    'JSESSIONID': '2178BD5E347096C9170C092EE4A8AAC8',
    'USERINFO': 'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJqd3RUb2tlbkdlbmVyYXRvciIsInN1YiI6ImNyaXN0b2JhbC5jYWxsZWpvbkBnbWFpbC5jb20iLCJjbGllbnQiOiJoYzEiLCJpZCI6NDEsIm5hbWUiOiJDcmlzdG9iYWwgTG9wZXoiLCJyb2xlIjoiRCIsImRmIjoiZGQvTU0veXl5eSIsImlhdCI6MTc2MTY0MzM2MSwiZXhwIjoxNzYxNjQ1MTYxLCJsYW5nIjoiZW4iLCJ0eiI6IkV1cm9wZS9NYWRyaWQifQ.X7fOrFq8ZtuSFd4EWRtQvsBMn5Vi4pw_zTCMRN4kMqewJA1erS2pWGk4UM2sdf9deJ2MES4EC2rZ348vx7tBEDYxth_r1KelUnFA9qT72eM2sBF46OCNBEMovrJcp8nX1nD2KU5-qc-rCgJ6s4rsL02aRwYbXpq9oqVhEq7lX307GDbxBi_WrQpM-0IyoVFlpmFxy7K5zbWEx00wobIIMJrOy-qNeHRr6B5WoOW0xWcycm_pGttu5pRCyL0Q02KdBPVthsMIrTobxgdHFmSsQMKrn6XM5EkOzpJfrJtPblCXMHXtWaeGjjyXeVecLck7u0Oqrl66IE_sk2Eq2yYO2Q',
    'SSOTOKEN': 'NLsbpaWYEHxtOUeYilExhsVlpdFTtxyairagFThrbQxzSZPmtY',
    'DSCLIENT': 'hc1',
    'TRACEINFO': 'hc1%3A%3Acristobal.callejon%40gmail.com'
}

fetcher = DigimindFetcher(cookies)

# Using the exact parameters from your example
fetcher.fetch(
    title="Onclusive Social  - CriterIA",
    topic_id=1,
    start_date="2025-10-21T22:00:00.000Z",
    end_date="2025-10-28T22:59:59.999Z",
    output_file="onclusive_report.csv",
    num_mentions=351452
)
