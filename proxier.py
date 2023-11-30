import re
from concurrent.futures import ThreadPoolExecutor
from random import choice, shuffle
from threading import Event, Lock

import requests

from colorize import Colors


class Proxier:
    PROXY_URL = 'https://free-proxy-list.net/'
    CHECK_URL = 'https://www.bing.com'
    MAX_WORKERS = 50
    TIMEOUT = 10

    def __init__(self):
        self.session = requests.Session()
        self.live_proxies = set()
        self.lock = Lock()
        self.event = Event()
        self._start_checking()

    def __del__(self):
        self.session.close()

    @property
    def live_proxy(self):
        if self.live_proxies:
            return choice(list(self.live_proxies))
        exit(f'{Colors.FAILED} No Live Proxy found!')

    @staticmethod
    def _search_proxies(response):
        pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b')
        return [f'http://{proxy}' for proxy in pattern.findall(response.text)]

    def fetch_proxies(self):
        try:
            response = self.session.get(self.PROXY_URL)
            response.raise_for_status()
            proxies = self._search_proxies(response)
            shuffle(proxies)
            return list(set(proxies))
        except Exception as exc:
            print(Colors.FAILED, str(exc))

    def _check_proxy(self, proxy: str):
        if self.event.is_set():
            return
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = self.session.get(self.CHECK_URL, proxies=proxies, timeout=self.TIMEOUT)
            if 200 <= response.status_code <= 299:
                with self.lock:
                    print(f'{Colors.PROXY} {proxy} - {Colors.green}Live!{Colors.reset}')
                    self.live_proxies.add(proxy)
                    self.event.set()
                    return proxy

        except requests.RequestException:
            with self.lock:
                if not self.event.is_set():
                    print(f'{Colors.PROXY} {proxy} - {Colors.red}Dead!{Colors.reset}')

    def _start_checking(self):
        proxies = self.fetch_proxies()
        if proxies:
            print(f'\n📍 Scraped {Colors.yellow}{len(proxies)}{Colors.reset} Proxies\n')
            with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                for proxy in proxies:
                    executor.submit(self._check_proxy, proxy)
                    if self.event.is_set():
                        break