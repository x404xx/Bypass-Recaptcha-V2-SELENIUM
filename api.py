import json
import os
from random import uniform
from time import sleep
from urllib.request import urlretrieve

import undetected_chromedriver as uc
from pydub import AudioSegment
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located as poel
from selenium.webdriver.support.ui import WebDriverWait
from speech_recognition import AudioFile, Recognizer
from user_agent import generate_user_agent

from colorize import Colors
from proxier import Proxier


class RecaptchaBypass:
    def __init__(self, debug=False, use_proxy=False, use_agent=False, headless=False):
        self.debug = debug
        self.browser = self._get_chromedriver(use_proxy, use_agent, headless)
        self.wait = WebDriverWait(self.browser, 10)

    def _get_chromedriver(self, use_proxy, use_agent, headless):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        if use_proxy:
            working_proxy = self._setup_proxy()
            self._print_message('\n' + Colors.INFO, f'{Colors.purple}Live Proxy {Colors.red}>{Colors.reset} {working_proxy}')
            chrome_options.add_argument(f'--proxy-server={working_proxy}')
        if use_agent:
            ua = generate_user_agent()
            self._print_message(Colors.INFO, f'{Colors.purple}User Agent {Colors.red}>{Colors.reset} {ua}')
            chrome_options.add_argument(f'--user-agent={ua}')
        if headless:
            chrome_options.add_argument('--headless')
        browser = uc.Chrome(options=chrome_options)
        browser.maximize_window()
        return browser

    def _print_message(self, level, message):
        print(f'{level} {message}')

    def _handle_exception(self, exc):
        block = self._is_block()
        if block:
            self._print_message(Colors.WARNING, f'IP has been blocked! {block.text}')
        else:
            self._print_message(Colors.FAILED, type(exc).__name__)
        self._quit_browser()

    def _quit_browser(self):
        self.browser.quit()
        self._is_debug('Browser closed!\n')

    def _setup_proxy(self):
        proxy = Proxier()
        return proxy.live_proxy

    def check_ip(self):
        """This is for checking IP only"""
        try:
            self._print_message(Colors.INFO, f'{Colors.blue}Checking IP information..{Colors.reset}')
            self.browser.get('https://ipwho.is')
            sleep(uniform(2, 3))
            pre_element = self.browser.find_element(By.TAG_NAME, 'pre')
            json_data = pre_element.text
            data_dict = json.loads(json_data)
            self._print_message(Colors.SUCCESS, f'{Colors.white}{data_dict["ip"]}{Colors.reset} ({data_dict["country"]})')
            self._quit_browser()
        except (TimeoutException, NoSuchElementException, Exception) as exc:
            self._handle_exception(exc)

    def bypass_recaptcha_v2(self, url):
        """Bypassing google recaptcha v2"""
        try:
            self._get_source(url)
            self._click_recaptcha_checkbox()
            self._click_audio_button()
            audio_url = self._get_audio_url()
            self._transcribe_audio(audio_url)
            self._click_demo_submit()
            self._quit_browser()
        except (TimeoutException, NoSuchElementException, Exception) as exc:
            self._handle_exception(exc)

    def _get_source(self, url):
        self._print_message(Colors.INFO, f'{Colors.blue}Initiating v2 bypass..{Colors.reset}')
        self.browser.get(url)
        sleep(uniform(2, 3))

    def _is_block(self):
        try:
            recaptcha_header = self.browser.find_element(By.CLASS_NAME, 'rc-doscaptcha-body-text')
            return recaptcha_header
        except NoSuchElementException:
            return None

    def _is_debug(self, message):
        if self.debug:
            self._print_message(Colors.INFO, f'{Colors.white}{message}{Colors.reset}')

    def _click_recaptcha_checkbox(self):
        self._is_debug('Getting recaptcha checkbox..')
        recaptcha_frame = self.browser.find_element(By.TAG_NAME, 'iframe')
        anchor_url = recaptcha_frame.get_attribute('src')
        self._print_message(Colors.INFO, f'{Colors.purple}Anchor URL {Colors.red}>{Colors.reset} {anchor_url}')
        self.browser.switch_to.frame(recaptcha_frame)
        check_box = self.wait.until(poel((By.CSS_SELECTOR, "#recaptcha-anchor")))
        self._is_debug('Clicking checkbox..')
        check_box.click()
        self.browser.switch_to.default_content()

    def _click_audio_button(self):
        self._is_debug('Getting recaptcha challenge..')
        captcha_challenge = self.browser.find_elements(By.TAG_NAME, 'iframe')[2]
        captcha_challenge_url = captcha_challenge.get_attribute('src')
        self._print_message(Colors.INFO, f'{Colors.purple}Bframe URL {Colors.red}>{Colors.reset} {captcha_challenge_url}')
        self.browser.switch_to.frame(captcha_challenge)
        audio_button = self.wait.until(poel((By.CSS_SELECTOR, '#recaptcha-audio-button')))
        self._is_debug('Clicking audio button..')
        audio_button.click()
        self.browser.switch_to.default_content()

    def _get_audio_url(self):
        self.browser.switch_to.frame(self.browser.find_elements(By.TAG_NAME, 'iframe')[2])
        download_button = self.wait.until(poel((By.CSS_SELECTOR, '.rc-audiochallenge-tdownload-link')))
        self._is_debug('Clicking download button..')
        audio_url = download_button.get_attribute('href')
        self._print_message(Colors.INFO, f'{Colors.purple}Audio URL {Colors.red}>{Colors.reset} {audio_url}')
        return audio_url

    def _transcribe_audio(self, audio_url):
        phrase_text, wav_output = self._audio_to_text(audio_url)
        self._print_message(Colors.INFO, f'{Colors.purple}Phrase Text {Colors.red}> {Colors.green}{phrase_text}{Colors.reset}')
        text_field = self.wait.until(poel((By.CSS_SELECTOR, '#audio-response')))
        text_field.send_keys(phrase_text, Keys.ENTER)
        self._is_debug('Entering the phrase text..')
        self.browser.switch_to.default_content()
        os.remove(wav_output)

    def _audio_to_text(self, audio_url):
        filename = 'audio.mp3'
        wav_output = 'audio.wav'
        urlretrieve(audio_url, filename)
        self._is_debug('Downloading the audio challenge..')
        AudioSegment.from_mp3(filename).export(wav_output, format='wav')
        sample_audio = AudioFile(wav_output)
        os.remove(filename)

        recognizer = Recognizer()
        with sample_audio as source:
            audio = recognizer.record(source)
        self._is_debug('Converting audio challenge to text..')
        return recognizer.recognize_google(audio), wav_output

    def _click_demo_submit(self):
        submit = self.wait.until(poel((By.CSS_SELECTOR, '#recaptcha-demo-submit')))
        self._is_debug('Clicking submit button..')
        submit.click()
        sleep(uniform(2, 3))
        if 'Hooray' in self.browser.page_source:
            self._print_message('\n' + Colors.SUCCESS, f'{Colors.white}Hooray V2 Bypassed! 📍{Colors.reset}\n')
        else:
            self._print_message('\n' + Colors.WARNING, f'{Colors.white}Bypass Failed! 📍{Colors.reset}\n')
