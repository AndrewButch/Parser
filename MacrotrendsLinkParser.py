# Парсинг всех ссылок с сайта https://www.macrotrends.net/stocks/stock-screener

import csv

from selenium import webdriver

#driver = webdriver.Firefox('geckodriver')
#driver.get("http://www.google.com")

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def write_csv(data):
    with open("ListMacrotrends.csv", "a", newline="") as f:
        writer = csv.writer(f, delimiter=',')
        for line in data:
            #print(line)
            writer.writerow([line]) #КОРТЕЖ!!!!! КВАДРАТНЫЕ СКОБКИ


opts = Options()
opts.headless = True
assert opts.headless  # без графического интерфейса.

browser = Firefox(options=opts)
browser.get('https://www.macrotrends.net/stocks/stock-screener')
page = 0
links_cpy = []
while True:
    links = []

    i = 0
    while i < 20:
        id = "row" + str(i) + "jqxGrid"     # id = "row+i+jqxGrid"

        try:
            row = browser.find_element_by_id(id)
            a = row.find_element_by_tag_name("a")   #находим ссылку
            href = a.get_attribute("href")          #Получаем адрес
            links.append(href)
            i = i+1
        except:
            break;

    try:
        if links_cpy == links and page != 0:
            break
        print(page, " ", links)
        write_csv(links)
        links_cpy = links[:]
        pager = browser.find_element_by_id("pagerjqxGrid")
        next_button = pager.find_element_by_class_name("jqx-icon-arrow-right")
        next_button.click()
        page = page + 1
    except:
        break

browser.close()
quit()

