# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

# needed for splunk stuff
from splunktransactions import Transaction

class Wunderground(unittest.TestCase):
    def setUp(self):
        # needed to allow kerberos settings
        fp = webdriver.FirefoxProfile()
        fp.set_preference( "browser.download.folderList", 2 )

        lf = open('/tmp/selenium.log', 'w')
        fb = webdriver.firefox.firefox_binary.FirefoxBinary( log_file=lf )

        # shuts up annoying message at end that gets output as stderr
        unittest.TextTestRunner( verbosity = 0 )

        self.driver = webdriver.Firefox( firefox_binary=fb, firefox_profile=fp )
        self.driver.implicitly_wait(30)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.wunderground.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

        # needed for splunk stuff
        self.trans=Transaction(self.driver, 'wunderground')


    def test_wunderground(self):
        try:
            self.trans.TransactionStart(self.driver, 'stamford-ziptest')

            driver = self.driver
            driver.get(self.base_url + "/")
            driver.find_element_by_id("hpSearch").click()
            driver.find_element_by_id("hpSearch").clear()
            driver.find_element_by_id("hpSearch").send_keys("06907")
            driver.find_element_by_css_selector("button.button.postfix").click()
            driver.find_element_by_id("ui-id-2").click()
            driver.find_element_by_id("station-select-button").click()
            driver.find_element_by_link_text("Birch Road, Norwalk, CT (KCTNORWA17)").click()
            driver.find_element_by_xpath("//div[@id='location']/h1/i").click()
            driver.find_element_by_id("LayerSatellite_radio").click()
            driver.find_element_by_id("LayerWebcams_radio").click()
            driver.find_element_by_id("LayerRadarAnimGif_radio").click()

            self.trans.TransactionEnd(self.driver, 'stamford-ziptest')
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
