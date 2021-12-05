#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# selenium libraries
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

# project libraries
from . import delay, wait_for_tag, wait_for_id
from .constants import ROOT, LOGOUT, TIMEOUT_SECONDS

LANG_EN = 'en-EN'

class Authentication:
    
    def __init__(self, driverChrome, lang=LANG_EN, headless=False):
        try:
            # create chrome driver
            op = webdriver.ChromeOptions()
            if headless :
                op.add_argument('--headless')
                op.add_argument('--disable-gpu')
                op.add_argument('--no-sandbox')
            op.add_argument('--lang='+LANG_EN)
            op.add_argument('--incognito')
            self.driver = webdriver.Chrome(executable_path=driverChrome, options=op)
            # go to website
            self.driver.get(ROOT)
            wait_for_tag(driver=self.driver, tag_name='form', seconds=TIMEOUT_SECONDS)
        except TimeoutException as tim:
            raise TimeoutException('[ERROR] {}'.format(tim.args[0]))
        except WebDriverException as wdr:
            raise WebDriverException('[ERROR] {}'.format(wdr.args[0]))
        except Exception as err:
            raise Exception('[ERROR] {}'.format(err.args[0]))

    def login(self, user, pwd):
        # go to login page
        delay(40)
        # complete login fields
        wait_for_id(driver=self.driver, id='extension_DocInput', seconds=TIMEOUT_SECONDS)
        login = self.driver.find_element_by_id('extension_DocInput')
        #login.clear()
        login.send_keys(user)

        wait_for_id(driver=self.driver, id='continue', seconds=TIMEOUT_SECONDS)
        wizard_1 = self.driver.find_element_by_id('continue')
        wizard_1.click()

        wait_for_id(driver=self.driver, id='password', seconds=TIMEOUT_SECONDS)
        login = self.driver.find_element_by_id('password')
        #login.clear()
        login.send_keys(pwd)

        # switch to recaptcha frame
        frames = self.driver.find_elements_by_tag_name('iframe')
        self.driver.switch_to.frame(frames[0])
        
        # solve recaptcha
        # click on checkbox to activate recaptcha
        self.driver.find_element_by_class_name('recaptcha-checkbox-border').click()
        delay(40)
        self.driver.switch_to.default_content()
        # login
        self.driver.find_element_by_id('continue').click()
        wait_for_id(driver=self.driver, id='right-sidenav', seconds=TIMEOUT_SECONDS)
        payload = {}
        payload['token'] = self.driver.execute_script("return sessionStorage.getItem('token');")
        payload['cache-guid'] = self.driver.execute_script("return sessionStorage.getItem('cache-guid');")

        return payload

    def logout(self):
        self.driver.get(LOGOUT)
