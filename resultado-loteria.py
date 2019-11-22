import asyncio
from aiohttp import ClientSession
import json
import bs4

BASE_URL = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/'
MEGASENA = BASE_URL + 'megasena/'
LOTOFACIL = BASE_URL + 'lotofacil/'
QUINA = BASE_URL + 'quina/'

URLS = [MEGASENA,LOTOFACIL,QUINA]

async def get_url(url, session):
    async with session.get(url) as response:
        return await response.read()

async def busca_resultado(url, session):
    
    
    #Requisição a página principal(BASE_URL) para localizar o endereço da API de resultados.
    html = await get_url(url, session)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    urlBase = soup.find("base")['href']
    urlBuscarResultado = soup.find("input", {"id": "urlBuscarResultado", "type":"hidden"})['value']
    urlAPI = urlBase + urlBuscarResultado
    
    #Processa o JSON da API.
    resultado = json.loads(await get_url(urlAPI,session))
    print(url.split('/')[-2].upper()) #Identifica o nome do jogo(ex: Megasena).
    print("Concurso:", resultado['proximoConcurso'])
    print("Resultado:",resultado['resultadoOrdenado'])
    print('------------')

async def main():
    async with ClientSession() as session:
        tasks = [busca_resultado(url,session) for url in URLS]
        await asyncio.gather(*tasks)
    
await main()
