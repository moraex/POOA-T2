'''
    LUAN VINICIUS MORAES - 744342

    PROGRAMAÇÃO ORIENTADA A OBJETOS AVANÇADA

    TRABALHO 2

'''

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import Request, urlopen
import csv
import sys


PAGE_DICT = dict()
PAGE_DICT["estadao"] = {
    "name" : 'estadao',
    "url" : 'https://www.estadao.com.br/'
}

PAGE_DICT["g1"] = {
    "name" : 'g1',
    "url" : 'https://g1.globo.com/'

}

PAGE_DICT["bol"] = {
    "name" : 'bol',
    "url" : 'https://www.bol.uol.com.br/'

}


class Open:
    def __init__(self):
        pass

    def fun_soup(self, site):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req)
        return BeautifulSoup(page, 'html.parser')


class Writer:
    def __init__(self, Open):
        self.Open = Open()

    def query(self, page_name, soap):
        answer = []

        # ESTADAO BEHAVIOR
        if(page_name == 'estadao'):
            query = soap.select("h3.title > a")

            for e in query:
                answer.append([
                    "Página Principal",
                    f"{e.get('title')}",
                    f"{e.get('href')}"
                ])

        # BOL BEHAVIOR
        elif(page_name == 'bol'):
            query = soap.select("div.thumbnails-wrapper")

            for e in query:
                url = e.select('a')[0].get('href')
                title = e.select('h3')[0].text
                answer.append([
                        "Página Principal",
                        f"{url}",
                        f"{title}"
                ])

        # G1 BEHAVIOR
        elif(page_name == 'g1'): 
            query = soap.select("div.feed-post")

            for e in query:
                url = e.select('a')[0].get('href')
                title = e.select('a')[0].text
                answer.append([
                        "Página Principal",
                        f"{url}",
                        f"{title}"
                ])

        return answer


    def write(self, page, parser = "soup"):
        page_name = page["name"]
        page_url = page["url"]

        # abertura de arquivo csv
        csv_file = open(f"dump_{page_name}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.csv", mode="w")
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(['category', 'title', 'link'])

        # obtemos a pagina da internet e fazemos o parser
        soap = self.Open.fun_soup(page_url)

        # query pelos titulos e links
        query = self.query(page_name, soap)

        for e in query:
            csv_writer.writerow([e[0], e[1], e[2]])

        csv_file.close()
        

# Main
# orquestra os modulos para produzir
# a saida desejada
class Main:
    def __init__(self, pagina):
        self.Open = Open()
        self.Writer = Writer(Open)
        self.Writer.write(PAGE_DICT[pagina])


if __name__ == '__main__':
    main = Main("estadao")

 