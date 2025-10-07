# encode_proxies.py
# Reads alive_proxies.txt and prints the hex string suitable for proxy.pac.template
lines = open('alive_proxies.txt','r',encoding='utf-8').read().splitlines()
out=[]
for L in lines:
    L=L.strip()
    if not L: continue
    if L.startswith('http://') or L.startswith('https://'):
        host = L.split('://',1)[1]
        out.append('PROXY '+host)
    elif L.startswith('socks5://'):
        host = L.split('://',1)[1]
        out.append('SOCKS5 '+host)
    else:
        out.append(L)
s='|'.join(out)
print(s.encode('utf-8').hex())
