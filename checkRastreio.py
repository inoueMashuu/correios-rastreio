#================================================
# 
# checkRastreio.py
# 
# Programa que lê uma planilha Excel, contendo os códigos de rastreios de 
# encomendas, e insere as informações mais atuais do item, como:
#        - Status atual
#        - Data do status
#        - Localização atual
#        - Alguma descrição extra
#
# O programa lê o arquivo 'Itens.xls', assim, adicionar o código de rastreio na
# linha correspondente, junto com uma descrição na coluna 'Item' para melhor
# entendimento de que item se trata o código
#
# Por: Matheus Inoue, 2017
#=================================================


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

from pandas import ExcelWriter


def saveXls(list_dfs, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n, index = False)
    writer.save()


def scrapCorreios(df):
    listaItem = ['Último Status', 'Data', 'Local', 'Descrição']
    
    for i in range(len(df)):
        codRastreio = df['Código de Rastreio'][i]
        params = {'objetos': codRastreio}
        header = {'Referer': 'http://www2.correios.com.br/sistemas/rastreamento/default.cfm' }
        link = 'http://www2.correios.com.br/sistemas/rastreamento/resultado.cfm?'

        a = requests.post(link, data=params, headers=header)
        
        soup = BeautifulSoup(a.text, 'lxml')
        tab = soup.find_all('table')
        
        try:
            firstRow = tab[0].find_all('tr')[0].find_all('td')
            dateLoc = firstRow[0]
            statusDescr = firstRow[1] 
            
            data = re.findall('\d{1,2}\/\d{1,2}\/\d{2,4}', str(dateLoc))[0]
            hora = re.findall('\d{1,2}:\d{1,2}', str(dateLoc))[0]
            dataHora = data+' - '+hora

            try:
                localAtual = str(dateLoc.label.string).replace('\xa0/\xa0','/')
            except:
                localAtual = re.findall('[\w]+ \/ \w{2}', str(dateLoc))
                
                if len(localAtual) > 0:
                    localAtual = localAtual[0]
                
                else:
                    localAtual = re.findall('[\w]+ \/', str(dateLoc))[0]

            statusAtual = statusDescr.strong.string
            descr = re.findall('\>[^\<\/]+\<\/td>',str(statusDescr))[0][1:-7]
        except:
            if not pd.isnull(df.loc[i,'Último Status']):
                statusAtual, dataHora, localAtual, descr = df.loc[i, listaItem]
            else:
                statusAtual, dataHora, localAtual, descr = 'Código inválido', np.nan, np.nan, np.nan
        
        
        df.loc[i,listaItem] = statusAtual, dataHora, localAtual, descr
    
    return df
    

df = pd.read_excel('Itens.xls')
df = scrapCorreios(df)

saveXls([df], 'Itens.xls')
