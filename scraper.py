from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from warnings import warn
from uuid import uuid4
import time, json, os

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.URL = 'https://coinmarketcap.com/'
        self.driver.get(self.URL)
        self.data = {'id':[],'uuid':[],'name':[],'icon':[],'rank':[],'24h £ range':[],'market cap':[]}
        self.page_no = 1
        self.links = set()

    def removeIntro(self):
        delay = 10
        # for x in range(0,3):
        a = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="gv-footer"]')))

        next_button = a.find_element(By.TAG_NAME,'button')
        next_button.click()


    def smoothScrolling(self, proportion, rate):
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, round(total_height*proportion), rate):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def toPage(self,number):
        self.driver.get(self.URL+"?page="+str(number))

    def toCategory(self,category):
        self.page_no = 1
        nextbutton = self.driver.find_element(by = By.LINK_TEXT,value=category)
        action = ActionChains(self.driver)
        action.click(nextbutton)
        action.perform()
        self.URL = self.driver.current_url
        print(self.URL)

    def stopScraping(self):
        self.driver.quit()
    
    def collectAllInfo(self,initialpage,finalpage,limit):
        for page in range(initialpage,finalpage+1):
            self.toPage(page)
            if page!=1 and self.driver.current_url==self.URL:
                warn("Exceeded actual number of pages")
                finalpage = page-1
                break
            else:
                self.links.update(self.collectPageLinks())
        print('it is',len(self.links))

        for count,link in enumerate(self.links):
            if count>limit:
                break
            self.driver.get(self.URL+link)
            self.collectCryptoInfo()
    
    def collectCryptoInfo(self): 
        ##collect from a particular crypto's page
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        name_location = soup.find(name = 'h2', attrs = {'class':'sc-1q9q90x-0 jCInrl h1'})
        name = name_location.text
        self.data['name'].append(name)

        id = name_location.findChild().text
        self.data['id'].append(id.lower())

        icon_location = soup.find(name = 'div', attrs = {'class':'sc-16r8icm-0 gpRPnR nameHeader'})
        icon = icon_location.find(name = 'img')['src']
        self.data['icon'].append(icon)

        rank = int(soup.find(name = 'div', attrs = {'class':'namePill namePillPrimary'}).text[6:]) #ignores word "rank "
        self.data['rank'].append(rank)

        price_locations = soup.find(name = 'div', attrs = {'class':'sc-16r8icm-0 kjciSH sliderSection'}).find_all(name = 'span',attrs = {'class':'n78udj-5 dBJPYV'})
        price_range = []
        for location in price_locations:
            price_range.append(location.findChild(name = 'span').text)
        self.data['24h £ range'].append(tuple(price_range))

        marketcap_location = soup.find(name = 'div', attrs = {'class':'statsBlock'}).find(name = 'div', attrs = {'class':'statsValue'})
        self.data['market cap'].append(marketcap_location.text)

        self.data['uuid'].append(uuid4())

    def collectPageLinks(self): 
        ##data hasn't loaded for all cryptos, so quickest route is to just collect links
        links = set()
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(name = 'table', attrs={'class': 'h7vnx2-2 czTsgW cmc-table'})
        locations = table.find_all(name = 'a', attrs = {'class': 'cmc-link'})

        for location in locations:
            link = location.attrs["href"]
            link_bd = link.split('/')[1:4] #we're only looking for direct children of the category
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
        
        print("Coming!")
        time.sleep(2)
        self.collectAllInfo(1,1,10)

if __name__ == "__main__":

    root_dir = os.path.abspath(os.curdir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir+"/raw_data")
    
    MyScraper = Scraper()
    MyScraper.doStuff()
    input("")
    MyScraper.stopScraping()

    for i,crypto in enumerate(MyScraper.data['id']):
        current_dir = os.path.join(root_dir,"raw_data",crypto)
        if not os.path.exists(current_dir):
            os.mkdir(current_dir)
        file = os.path.join(current_dir,'data.json')
        with open(file,'w') as f:
            json.dump({
                'id':crypto,
                'uuid':str(MyScraper.data['uuid'][i]),
                'name':MyScraper.data['name'][i],
                'icon':MyScraper.data['icon'][i],
                'rank':MyScraper.data['rank'][i],
                '24h £ range':MyScraper.data['24h £ range'][i],
                'market cap':MyScraper.data['market cap'][i]
            }, f)