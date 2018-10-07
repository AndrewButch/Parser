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

        writer.writerow(data)


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
    bs = BeautifulSoup(url, "lxml")
    refs = bs.find("div", class_ = "company_summary_tabs").find_all("a")
    for ref in refs:
        title = ref.get("title")
        if title is not "Fundamentals":
            continue
        else:
            return ref.get("href")
    return " "

def get_per_tax(url):
    bs = BeautifulSoup(url, "lxml")
    table = bs.find("div", class_ = "table_dati")
    ths = table.find_all("th")
    titles = []
    for th in ths:
        print(th.text)
        titles.append(th.text)


def main():
    LIST_PATH = "assets\ListLondonExchange.csv"  # путь к списку

    # 1. Прочитать ссылки
    links = read_links(LIST_PATH)

    # 2. Найти страничку с финансами
    data = []
    for link in links:
        page = find_finance_page(link)
        if page is "":
            data.append(link)

        else:
            data.append(get_per_tax(link))
        write_csv(data)



    # 3. Прочитать нужную строку
    # 4. Записать в файл


#-----START---------
if __name__ == '__main__':
    thread_index = 0
    main()