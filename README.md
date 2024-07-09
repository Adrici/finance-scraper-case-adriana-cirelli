# finance-scraper-case-adriana-cirelli

##Yahoo Finance Scraper

Este projeto consiste em um web scraper desenvolvido em Python usando Selenium. O objetivo é coletar dados de nomes, símbolos e preços (intraday) de empresas listadas no site Yahoo Finance, com a capacidade de filtrar por região.

##Funcionalidades

Filtragem por Região: Utiliza um parâmetro de entrada para filtrar resultados por região.
Extração de Dados: Captura dados de todas as páginas resultantes da filtragem.
Saída em CSV: Salva os dados coletados em um arquivo CSV contendo apenas as colunas Symbol, Name, Price.

##Configuração do Ambiente:

Instale as dependências necessárias listadas no requirements.txt.

##Execução:

Execute o arquivo main_program.py para iniciar o scraper.
A saída será salva automaticamente na pasta results como yahoo_finance_screener.csv.
Ao executar os testes unitários a sáida será salva no mesmo diretório 'results' como tes_output.csv

##Notas

Este projeto foi desenvolvido como parte de um desafio para capturar informações específicas de empresas listadas na Argentina no Yahoo Finance.
A página padrão exibe 25 resultados por página, com um total de 29 páginas processadas para coletar 709 resultados.

##Comando para executar o programa principal que coleta dados do Yahoo Finance:

```python main.py```

##Comando para executar os testes unitários que verificam o funcionamento do scraper:

```python -m unittest test_scraper.py```

