# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os

# needed for splunk stuff
from splunktransactions import Transaction


class Weather(unittest.TestCase):
    def setUp(self):
        # needed to allow kerberos settings
        fp = webdriver.FirefoxProfile()
        fp.set_preference( "browser.download.folderList", 2 )

        lf = open('/tmp/selenium.log', 'w')
        fb = webdriver.firefox.firefox_binary.FirefoxBinary( log_file=lf )

        # shuts up annoying message at end that gets output as stderr
        unittest.TextTestRunner( stream=open( os.devnull ) )

        self.driver = webdriver.Firefox( firefox_binary=fb, firefox_profile=fp )
        self.driver.implicitly_wait(30)

        self.base_url = "http://www.weather.com"
        self.verificationErrors = []
        self.accept_next_alert = True

        # needed for splunk stuff
        self.trans=Transaction(self.driver, 'weather.com')
    
    def test_stamford(self):
        try:
            driver = self.driver
            self.trans.TransactionStart(self.driver, 'weather.com-stamford-ziptest')
            driver.get(self.base_url + "/")
            driver.find_element_by_name("search").click()
            driver.find_element_by_name("search").clear()
            driver.find_element_by_name("search").send_keys("06907")

            for i in range(60):
                try:
                    if self.is_element_present(By.XPATH, "//div[@id='wx-header']/div/div/div[2]/div/div[2]/div/div/section/div/div[2]/div/div/div/div/ul/li/div/div/p"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            driver.find_element_by_css_selector("div.twc-typeahead-item-active").click()
            driver.find_element_by_xpath("//div[@id='wx-local-wrap']/div[2]/div[3]/div/div/div/div/nav/ul/li[3]/a/span").click()
            driver.find_element_by_css_selector("a.linklist-default.default > span.ng-binding").click()
            self.assertEqual('Stamford, CT Weather', driver.find_element_by_css_selector("h1.ng-binding").text)
            self.trans.TransactionEnd(self.driver, 'weather.com-stamford-ziptest')
        except Exception, e: 
            self.trans.TransactionExcept(self.driver,e)

    def test_poundridge(self):
        try:
            driver = self.driver
            self.trans.TransactionStart(self.driver, 'weather.com-poundridge-ziptest')
            driver.get(self.base_url + "/")
            driver.find_element_by_name("search").click()
            driver.find_element_by_name("search").clear()
            driver.find_element_by_name("search").send_keys("10576")

            for i in range(60):
                try:
                    if self.is_element_present(By.XPATH, "//div[@id='wx-header']/div/div/div[2]/div/div[2]/div/div/section/div/div[2]/div/div/div/div/ul/li/div/div/p"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            driver.find_element_by_css_selector("div.twc-typeahead-item-active").click()
            driver.find_element_by_xpath("//div[@id='wx-local-wrap']/div[2]/div[3]/div/div/div/div/nav/ul/li[3]/a/span").click()
            driver.find_element_by_css_selector("a.linklist-default.default > span.ng-binding").click()
            self.assertEqual("Pound Ridge, NY (10576) Weather", driver.find_element_by_css_selector("h1.ng-binding").text)
            self.trans.TransactionEnd(self.driver, 'weather.com-poundridge-ziptest')
        except Exception, e: 
            self.trans.TransactionExcept(self.driver,e)
 
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
