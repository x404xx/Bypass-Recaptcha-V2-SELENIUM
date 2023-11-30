import os

from api import RecaptchaBypass

if __name__ == '__main__':
    # Clearing the console screen (works on both Windows and Unix-like systems)
    os.system('cls' if os.name == 'nt' else 'clear')

    # For demonstration purposes only (no need to write it like I did)
    debug = True
    headless = False
    use_proxy = True
    use_agent = False

    # Optional: Set to True to check IP information if using a proxy
    ip_info = True

    # URL for the Recaptcha demo
    demo_url = 'https://www.google.com/recaptcha/api2/demo'

    # By default, all options are set to False; set to True directly if needed.
    bypass_instance = RecaptchaBypass(debug=debug, headless=headless, use_proxy=use_proxy, use_agent=use_agent)

    if ip_info:
        # Optional: Check IP information if using a proxy
        bypass_instance.check_ip()
    else:
        # Bypass the Recaptcha v2 on the demo URL
        bypass_instance.bypass_recaptcha_v2(demo_url)
