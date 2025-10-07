#!/usr/bin/env python3
import os
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def build_proxy_pac():
    proxy_file = 'alive_proxies.txt'
    template_file = 'proxy.pac.template'
    output_file = 'proxy.pac'
    
    try:
        if not os.path.exists(proxy_file):
            logging.warning(f"{proxy_file} not found. Creating basic PAC file.")
            proxies = []
        else:
            with open(proxy_file, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            
            proxies = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if line.startswith(('http://', 'https://')):
                    host = line.split('://', 1)[1]
                    proxies.append(f'PROXY {host}')
                elif line.startswith('socks5://'):
                    host = line.split('://', 1)[1]
                    proxies.append(f'SOCKS5 {host}')
                else:
                    proxies.append(f'PROXY {line}')
        
        if proxies:
            proxy_string = '|'.join(proxies)
            hexed = proxy_string.encode('utf-8').hex()
        else:
            hexed = ""
        
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('HEXLIST_HERE', hexed)
            content = content.replace('TIMESTAMP_HERE', datetime.now().isoformat())
            content = content.replace('PROXY_COUNT_HERE', str(len(proxies)))
        else:
            content = f'''function FindProxyForURL(url, host) {{
    var proxies = "{hexed}";
    
    if (proxies) {{
        var proxyList = hexToString(proxies).split('|');
        if (proxyList.length > 0) {{
            return proxyList[0];
        }}
    }}
    
    return "DIRECT";
}}

function hexToString(hex) {{
    var str = '';
    for (var i = 0; i < hex.length; i += 2) {{
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }}
    return str;
}}'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logging.info(f"✓ {output_file} created with {len(proxies)} proxies")
        return True
        
    except Exception as e:
        logging.error(f"Error building PAC file: {e}")
        return False

if __name__ == "__main__":
    success = build_proxy_pac()
    sys.exit(0 if success else 1)