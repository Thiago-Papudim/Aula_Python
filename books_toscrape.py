import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
page_catalogue = "https://books.toscrape.com/catalogue/page-"

response = requests.get(url)
response_page = BeautifulSoup(response.text, 'html.parser')

text_num_pages = response_page.find('li', {'class': 'current'}).text.strip()
total_pages = int(text_num_pages.split()[3])

catalogo_livros = []

for num_page in range(1, total_pages+1):
    pagina = f"{page_catalogue}{num_page}.html"
    response = requests.get(pagina)
    response_page = BeautifulSoup(response.text, 'html.parser')
    livros = response_page.find_all('article', {'class': 'product_pod'})

    for livro in livros:
        titulo = livro.find('h3').a['title']
        preco = float(livro.find('p', {'class': 'price_color'}).text.lstrip('Â£'))
        ancora = livro.find('a')['href']
        link = f"{url}{ancora}"
        catalogo_livros.append(dict(titulo=titulo, preco=preco, link=link))
    

df = pd.DataFrame(data=catalogo_livros)
df.columns = ['Título', 'Preço', 'Link']
df = df.sort_values(by=['Preço'], ascending=False)

df.to_excel('catalogo_livros.xlsx', index=False)