# Парсит данные Per-tax c сайта Macrotrends по списку ListMacrotrends.csv

import requests
import datetime

import csv
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)   # Объект Response
    return r.text           # Return html code of page URL

def write_csv(data):
    with open("assets\MacrotrendsQuarterly.csv", "a", newline="") as f:
        writer = csv.writer(f, delimiter=",")

        writer.writerow(data)


def read_links(path):
    """ Чтение ссылок в список """
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        i = 0
        links = []
        for row in reader:
            #print(i, " ", row[0])
            links.append(row[0])
            i = i + 1
    return links


def link_to_finstate(links):
    """ Замена URL \stock-price-history на \financial-statements """
    tmp_links = []
    for link in links:
        link = str(link).replace("stock-price-history", "financial-statements")
        tmp_links.append(link)
    links = tmp_links[:]
    return links


def get_per_tax(url):
    #print(url)
    titles = []                         # Тут хранятся заголовки с датами
    data = []                           # Тут хранится цифра за эту дату
    global thread_index

    titles.append(url)                  # добавляем метку URL



    try:
        html = get_html(url)
    except:
        titles.append("Ошибка")
        write_csv(titles)

        ind = thread_index + 1
        thread_index = ind
        print(thread_index, " ", titles)
        return titles


    # Очищаем HTML от лишней "шелухи"
    pre_tax_index = html.find("Pre-Tax Income")     # определяем индекс начала среза
    income_tax_index = html.find("Income Taxes")    # определяем индекс конца среза
    cutt = html[pre_tax_index:income_tax_index]     # делаем срез

    # более детальная очистка
    div = cutt.rfind("div")+6                       # определяем индекс начала среза
    field_name = cutt.find("field_name")-4          # определяем индекс конца среза
    cutt2 = cutt[div:field_name]                    # делаем срез
    cutt2 = cutt2.replace("\"", "")                 # удаляем "

    str = ""                                        # Временна строка
    i = 0
    lenght = cutt2.__len__()

    # побуквенный перебор
    while i <= lenght:
        # проверка конца строки
        if i == lenght:
            data.append(str)
            break
        s = cutt2[i]

        # проверка разделителя : (заголовок:данные)
        if s == ":":
            titles.append(str)
            str = ""
        # проверка разделителя , (данные,заголовок)
        elif s == ",":
            data.append(str)
            str = ""
        else:
            str += s
        i += 1

    # Добавление пустой записи, для выравнивания, если нет данных о текущем году (2018)
    # is_2018 = False
    # for title in titles:
    #     if "2018" in title:
    #         is_2018 = True
    #         break
    # if not is_2018:
    #     titles.insert(1, " ")
    #     data.insert(0, " ")

    while titles.__len__() < 30:        # Дополняет пробелами если в заголовке меньше чем 2018-2005 = 13 + 1 + 1
        titles.append(" ")
    # print(titles)
    # print(data)

    titles.extend(data)                 # Объединяем заголовки и данные в одну строку

    write_csv(titles)
    ind = thread_index + 1
    thread_index = ind

    print(thread_index, " ", titles)
    return titles


def main():
    start = datetime.datetime.now()

    LIST_PATH = "assets\ListMacrotrends.csv"    # путь к списку
    ANNUAL = "?freq=A"                          # Annual добавка к URL
    QUARTERLY = "?freq=Q"                       # Quarterly добавка к URL

    history_links = read_links(LIST_PATH)       # чтение списка ссылок
    all_links= link_to_finstate(history_links)  # замена URL \stock-price-history на \financial-statements
    #print(all_links)

    finance_links = []
    for link in all_links:                      # Добавление Annual или Quarterly
        tmp = str(link) + QUARTERLY
        finance_links.append(tmp)

    # with Pool(10) as p:
    #     p.map(get_per_tax, finance_links)
    # finance_links = finance_links[1382:]
    for link in finance_links:
        get_per_tax(link)

    end = datetime.datetime.now()

    total = end - start
    print(str(total))




#-----START---------
if __name__ == '__main__':
    thread_index = 0
    main()