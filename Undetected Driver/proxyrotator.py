import re
import urllib3
from colortext import *
from requests import get
from random import shuffle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getProxy():
    resp = get('https://free-proxy-list.net/#Get')
    proxi = re.findall(r'<tr><td>(\w+\.\w+\.\w+\.\w+)[^>].td><td>(\d+)<', resp.text)
    prox = [f"http://{proxies}:{''.join(port)}" for proxies, port in proxi]
    shuffle(prox)
    return prox

def getWorking():
    working = []
    for proxy in getProxy():
        try:
            get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, verify=False, timeout=5)
        except Exception:
            print(f'{PROXY} {proxy} - {red}Dead!{reset}')
            pass
        else:
            print(f'{PROXY} {proxy} - {green}Live!{reset}')
            working.append(proxy)
            break
    return working
