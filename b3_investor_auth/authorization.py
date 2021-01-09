#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import platform

# selenium libraries
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

# recaptcha libraries
import speech_recognition as sr
import urllib
import pydub

# project libraries
from . import delay, wait_for_tag, wait_for_id
from .constants import ROOT, LOGIN, LOGOUT, TIMEOUT_SECONDS

SOUND_FOLDER = os.getcwd()+'\\' if (platform.system() == 'Windows') else os.getcwd()+'/'
LANG_EN = 'en-EN'


class Authorization:
    def __init__(self, path_chrome_driver, lang=LANG_EN, headless=True):
        try:
            # create chrome driver
            op = webdriver.ChromeOptions()
            if headless :
                op.add_argument('--headless')
                op.add_argument('--disable-gpu')
                op.add_argument('--no-sandbox')
            op.add_argument('--lang='+LANG_EN)
            op.add_argument('--incognito')
            self.driver = webdriver.Chrome(executable_path=path_chrome_driver, options=op)
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
        self.driver.get(LOGIN)
        wait_for_tag(driver=self.driver, tag_name='form', seconds=TIMEOUT_SECONDS)

        # complete login fields
        login = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtLogin')
        login.clear()
        login.send_keys(user)
        login = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtSenha')
        login.clear()
        login.send_keys(pwd)

        # switch to recaptcha frame
        frames = self.driver.find_elements_by_tag_name('iframe')
        self.driver.switch_to.frame(frames[0])
        # solve recaptcha
        self.recaptcha_solver()
        delay(10)
        # login
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnLogar').click()
        wait_for_id(driver=self.driver, id='ctl00_lblNome', seconds=TIMEOUT_SECONDS)
        return self.driver

    def recaptcha_solver(self):
        # click on checkbox to activate recaptcha
        self.driver.find_element_by_class_name('recaptcha-checkbox-border').click()
        delay()
        # switch to recaptcha audio control frame
        self.driver.switch_to.default_content()
        xpath = self.driver.find_element_by_xpath('/html/body/div/div[4]')
        frames = xpath.find_elements_by_tag_name('iframe')
        self.driver.switch_to.frame(frames[0])
        delay()
        # click on audio challenge
        self.driver.find_element_by_id('recaptcha-audio-button').click()
        # switch to recaptcha audio challenge frame
        self.driver.switch_to.default_content()
        frames = self.driver.find_elements_by_tag_name('iframe')
        self.driver.switch_to.frame(frames[-1])
        # play captcha, download mp3, translate audio to text and verify
        self.download_translate_captcha()

    def download_translate_captcha(self):
        while True:
            delay()
            # click on the play button
            try:
                self.driver.find_element_by_xpath('/html/body/div/div/div[3]/div/button').click()
            except Exception as e:
                break
            # get the mp3 audio file
            src = self.driver.find_element_by_id('audio-source').get_attribute('src')
            delay()
            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, SOUND_FOLDER + 'sample.mp3')
            delay()
            sound = pydub.AudioSegment.from_mp3(SOUND_FOLDER + 'sample.mp3')
            sound.export(SOUND_FOLDER + 'sample.wav', format='wav')
            sample_audio = sr.AudioFile(SOUND_FOLDER + 'sample.wav')
            r = sr.Recognizer()

            with sample_audio as source:
                audio = r.record(source)

            try:
                # translate audio to text with google voice recognition
                key = r.recognize_google(audio, language=LANG_EN)
                print('[INFO] Recaptcha Passcode: %s' % key)
            except Exception as err:
                raise Exception('[ERROR] {}'.format(err.args[0]))

            # key in results and submit
            self.driver.find_element_by_id('audio-response').send_keys(key.lower())
            delay()
            try:
                verify = self.driver.find_element_by_id('recaptcha-verify-button')
                verify.click()
            except Exception as e:
                print('[WARN] {}'.format(e.args[0]))

        self.driver.switch_to.default_content()
        try:
            os.remove(SOUND_FOLDER + 'sample.mp3')
            os.remove(SOUND_FOLDER + 'sample.wav')
        except Exception as e:
            print('[WARN] {}'.format(e.args[0]))

    def logout(self):
        self.driver.get(LOGOUT)