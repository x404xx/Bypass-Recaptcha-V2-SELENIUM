<div align='center'>

# Google Recaptcha v2 <img src='https://github.com/x404xx/Bypass-Recaptcha-V2-SELENIUM/assets/114883816/6f65b89c-3c57-465b-ad3c-87edb2efef2f' width='30px'>

**BypassV2** tool for bypassing google recaptcha v2 using `undetected-chromedriver`.

<img src='https://github.com/x404xx/Bypass-Recaptcha-V2-SELENIUM/assets/114883816/11102253-ea62-4a30-8152-b1afab96fe49' width='auto' height='auto'>

</div>

## Installation

To use _**BypassV2**_, open your terminal and navigate to the folder that contains _**BypassV2**_ content ::

```
pip install -r requirements.txt
```

## Parameters (boolean)

```
debug (For debugging information)
headless (For headless mode) - Not recommended because sometimes it will get blocked.
use_proxy (Use a proxy) - Very fast checking (Concurrent)
use_agent (Use a custom user agent)
```

## Without Proxy

```python
import os

from api import RecaptchaBypass


os.system('cls' if os.name == 'nt' else 'clear')

demo_url = 'https://www.google.com/recaptcha/api2/demo'

bypass_instance = RecaptchaBypass()
bypass_instance.bypass_recaptcha_v2(demo_url)
```

<img src='https://github.com/x404xx/Bypass-Recaptcha-V2-SELENIUM/assets/114883816/e6c9b0bd-65ed-4f22-af84-cb282310646e' width='600' height='auto'>

## Without Proxy + Debug

```python
import os

from api import RecaptchaBypass


os.system('cls' if os.name == 'nt' else 'clear')

demo_url = 'https://www.google.com/recaptcha/api2/demo'

bypass_instance = RecaptchaBypass(debug=True)
bypass_instance.bypass_recaptcha_v2(demo_url)
```

<img src='https://github.com/x404xx/Bypass-Recaptcha-V2-SELENIUM/assets/114883816/ac3118e1-d74f-4bc4-a13c-a7b8e6f7c571' width='600' height='auto'>

## Using Proxy + Bypassing

> Not all proxies are working; some of them will get blocked.

```python
import os

from api import RecaptchaBypass


os.system('cls' if os.name == 'nt' else 'clear')

demo_url = 'https://www.google.com/recaptcha/api2/demo'

bypass_instance = RecaptchaBypass(use_proxy=True)
bypass_instance.bypass_recaptcha_v2(demo_url)
```

<img src='https://github.com/x404xx/Bypass-Recaptcha-V2-SELENIUM/assets/114883816/48e7662c-3cad-4f06-a2fc-eb36f4825c9e' width='600' height='auto'>

## Using Proxy + Check IP

```python
import os

from api import RecaptchaBypass


os.system('cls' if os.name == 'nt' else 'clear')

demo_url = 'https://www.google.com/recaptcha/api2/demo'

bypass_instance = RecaptchaBypass(use_proxy=True)
bypass_instance.check_ip()
```

<img src='https://github.com/x404xx/Bypass-Recaptcha-V2-SELENIUM/assets/114883816/baf5085f-3499-47d8-8ae9-f57af13bfa95' width='600' height='auto'>

## Legal Disclaimer

> **Note**
> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**
