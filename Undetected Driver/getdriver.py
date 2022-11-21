from colortext import *
from random import choice
from proxyrotator import *
from user_agent import generate_user_agent as gua

import undetected_chromedriver as uc

#! Dont Change Params. Default set False
def getChromedriver(use_proxy=False, user_agent=False, headless=False):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    if use_proxy:
        print(f'\n📍 Scraped {yellow}{len(getProxy())}{reset} Proxies\n')
        chrome_options.add_argument(f'--proxy-server={choice(getWorking())}')
    if user_agent:
        chrome_options.add_argument(f'--user-agent={gua()}')
    if headless:
        chrome_options.add_argument('--headless')
    browser = uc.Chrome(options=chrome_options, use_subprocess=True)
    return browser
