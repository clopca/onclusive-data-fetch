#!/usr/bin/env python3
import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import json

class DigimindSeleniumFetcher:
    def __init__(self, email, password, headless=True, download_dir=None):
        self.email = email
        self.password = password
        self.base_url = "https://social.digimind.com/d/hc1"
        self.download_dir = download_dir or os.path.join(os.getcwd(), "downloads")
        
        # Crear directorio de descargas si no existe
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Configurar Chrome
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Configurar descargas automáticas
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.session = None
    
    def login(self):
        """Login a Digimind y espera a que cargue el home"""
        print(f"Logging in as {self.email}...")
        self.driver.get(f"{self.base_url}/login.do")
        
        # Esperar y llenar el formulario
        email_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(self.email)
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.password)
        
        # Submit
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Esperar a que cargue el home (ajustar el selector según la página)
        print("Waiting for home page to load...")
        self.wait.until(
            EC.url_contains("/reader/home.do")
        )
        
        print("Login successful!")
        time.sleep(2)  # Esperar un poco más para que cargue todo
        
        # Extraer cookies para usar con requests
        self._extract_session()
    
    def _extract_session(self):
        """Extrae cookies del navegador y crea una sesión de requests"""
        cookies = self.driver.get_cookies()
        
        self.session = requests.Session()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        
        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en,es-ES;q=0.9,es;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': f'{self.base_url}/reader/home.do',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': self.driver.execute_script("return navigator.userAgent;")
        })
        
        print("Session cookies extracted")
    
    def generate_report(self, title, topic_id, start_date, end_date, num_mentions, date_range_type="CUSTOM"):
        """Genera el reporte usando la API con las cookies del navegador"""
        if not self.session:
            raise Exception("Must login first")
        
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
                "dateRangeType": date_range_type,
                "startDate": start_date,
                "endDate": end_date
            },
            "sample": False,
            "sampleSize": "1000"
        }
        
        url = f"{self.base_url}/rest/reader/feed/reportasync/generate.do"
        params = {'reportFormJson': json.dumps(report_config)}
        
        print(f"Generating report: {title}")
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response
    
    def check_status(self):
        """Chequea el estado del reporte"""
        url = f"{self.base_url}/rest/reader/feed/reportasync/checkdownload"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def download_report(self, output_file):
        """Descarga el reporte cuando esté listo"""
        url = f"{self.base_url}/rest/reader/feed/reportasync/download.do"
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Report downloaded to: {output_file}")
        return output_file
    
    def fetch(self, title, topic_id, start_date, end_date, output_file, num_mentions=0, date_range_type="CUSTOM", max_wait_time=600):
        """Flujo completo: login -> generar -> esperar -> descargar"""
        
        # Login
        self.login()
        
        # Generar reporte
        print(f"Period: {start_date} to {end_date}")
        print(f"Mentions: {num_mentions}")
        self.generate_report(title, topic_id, start_date, end_date, num_mentions, date_range_type)
        
        # Esperar a que se complete
        print("Waiting for report generation...")
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                raise Exception(f"Timeout after {max_wait_time}s")
            
            time.sleep(3)
            status = self.check_status()
            state = status.get('status')
            progress = status.get('progression', 0)
            print(f"Status: {state} - Progress: {progress}% (elapsed: {elapsed:.0f}s)")
            
            if state == 'COMPLETED':
                break
            elif state == 'FAILED':
                raise Exception("Report generation failed")
        
        # Descargar
        self.download_report(output_file)
        print("Done!")
        return output_file
    
    def close(self):
        """Cerrar el navegador"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    # Usar variables de entorno para credenciales
    EMAIL = os.getenv("DIGIMIND_EMAIL", "cristobal.callejon@gmail.com")
    PASSWORD = os.getenv("DIGIMIND_PASSWORD")
    
    if not PASSWORD:
        raise Exception("Set DIGIMIND_PASSWORD environment variable")
    
    with DigimindSeleniumFetcher(EMAIL, PASSWORD, headless=True) as fetcher:
        # Today's report
        end_date = datetime.utcnow().replace(hour=22, minute=59, second=59, microsecond=999000)
        start_date = end_date.replace(hour=23, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        fetcher.fetch(
            title="test-all-today",
            topic_id=1,
            start_date=start_date.isoformat().replace('+00:00', '.000Z'),
            end_date=end_date.isoformat().replace('+00:00', '.999Z'),
            output_file="digimind_report.csv",
            num_mentions=38345,
            date_range_type="TODAY"
        )

