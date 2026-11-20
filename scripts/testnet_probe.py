#!/usr/bin/env python3
"""Read-only Binance Spot Testnet probe. Never places orders."""
import argparse,hashlib,hmac,json,os,time,urllib.parse,urllib.request,urllib.error
BASE='https://testnet.binance.vision'
def request(path,params=None,signed=False):
    if path not in ('/api/v3/ping','/api/v3/time','/api/v3/exchangeInfo','/api/v3/account'): raise ValueError('Endpoint not allowed')
    p=dict(params or {})
    key=os.getenv('TESTNET_API_KEY'); secret=os.getenv('TESTNET_API_SECRET')
    if signed:
        if not key or not secret: raise ValueError('Missing Testnet credentials')
        p.update(timestamp=int(time.time()*1000),recvWindow=5000)
    q=urllib.parse.urlencode(p)
    if signed:q+='&signature='+hmac.new(secret.encode(),q.encode(),hashlib.sha256).hexdigest()
    headers={'User-Agent':'gahenax-testnet-probe/0.3'}
    if signed:headers['X-MBX-APIKEY']=key
    req=urllib.request.Request(BASE+path+('?' + q if q else ''),headers=headers,method='GET')
    with urllib.request.urlopen(req,timeout=12) as response:return json.load(response)
def main():
    a=argparse.ArgumentParser();a.add_argument('--account',action='store_true');args=a.parse_args()
    checks=[('/api/v3/ping',False),('/api/v3/time',False),('/api/v3/exchangeInfo',False)]
    if args.account:checks.append(('/api/v3/account',True))
    results={}
    for path,signed in checks:
        try:
            params={'symbol':'BTCUSDT'} if path.endswith('exchangeInfo') else None
            data=request(path,params,signed)
            results[path]={'ok':True,'canTrade':data.get('canTrade')} if signed else {'ok':True}
        except (urllib.error.URLError,ValueError,TimeoutError,json.JSONDecodeError) as e:
            results[path]={'ok':False,'error_type':type(e).__name__,'http_status':getattr(e,'code',None)}
    print(json.dumps({'mode':'READ_ONLY','orders_sent':0,'checks':results},indent=2))
    return 0 if all(v['ok'] for v in results.values()) else 1
if __name__=='__main__':raise SystemExit(main())
