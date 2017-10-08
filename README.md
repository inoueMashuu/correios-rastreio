# correios-rastreio
----
Script para obter a última atualização de encomendas pelo site dos Correios, utilizando técnicas de data scraping, além de manipulação de planilhas Excel para armazenamento das informações das encomendas.

### Requisitos
----
- Requests
- BeautifulSoup
- pandas
- numpy

A distribuição [Anaconda](https://www.anaconda.com/distribution/) já contém todas as bibliotecas utilizadas, não sendo necessária outras instalações.

### Como funciona?
----
Basta apenas inserir os códigos de rastreio desejados na planilha **Itens.xls**, na coluna *Código de Rastreio*, um por linha. Para melhor visualização, é recomendado inserir uma descrição do item na coluna *Item*.

Com os códigos de rastreio, rodar o arquivo **checkRastreio.py**, o script Python que faz o data scraping do site dos Correios, pegando as últimas atualizações de cada encomenda, como:
- Status atual
- Data do status
- Localização atual
- Alguma descrição extra

O programa então atualiza a planilha **Itens.xls**, com os dados obtidos, de modo que é possível ver o último status disponível de cada encomenda.

