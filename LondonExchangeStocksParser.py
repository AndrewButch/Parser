import requests
import datetime
import csv
from bs4 import BeautifulSoup

# 1. Прочитать ссылки
# 2. Найти страничку с финансами
# 3. Прочитать нужную строку
# 4. Записать в файл

def get_html(url):
    r = requests.get(url)   # Объект Response
    return r.text           # Return html code of page URL


def write_csv(data):
    with open("assets\LondonExchangeAnnual.csv", "a", newline="") as f:
        writer = csv.writer(f, delimiter=",")

        writer.writerow([data])


def read_links(path):
    """ Чтение ссылок в список """
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        i = 0
        links = []
        for row in reader:
            print(i, " ", row[0])
            links.append(row[0])
            i = i + 1
    return links

def find_finance_page(url):
    # print("Finance URL: ", url)
    STR = "Fundamentals"
    html = get_html(url)
    bs = BeautifulSoup(html, "lxml")
    refs = bs.find("div", class_ = "company_summary_tabs").find_all("a", class_ = "btn")
    for ref in refs:
        title = ref.get("title")
        if title == STR:
            a = "https://www.londonstockexchange.com" + ref.get("href")
            return a
        else:
            continue
    return " "

def get_per_tax(url):
    print("Pre_tax URL: ", url)
    html = get_html(url)
    bs = BeautifulSoup(html, "lxml")
    try:
        table = bs.find("table", class_ = "table_dati")
        ths = table.find_all("th")

        # Находим заголовки таблицы
        titles = []
        titles.append(url)
        for th in ths:
            s = str(th.text).strip()
            # print ("S: ", s)
            newstr = s[:s.index(" ")]
            #print(newstr)
            titles.append(newstr)
        # print("Titles: ", titles)

        # Находим данные нужной строки
        data = []

        trs = table.find("tbody").find_all("tr")
        tr = trs[4]
        tds = tr.find_all("td")
        s = tds[0].text.strip()
        # print("S: ", s)
        if s == "Profit Before Tax":
            # print("Find")
            pre_tax = trs[4].find_all("td")
            for t in pre_tax:
                stripped = t.text.strip()
                # print(stripped)
                data.append(stripped)
        else:
            data.append("NO Profit Before Tax")
        # print(data)
    except:
        data.append("NO Profit Before Tax")

    titles.extend(data)
    print(titles)
    return titles


def main():
    LIST_PATH = "assets\ListLondonExchange.csv"  # путь к списку

    # 1. Прочитать ссылки
    links = read_links(LIST_PATH)

    # 2. Найти страничку с финансами
    data = []

    #link = "https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary/GB00BCDBXK43GBGBXASX1.html"

    for link in links:

        pageURL = find_finance_page(link)
        if pageURL is "":
            data.append(link)
        else:
            per_tax = get_per_tax(pageURL)
            data.append(per_tax)
        write_csv(data)



    # 3. Прочитать нужную строку
    # 4. Записать в файл


#-----START---------
if __name__ == '__main__':
    thread_index = 0
    main()