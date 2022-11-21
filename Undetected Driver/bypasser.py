import os
from time import sleep
from proxyrotator import *
from audiototext import audioText

from getdriver import getChromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as poel
os.system('cls')


def main(url:str, chkIPUA=False):
    wait = WebDriverWait(browser, 10)

    #! Check IP And UserAgent
    if chkIPUA:
        chkIPUA = 'https://www.willmaster.com/blog/tips/ip-address.php'
        browser.get(chkIPUA)
        sleep(10)
        exit()

    #! NOW START TESTING
    try:
        browser.get(url)
        sleep(5)
    except Exception as exc:
        print(f'{WARNING} {exc}')
    else:
        if 'iframe' in browser.page_source:
            try:
                aFrame = browser.find_element(By.TAG_NAME, 'iframe')
                anc = aFrame.get_attribute('src')
                print(f'{INFO} {purple}Anchor URL{reset} {red}>{reset} {anc}')
                browser.switch_to.frame(aFrame)
                sleep(3)
            except Exception as exc:
                print(f'{WARNING} {exc}')
                browser.close()
            else:
                try:
                    check_box = wait.until(poel((By.CSS_SELECTOR ,"#recaptcha-anchor")))
                    check_box.click()
                    browser.switch_to.default_content()
                    sleep(3)
                except Exception as exc:
                    print(f'{WARNING} {exc}')
                else:
                    try:
                        bFrame = browser.find_elements(By.TAG_NAME, 'iframe')[2]
                        bfr = bFrame.get_attribute('src')
                        print(f'{INFO} {purple}Bframe URL{reset} {red}>{reset} {bfr}')
                        browser.switch_to.frame(bFrame)
                        sleep(3)
                    except Exception as exc:
                        print(f'{WARNING} {exc}')
                    else:
                        try:
                            audio = wait.until(poel((By.CSS_SELECTOR, '#recaptcha-audio-button')))
                            audio.click()
                            browser.switch_to.default_content()
                            sleep(3)
                        except Exception as exc:
                            print(f'{WARNING} {exc}')
                        else:
                            try:
                                browser.switch_to.frame(browser.find_elements(By.TAG_NAME, 'iframe')[2])
                                download = wait.until(poel((By.CSS_SELECTOR,'.rc-audiochallenge-tdownload-link')))
                                getLink = download.get_attribute('href')
                                print(f'{INFO} {purple}Audio URL{reset} {red}>{reset} {getLink}')
                                sleep(3)
                            except Exception as exc:
                                print(f'{WARNING} {exc}')
                            else:
                                try:
                                    phraseText = audioText(getLink)
                                except Exception as exc:
                                    print(f'{WARNING} {exc}')
                                else:
                                    try:
                                        result = wait.until(poel((By.CSS_SELECTOR,'#audio-response')))
                                        result.send_keys(phraseText, Keys.ENTER)
                                        browser.switch_to.default_content()
                                        sleep(3)
                                        os.remove(f'{os.getcwd()}\\audio.mp3')
                                        os.remove(f'{os.getcwd()}\\audio.wav')
                                    except Exception as exc:
                                        print(f'{WARNING} {exc}')
                                    else:
                                        submit = wait.until(poel((By.CSS_SELECTOR,'#recaptcha-demo-submit')))
                                        submit.click()
                                        sleep(2)
                                        print(f'\n{SUCCESS} {white}Hooray V2 Bypassed! 📍{reset}\n')

if __name__ == '__main__':

    url = 'https://www.google.com/recaptcha/api2/demo'

    #! If you want to use Proxy or HeadLess. Set it True :))
    browser = getChromedriver(use_proxy=False, user_agent=True, headless=False)

    #! Please set url=None and chkIPUA=True if you want to check IP and UserAgent Only
    #!==> Else set url=url and chkIPUA=False if you want to Start Bypassing :))
    main(url=None, chkIPUA=True)
