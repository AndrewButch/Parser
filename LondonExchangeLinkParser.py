# https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?&page=1

# 1. зайти на ссылку
# 2. спарсить 20 строк ссылок
# 2. перейти на другую страницу


import requests, csv
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_html(url):
    r = requests.get(url)  #объект Response
    return r.text           #return html code of page URL

def write_csv(data):
    with open("assets\ListLondonExchange.csv", "a", newline="") as f:
        writer = csv.writer(f, delimiter=',')
        for line in data:
            #print(line)
            writer.writerow([line]) #КОРТЕЖ!!!!! КВАДРАТНЫЕ СКОБКИ

def get_link_from_page(url):
    try:
        html = get_html(url)
    except:
        return " "
    soup = BeautifulSoup(html, "lxml")
    links = []
    try:
        trs = soup.find("tbody").find_all("tr")
        for tr in trs:
            a = tr.find("a").get("href")
            a = "https://www.londonstockexchange.com" + a
            links.append(a)
    except:
        return " "
    return links


def main():
    # URL без номера страницы

    url = "https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?&page="
    PAGES = 1232
    for page in range(1, 1232):
        url_page = url + str(page)
        links = get_link_from_page(url_page)
        write_csv(links)
        print(page, " ", links)




#-----START---------
if __name__ == '__main__':
    main()