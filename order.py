'''
    This script will use Selenium to open up Barbora's site and check
    if there are any timeslots available.

    Notification possible via Slack as well as email.

    config.py should contain these:
        Barbora Credentials
        credentials():
            returns {"user": "",
                     "pass": ""}

        slack_settings():
            returns {
                "token": "",
                "barbora": "channel_id",
                "general": "channel_id"
            }

        https://myaccount.google.com/apppasswords
        gmail_smtp():
            returns {
                "from": "email@address",
                "hostname": "smtp.gmail.com",
                "port": 587,
                "user": ""
                "pass": ""
            }

        recipients():
            dict of lists with regions as keys

    TODO: automatically confirm order.
'''
import os
import time
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import credentials, recipients
from slackbot import send_message
from gmail import send_email

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
file_name = "{}.log".format(os.path.realpath(__file__))
handler = logging.FileHandler("{}".format(file_name), 'w')
formatter = logging.Formatter(u'%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def handleError(self, record):
    traceback.print_stack()


logger.handleError = handleError

NOTIFY = False
DEBUG = False
# CHROME DRIVER LOCATION ON COMPUTER
CHROME_DRIVERS = os.path.join(os.path.abspath(os.sep), "chromedrivers")
CHROME_DRIVERS = "/mnt/c/chromedrivers"


def init_driver():
    options = Options()
    if not DEBUG:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    for file in os.listdir(CHROME_DRIVERS):
        try:
            chrome_driver = os.path.join(CHROME_DRIVERS, file)
            driver = webdriver.Chrome(options=options,
                                      executable_path=chrome_driver)
            driver.set_window_size(1920, 1080)
            return driver
        except Exception:
            continue


def log_into_barbora(driver, region="vilnius", url="https://www.barbora.lt"):
    creds = credentials()
    driver.get(url)
    if "www" in url:
        region = f'//*[@data-county="{region}"]'
        driver.find_element_by_xpath(region).click()
        driver.find_element_by_class_name("link-to-page-btn").click()
    while True:
        try:
            login_xpath = "b-login-register--login"
            driver.find_element_by_class_name(login_xpath).click()
            user_xpath = "b-login-email"
            driver.find_element_by_id(user_xpath).send_keys(creds["user"])
            pass_xpath = "b-login-password"
            driver.find_element_by_id(pass_xpath).send_keys(creds["pass"])
            login = "/html/body/div[5]/div/div/div[2]/div/div[1]\
                     /form/div[4]/div/button"
            driver.find_element_by_xpath(login).click()
            time.sleep(3)
            try:
                adx = "/html/body/div[4]/div/div[1]/div/div/div[1]/h1/button"
                driver.find_element_by_xpath(adx).click()
            except Exception:
                pass
            return driver
        except Exception:
            continue


body = '''
Sveiki,
\n\n
{} Barboroj yra laisvų laikų: https://www.barbora.lt
\n\n
Viso geriausio!
'''

if __name__ == "__main__":
    recipients = recipients()
    kilm = {
        "vilnius": "Vilniaus",
        "kaunas": "Kauno"
    }
    for region in ["vilnius", "kaunas"]:
        driver = init_driver()
        driver = log_into_barbora(driver, region)
        time.sleep(2)
        reserve = "/html/body/div[2]/div/div/div[2]/div[1]/div[2]/div[2]\
                   /div[1]/div/div/div[1]/button[2]"
        driver.find_element_by_xpath(reserve).click()
        time.sleep(2)
        as_xpath = "b-deliverytime--slot-available"
        available_slots = driver.find_elements_by_class_name(as_xpath)
        city = region.capitalize()
        if len(available_slots) > 0:
            message = f"Barbora timeslots are available for {city}!"
            send_message(message, "barbora")
            if NOTIFY:
                send_email(recipients[region],
                           "Barboros apdeitas",
                           body.format(kilm[region]))
        else:
            logger.info(f"No timeslots available for {city}")
        driver.quit()
