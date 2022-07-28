from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# el = driver.find_element(by=By.XPATH, value='//button')
def load_and_accept_cookies(URL = "https://www.zoopla.co.uk/for-sale/property/london/?q=london&search_source=home") -> webdriver.Chrome:
    driver = webdriver.Chrome()
    
    driver.get(URL)

    time.sleep(2)
    try:
        driver.switch_to.frame('gdpr-consent-notice')
        accept_cookies_button = driver.find_element(by = By.XPATH, value = '//*[@id="save"]')
        accept_cookies_button.click()
    except AttributeError:
        driver.switch_to.frame('gdpr-consent-notice')
        accept_cookies_button = driver.find_element(by = By.XPATH, value = '//*[@id="save"]')
        accept_cookies_button.click()
    except:
        pass
    return driver



def get_links(driver: webdriver.Chrome) -> list:
    prop_container = driver.find_element(By.XPATH, '//div[@class="css-1itfubx edluams0"]')
    prop_list = prop_container.find_elements(By.XPATH, './div')
    link_list = []

    for house_property in prop_list:
        a_tag = house_property.find_element(By.TAG_NAME,'a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list

big_list = []
driver = load_and_accept_cookies()

for i in range(5):
    big_list.extend(get_links(driver))
    li_tag = driver.find_element(By.XPATH,'//*[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
    a_tag = li_tag.find_element(By.TAG_NAME,'a')
    next_link = a_tag.get_attribute('href')
    print(next_link)
    time.sleep(2)
    driver = load_and_accept_cookies(next_link)


print(f'There are {len(big_list)} properties in these pages')
dict_properties = {'Price':[], 'Address':[], 'Bedrooms':[], 'Description':[]}
for link in big_list:
    time.sleep(2)
    driver.get(link)
    price = driver.find_element(By.XPATH, '//p[@data-testid="price"]').text
    address = driver.find_element(By.XPATH, '//address[@data-testid="address-label"]').text
    num_bedrooms = driver.find_element(By.XPATH, '//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
    div_tag = driver.find_element(By.XPATH, '//div[@data-testid="truncated_text_container"]')
    span_tag = div_tag.find_element(By.XPATH,'.//span')
    description = span_tag.text

    dict_properties['Price'].append(price)
    dict_properties['Address'].append(address)
    dict_properties['Bedrooms'].append(num_bedrooms)
    dict_properties['Description'].append(description)
print(dict_properties['Price'])
driver.quit()
# time.sleep(2)
# house_property = driver.find_element(by = By.XPATH,value = '//*[@id="listing_62026808"]')





