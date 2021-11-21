from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import *
from .utils import convert_response


class SeleniumTest(TestCase):
    def setUp(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.url =  "http://www.skdue.site/"
        self.username = "pat"
        self.password = "patpat123"

    def test_login(self):
        self.browser = webdriver.Chrome('skdue_calendar/api/v2/tests/chromedriver',options=self.chrome_options)
        self.browser.get(self.url)
        input_class= 'register-input'
        input_field = self.browser.find_elements_by_class_name(input_class)
        input_field[3].send_keys(self.username)
        input_field[4].send_keys(self.password)
        input_field[4].send_keys(Keys.RETURN)
        self.browser.implicitly_wait(15)
        #home button
        SKDUE = 'user-detail-app-button'
        b_field = self.browser.find_elements_by_class_name(SKDUE)
        self.assertEqual('Skdue',b_field[0].text)
        #username
        USER = 'user-detail-login'
        n_field = self.browser.find_elements_by_class_name(USER)
        self.assertEqual(self.username,n_field[0].text)

    def test_search(self):
        self.browser = webdriver.Chrome('skdue_calendar/api/v2/tests/chromedriver',options=self.chrome_options)
        self.browser.get(self.url)
        input_class= 'register-input'
        input_field = self.browser.find_elements_by_class_name(input_class)
        input_field[3].send_keys(self.username)
        input_field[4].send_keys(self.password)
        input_field[4].send_keys(Keys.RETURN)
        self.browser.implicitly_wait(15)

        SEARCH = 'dropdown-input'
        s_field = self.browser.find_elements_by_class_name(SEARCH)
        s_field[0].send_keys("pun")
        DROP = 'dropdown-item'
        d_field = self.browser.find_elements_by_class_name(DROP)
        self.assertIn('pun', d_field[11].text)
        self.assertIn('Calendars', d_field[11].text)

        d_field[11].click()
        fm = 'follow-main'
        fm_field = self.browser.find_elements_by_class_name(fm)
        self.assertIn('pun', fm_field[0].text)

    def test_follow_button(self):
        self.browser = webdriver.Chrome('skdue_calendar/api/v2/tests/chromedriver',options=self.chrome_options)
        self.browser.get(self.url)
        input_class= 'register-input'
        input_field = self.browser.find_elements_by_class_name(input_class)
        input_field[3].send_keys(self.username)
        input_field[4].send_keys(self.password)
        input_field[4].send_keys(Keys.RETURN)
        self.browser.implicitly_wait(15)
        #go to other calendar
        SEARCH = 'dropdown-input'
        s_field = self.browser.find_elements_by_class_name(SEARCH)
        s_field[0].send_keys("pun")
        DROP = 'dropdown-item'
        d_field = self.browser.find_elements_by_class_name(DROP)
        d_field[11].click()
        #before follow
        fb = 'follow-button'
        fm_field = self.browser.find_elements_by_class_name(fb)
        self.assertIn('follow', str(fm_field[0].text).lower())
        fm_field[0].click()
        #after follow
        after_fm_field = self.browser.find_elements_by_class_name(fb)
        self.assertIn('unfollow', str(after_fm_field[0].text).lower())

    # def test_create_event(self):
    #     #login
    #     self.browser = webdriver.Chrome('/Users/patkamon/Downloads/chromedriver')
    #     self.browser.get(self.url)
    #     input_class= 'register-input'
    #     input_field = self.browser.find_elements_by_class_name(input_class)
    #     input_field[3].send_keys(self.username)
    #     input_field[4].send_keys(self.password)
    #     input_field[4].send_keys(Keys.RETURN)
    #     self.browser.implicitly_wait(15)
    #     #event-create
    #     EC = 'event-create'
    #     e_field = self.browser.find_elements_by_class_name(EC)
    #     self.assertIn('+',e_field[0].text)
    #     e_field[0].click()
    #     #fill info
    #
