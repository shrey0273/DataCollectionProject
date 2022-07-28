from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://coinmarketcap.com/')
        
    
    def removeIntro(self):
        for x in range(0,3):
            time.sleep(2)
            a = self.driver.find_element(by = By.XPATH, value = '//*[@class="sc-8ukhc-0 ljgYka"]')
            b = a.find_element(by = By.XPATH, value = './/*[@class="gv-footer"]')
            next_button = b.find_element(By.TAG_NAME,'button')
            next_button.click()
            
    def stopScraping(self):
        self.driver.quit()

MyScraper = Scraper()
MyScraper.removeIntro()
MyScraper.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
input("")
MyScraper.stopScraping()