import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import csv
import time

'''Selenium Code'''
driver = webdriver.Chrome(executable_path= "C:/chromedriver.exe")
driver.implicitly_wait(5)
driver.maximize_window()
driver.get("https://affiliate-program.amazon.com/")
driver.find_element_by_link_text("Sign in").click()
driver.find_element_by_id("ap_email").send_keys("gunturu.lali@gmail.com")
driver.find_element_by_id("ap_password").send_keys("saipatham999")
driver.find_element_by_id("signInSubmit").click()
act_chains = ActionChains(driver)
promotion = driver.find_element_by_link_text("Promotions")
act_chains.move_to_element(promotion).perform()
promo_codes = driver.find_element_by_xpath("//a[@title='Amazon Promo Codes']")
promo_codes.click()


''' Calculating Time'''
start = time.time()


''' Scrolling code'''
number_of_scroll = 250

while number_of_scroll > 0:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    number_of_scroll = number_of_scroll-1


'''' Beautiful Soup Code'''
content = driver.page_source
soup = BeautifulSoup(content,'lxml')
search_data = []  # list to store extracted data
table = soup.find('div', attrs={'class': 'search-result-body'})
for row in table.findAll('div',attrs={'class': 'promo-desc'}):
    data = {}
    temp_list = row.a.text
    str_list = str(temp_list)
    match = re.compile(r'promo code \w+')

    str_promo = match.findall(str_list)
    str_promo = [str(i) for i in str_promo]
    s = ','.join(str_promo)
    s.replace('promo code', '')

    replace_str = s.replace('promo code', '')
    data['promo_code'] = replace_str.strip()

    data['url'] = row.a['href']
    search_data.append(data)


''' Writing Data to csv file'''

filename = 'scraped_data.csv'
with open(filename, 'w',  newline='') as f:
    w = csv.DictWriter(f, ['promo_code', 'url'])
    w.writeheader()
    for quote in search_data:
        w.writerow(quote)

print(f'Time: {(time.time() - start)/60}')
