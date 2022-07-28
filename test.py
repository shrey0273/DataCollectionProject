import requests
from bs4 import BeautifulSoup
page = requests.get('https://en.wikipedia.org/wiki/Python_(programming_language)')
html = page.text # Get the content of the webpage
soup = BeautifulSoup(html, 'html.parser') # Convert that into a BeautifulSoup object that contains methods to make the tag searcg easier
#print(soup.prettify())
method = soup.find(name = 'span', attrs={'id': 'Methods', 'class': 'mw-headline'})
method2 = method.find_next()
print(method2)

# from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option("excludeSwitches",["enable-automation"])

# driver_path = '/Users/myuser/Downloads/chromedriver'
# driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
# driver.get('https://google.com')

# driver.close()