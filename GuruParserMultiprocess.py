
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)  #объект Response
    return r.text           #return html code of page URL

# Получение ссылки на Definitions
def get_definitions_link(html):
    soup = BeautifulSoup(html, "lxml")
    link = ""
    try:
        a = soup.find("ul", class_ = "tabs").find("a", class_= "m13").get("href")
    except:
        a = ""
        return a
    link = "https://www.gurufocus.com" + a
    #print("Definitions link: ", link)
    return link

# Получение ссылки на таблицу До вычета налогов
def get_per_tax_link(html):
    soup = BeautifulSoup(html, "lxml")
    try:
        a = soup.find("ul", id = "Pretax_Income").find("a").get("href")
    except:
        a = ""
        return a
    link = "https://www.gurufocus.com" + a
    #print("Per-Tax link: ", link)
    return link

# Считывание данных с годовой таблицы до налогов
def get_annual_data(html):
    soup = BeautifulSoup(html, "lxml")
    anual_data = []
    div_historical = soup.find("div", id="target_def_historical_data")
    divs = div_historical.find_all("div")
    for div in divs:
        try:
            title = div.find("p").text.strip()
            #print("Title: ", title)
            if "Annual Data" in title:
                #print("Annual!")
                trs = div.find("table", class_="R10").find_all("tr")

                # первая строка с датами
                tr = trs[0]
                tds = tr.find_all("td")
                for td in tds:
                    text = td.text.strip()
                    anual_data.append(text)

                # вторая строка с цифрами
                tr = trs[1]
                tds = tr.find_all("td")
                for td in tds:
                    text = td.text.strip()
                    anual_data.append(text)
                break
        except:
            #print("Ерунда! не найден тег <p>")
            continue
    return anual_data

def write_csv(data):
    with open("SPB_From_Guru.csv", "a", newline="") as f:
        writer = csv.writer(f, delimiter=",")

        writer.writerow(data)

def parse(url):
    annual = []
    definition_link = get_definitions_link(get_html(url))
    if definition_link != "":

        per_tax_link = get_per_tax_link(get_html(definition_link))
        if per_tax_link != "":
            annual.append(url)
            annual.extend(get_annual_data(get_html(per_tax_link)))

            write_csv(annual)
        else:
            annual.append(url)
            write_csv(annual)
            print(url, "Not parsed")
        print(url, "parsed")
    else:
        annual.append(url)
        write_csv(annual)
        print(url, "Not parsed")


def get_all_links():
    preURL = "https://www.gurufocus.com/stock/"
    links = []

    file = open("ListSPB.txt", "r", encoding="utf-8")

    for line in file:
        tiker = line.rstrip("\n")
        links.append(preURL+tiker)

    return links

def main():

    all_links = get_all_links()
    print(all_links)

    with Pool(40) as p:
        p.map(parse, all_links)


#-----START---------
if __name__ == '__main__':
    main()