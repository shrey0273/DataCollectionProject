from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from warnings import warn
import time

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.URL = 'https://coinmarketcap.com/'
        self.driver.get(self.URL)
        self.data = {'price':[],'7d change':[],'circulating supply':[],'market cap':[],'volume':[]}
        self.page_no = 1
        self.buttons = self.driver.find_elements(By.CLASS_NAME,"chevron")
        print(len(self.buttons))
        self.next_button = self.buttons[len(self.buttons)-1]
        self.links = set()

    def removeIntro(self):
        delay = 10
        for x in range(0,3):
            
            a = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="gv-footer"]')))

            next_button = a.find_element(By.TAG_NAME,'button')
            next_button.click()
    
    def smoothScrolling(self, proportion, rate):
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, round(total_height*proportion), rate):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def toPage(self,number):
        self.driver.get(self.URL+"?page="+str(number))

    def category(self,category):
        self.page_no = 1
        nextbutton = self.driver.find_element(by = By.LINK_TEXT,value=category)
        action = ActionChains(self.driver)
        action.click(nextbutton)
        action.perform()
        self.URL = self.driver.current_url
        print(self.URL)

    def stopScraping(self):
        self.driver.quit()
    
    def collectBasicInfo(self,finalpage):
        for page in range(1,finalpage+1):
            self.toPage(page)
            if page!=1 and self.driver.current_url==self.URL:
                warn("Exceeded actual number of pages")
                finalpage = page-1
                break
            else:
                self.links.update(self.collectLinks())
        print(len(self.links))

        for link in self.links:
            pass

    def collectLinks(self):
        links = set()
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(name = 'table', attrs={'class': 'h7vnx2-2 czTsgW cmc-table'})
        locations = table.find_all(name = 'a', attrs = {'class': 'cmc-link'})

        for location in locations:
            link = location.attrs["href"]
            link_bd = link.split('/')[1:4]
            link_bd[2] = ""
            link = "/".join(link_bd)
            links.add(link)
        
        return links
        # delay = 10
        # html = self.driver.page_source
        # soup = BeautifulSoup(html, 'html.parser')
        # table = soup.find(name = 'table', attrs={'class': 'h7vnx2-2 czTsgW cmc-table'})
        # trows = table.findAll('',{})[2:]
        
        # for tr in trows:
        #     tcols = tr.find_all('td')
        #     [2,3,6,7,8,9]
        #     print(tcols[2].find('a')
        # print(len(trows))

    def doStuff(self):
        self.removeIntro()
        time.sleep(2)
        self.collectBasicInfo(5)

if __name__ == "__main__":
    MyScraper = Scraper()
    MyScraper.doStuff()
    input("")
    MyScraper.stopScraping()