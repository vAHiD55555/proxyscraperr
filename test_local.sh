#!/bin/bash

echo "🔍 Testing proxy scraper locally..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo "🌐 Testing proxy checker..."
python3 proxy_check.py

if [ -f "alive_proxies.txt" ]; then
    proxy_count=$(wc -l < alive_proxies.txt)
    echo "✅ Found $proxy_count working proxies"
else
    echo "❌ No alive_proxies.txt generated"
    exit 1
fi

echo "📄 Building PAC file..."
python3 build_proxy_pac.py

if [ -f "proxy.pac" ]; then
    echo "✅ proxy.pac generated successfully"
    echo "📊 File size: $(du -h proxy.pac | cut -f1)"
else
    echo "❌ proxy.pac not generated"
    exit 1
fi

echo "🎉 All tests passed!"