#!/usr/bin/env python3
import requests
import concurrent.futures
import time
import logging
import sys
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('proxy_check.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class ProxyChecker:
    def __init__(self, timeout=10, max_workers=50):
        self.timeout = timeout
        self.max_workers = max_workers
        self.test_urls = [
            'http://httpbin.org/ip',
            'https://api.ipify.org?format=json',
            'http://icanhazip.com'
        ]
        
    def get_proxy_sources(self):
        sources = [
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
            'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt'
        ]
        return sources
    
    def fetch_proxies_from_source(self, url):
        try:
            logging.info(f"Fetching proxies from: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            proxies = []
            for line in response.text.splitlines():
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        try:
                            ip, port = parts[0], int(parts[1])
                            if 1 <= port <= 65535:
                                proxies.append(f"http://{ip}:{port}")
                        except ValueError:
                            continue
            
            logging.info(f"Found {len(proxies)} proxies from {url}")
            return proxies
            
        except Exception as e:
            logging.error(f"Error fetching from {url}: {e}")
            return []
    
    def test_proxy(self, proxy):
        try:
            proxy_dict = {
                'http': proxy,
                'https': proxy
            }
            
            test_url = self.test_urls[0]
            response = requests.get(
                test_url,
                proxies=proxy_dict,
                timeout=self.timeout,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                logging.info(f"✓ Working proxy: {proxy}")
                return proxy
                
        except Exception as e:
            logging.debug(f"✗ Failed proxy {proxy}: {e}")
            
        return None
    
    def check_proxies_batch(self, proxies):
        working_proxies = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in proxies}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                if result:
                    working_proxies.append(result)
        
        return working_proxies
    
    def run(self):
        start_time = time.time()
        logging.info("Starting proxy collection and testing...")
        
        all_proxies = set()
        sources = self.get_proxy_sources()
        
        for source in sources:
            proxies = self.fetch_proxies_from_source(source)
            all_proxies.update(proxies)
        
        all_proxies = list(all_proxies)
        logging.info(f"Total unique proxies collected: {len(all_proxies)}")
        
        if not all_proxies:
            logging.error("No proxies found!")
            sys.exit(1)
        
        working_proxies = self.check_proxies_batch(all_proxies)
        
        if working_proxies:
            with open('alive_proxies.txt', 'w', encoding='utf-8') as f:
                for proxy in working_proxies:
                    f.write(proxy + '\n')
            
            elapsed = time.time() - start_time
            logging.info(f"✓ Found {len(working_proxies)} working proxies in {elapsed:.2f} seconds")
            logging.info(f"Success rate: {len(working_proxies)/len(all_proxies)*100:.1f}%")
        else:
            logging.error("No working proxies found!")
            open('alive_proxies.txt', 'w').close()

if __name__ == "__main__":
    checker = ProxyChecker(timeout=8, max_workers=30)
    checker.run()