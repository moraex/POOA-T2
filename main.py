'''
    LUAN VINICIUS MORAES - 744342

    PROGRAMAÇÃO ORIENTADA A OBJETOS AVANÇADA

    TRABALHO 2

'''

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
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

# main.py -site estadao -o csv -sep ;

ERR_MSG = '''
    padrao de isercao incorreto
    por favor respeite o padrao
        python main.py -site <seu_site> [-sep <seu_sep>]
    em que
        -sep        opcional
        <seu_sep>   o separador desejado (default ';')
    e <seu_site> deve ser um dos nomes a seguir:
'''

class ArgParser:
    def __init__(self):
        self.args = sys.argv[1:]
        self.error = False

        if len(self.args) < 1:
            self.error = True
            print(ERR_MSG)
            print('\n'.join(PAGE_DICT.keys()))

        else:
            # verificacoes obrigatorias
            if (self.args[0] != "-site"):
                self.error = True
            if (self.args[1] not in PAGE_DICT.keys()):
                self.error = True
            
            if len(self.args) > 2:
                if len(self.args) > 4:
                    self.error = True
                if not self.args.__contains__("-sep"):
                    self.error = True

            if(self.error):
                print(ERR_MSG)
                print('\n\t'.join(PAGE_DICT.keys()))

            self.args_site = self.args[1]
            self.args_sep = ";" if not self.args.__contains__("-sep") else self.args[3]

    def getSite(self):
        return self.args_site

    def getSep(self):
        return self.args_sep

    def getError(self):
        return self.error

class Open:
    def __init__(self):
        pass

    def fun_soup(self, site):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req)
        return BeautifulSoup(page, 'html.parser')

class QueryManage:
    def __init__(self):
        pass

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

class Writer:
    def __init__(self, Open):
        self.Open = Open()
        self.Query = QueryManage()

    def write(self, page, sep, parser = "soup"):
        page_name = page["name"]
        page_url = page["url"]

        # abertura de arquivo csv
        csv_file = open(f"dump_{page_name}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.csv", mode="w")
        csv_writer = csv.writer(csv_file, delimiter=sep)
        csv_writer.writerow(['category', 'title', 'link'])

        # obtemos a pagina da internet e fazemos o parser
        soap = self.Open.fun_soup(page_url)

        # query pelos titulos e links
        query = self.Query.query(page_name, soap)

        for e in query:
            csv_writer.writerow([e[0], e[1], e[2]])

        csv_file.close()
        

# Main
# orquestra os modulos para produzir
# a saida desejada
class Main:
    def __init__(self):
        self.Open = Open()
        self.Args = ArgParser()

        if not self.Args.getError():
            self.Writer = Writer(Open)
            self.Writer.write(PAGE_DICT[self.Args.getSite()], self.Args.getSep())


if __name__ == '__main__':
    main = Main()

 