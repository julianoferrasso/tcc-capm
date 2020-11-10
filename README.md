### TCC - Uma Análise Estatística da Bolsa de Valores

##### Trabalho de Conclusão de Curso de Ciência da Computação - UNICARIOCA

#### OBJETIVO PRINCIPAL

Este trabalho visa a sistematização do modelo matemátcio chamado CAPM que é utilizado para o cálculo da estimativa do retorno de um investimento em ações e uma sistematização do cálculo do Beta que representa o risco de uma determinada ação.
Para tanto foi utilizado o arquivo da série histórica da BOVESPA e utlizada a liguagem Python para a elabotração do algoritmo.

Pela pouco eficiência em trabalhar com leitura de arquivo, para o algorimto processar os dados, foi elaborado um algoritmo auxiliar **(tcc-importa-acoes-ibov.py)** para popular um banco de dados relacional em PostgreSQL que através do arquivo da série histórica do BOVESPA o algoritmo fez a inserção dos valores necessários no banco de dados. 

O algoritmo principal **(tcc-calcula-capm.py)** tem uma função chamada *calcula_capm(arg1, arg2, arg3, arg4)* com quatro seguintes argumentos:
  - arg1 - destinado a informar o código da ação de operação na bolsa de valores a ser analisada. ex: (PETR4, ABEV3, BBAS3)
  - arg2 - destinado a informar a data inicial do período a ser analisado. A data deve estar no formato AAAA-MM-DD. ex: (2019-01-01)
  - arg3 - destinado a informar a data final do período a ser analisado. A data deve estar no formato AAAA-MM-DD. ex: (2019-01-31)
  - arg4 - destinado a informar o tipo de gráfico desejado na saída do algoritmo. valores aceitos são '1' e '2'. 1 para gerar o gráfico do retorno do Ibovespa x Ação analisada; 2 para gerar o gráfico do Beta da ação
  
 Por questão do arquivo da serie historica anual das ações listadas na BOVESPA term mais de 25Mb o limite permitido pelo guithub, nao foi possivel o carregamento do mesmo. Porem o arquivo da série historica pode ser facilmente encontrado através do link XXX
 
 Ja os índices IBOVESPA, como não estão disponibilizados em arquivos e somente em html no site da BOVESPA atraves do link #http://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-estatisticas-historicas.htm foi gerado um arquivo .TXT manualmente com os dados em tela para o algorimto auxiliar fazer a leitura do mesmo e inserir as informações no banco de dados.
