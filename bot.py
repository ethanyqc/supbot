from selenium import webdriver
from selenium.webdriver.support.ui import Select
from config import keys
from bs4 import BeautifulSoup
import time
import json
import requests


headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'If-None-Match': '"MnhlSMUKPPVW1gPfswixCrrWB9Y="',
}

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper


@timeme
def order():
    # add to cart
    selectSize = Select(driver.find_element_by_id('s'))

    # select size
    selectSize.select_by_visible_text('Medium')

    driver.find_element_by_name('commit').click()

    # wait for checkout
    time.sleep(.5)
    checkout_element = driver.find_element_by_class_name('checkout')
    checkout_element.click()

    # fill out infos
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys['name'])
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(keys['email'])
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys['phone_number'])
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(keys['street_address'])
    driver.find_element_by_xpath('//*[@id="oba3"]').send_keys(keys['apt_num'])
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys['zip_code'])
    # driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys['city'])
    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(keys['card_cvv'])
    driver.find_element_by_id('nnaerb').send_keys(keys['card_number'])

    selectMonth = Select(driver.find_element_by_id('credit_card_month'))
    selectMonth.select_by_value('11')
    selectDate = Select(driver.find_element_by_id('credit_card_year'))
    selectDate.select_by_value('2023')

    process_payment = driver.find_element_by_xpath('//*[@id="pay"]/input')
    process_payment.click()

s = requests.session()

#scrape for new product
def scrape():
    i = 0
    response = requests.get('http://www.supremenewyork.com/shop.json', headers=headers)
    a = json.loads(response.text)

    products = a['products_and_categories']
    urlArr = []
    print("All the new item:")
    for product in products['new']:
        pid = product['id']
        pname = product['name']
        pcategory = product['category_name']
        urlArr.append('http://www.supremenewyork.com/shop/'+str(pid))
        print(str((i)) + ": " + pname)
        print('http://www.supremenewyork.com/shop/'+str(pid))
        i = i + 1
    keyword_index = int(input("Enter item index: "))

    return urlArr[keyword_index]




if __name__ == '__main__':

    url = scrape()
    # load chrome
    driver = webdriver.Chrome('./chromedriver')
    #get product url
    driver.get(url)
    order()
