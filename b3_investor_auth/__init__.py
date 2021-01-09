import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def delay(seconds=0):
    if seconds == 0:
        seconds = 4
    time.sleep(seconds)


def wait_for_tag(driver, tag_name, seconds):
    w = WebDriverWait(driver=driver, timeout=seconds)
    tag = EC.presence_of_all_elements_located((By.TAG_NAME, tag_name))
    w.until(tag, message='[ERROR] expected tag {}'.format(tag_name))


def wait_for_id(driver, id, seconds):
    w = WebDriverWait(driver=driver, timeout=seconds)
    tag = EC.presence_of_element_located((By.ID, id))
    w.until(tag, message='[ERROR] expected component id {}'.format(id))
