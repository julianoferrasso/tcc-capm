"""
Created on Wed Sep 16 11:12:18 2020

@author: Juliano.Ferrasso
@author: Douglas.Muniz
"""

import time
import psycopg2
import numpy as np
from matplotlib import pyplot as plt

def calcula_capm():
    print ("-- Iniciando conexão com o banco de dados PostgresSQL")
    try:
        connection = psycopg2.connect(user = "tcc",
                                      password = "tcc",
                                      host = "192.168.0.35",
                                      port = "5432",
                                      database = "tcc")

        cursor = connection.cursor()

        print ("-- Conexão estabelecida com o banco de dados PostgresSQL")
        
        #inicializacao var COV -C-ovariancia
        COV = 0
        
        #inicializacao var VAR --Variancia
        VAR = 0
        
        #informa Acao a ser analisada
        cod_acao = 'SUZB3'
        
        #informa dia inicial do periodo analisado
        dia_inicio = '2019-01-01'
        
        #informa dia final do periodo analisado
        dia_fim = '2019-07-31'
        
        #busca no BD quantidade de  pregoes no periodo informado:
        cursor.execute("SELECT count(preco) FROM preco WHERE cod_acao like '%IBOV%' and dia >= '"+dia_inicio+"' and dia <= '"+dia_fim+"';")
        N = cursor.fetchone()
        N = (N[0])
        
        #busca no BD precos da acao no periodo informado
        cursor.execute("SELECT preco FROM preco WHERE cod_acao like '%"+cod_acao+"%' and dia >= '"+dia_inicio+"' and dia <= '"+dia_fim+"';")
        acao = cursor.fetchall()            
        
        #busca no BD precos do IBOV  no periodo informado
        cursor.execute("SELECT preco FROM preco WHERE cod_acao like '%IBOV%' and dia >= '"+dia_inicio+"' and dia <= '"+dia_fim+"';")
        ibov = cursor.fetchall()      
        
        #busca no BD as datas dos precos no periodo informado
        cursor.execute("SELECT dia FROM preco WHERE cod_acao like '%IBOV%' and dia >= '"+dia_inicio+"' and dia <= '"+dia_fim+"';")
        dias = cursor.fetchall()  
        
        #inicializa vetores do ibov, acao, retorno ibov e retorno da acao
        vet_dia = []
        vet_dia_ret = []
        vet_ibov = []
        vet_acao = []
        vet_ret_ibov = []
        vet_ret_acao = []
        
        #preenche vetor dias com o resultado da consulta no BD
        for x in range (N):
            vet_dia.append(dias[x][0]) 

        #preenche vetor ibov com o resultado da consulta no BD
        for x in range (N):
            vet_ibov.append(ibov[x][0])
        
        #preenche vetor acao com o resultado da consulta no BD
        for x in range (N):
            vet_acao.append(acao[x][0])
        
        #inverte os vetores ibov e acao para faciltar o calulco do retorno que deve ser da divisão do dia mais atual para o dia menos atual
        vet_ibov.reverse()
        vet_acao.reverse()   
        
        #preenche vetor retorno ibov
        i = 0
        for i in range (N-1):
            vet_ret_ibov.append(1-(vet_ibov[i]/vet_ibov[i+1]))
            i +=1
           
        #preenchendo vetor retorno acao    
        i = 0
        for i in range (N-1):
            vet_ret_acao.append(1-(vet_acao[i]/vet_acao[i+1]))
            i +=1
            
        #preenchendo vetor dia retorno acao    
        i = 0
        for i in range (N-1):
            vet_dia_ret.append(vet_dia[i])
            i += 1
        
        #calculo da covariancia
        
        #obtem tamanho do vetor de retorno da acao e do ibov
        len_ret_ibov = vet_ret_ibov.__len__()
        len_ret_acao = vet_ret_acao.__len__()
        
        #calculo da media do retorno do ibov
        media_ret_ibov = 0
        for x in vet_ret_ibov:
            media_ret_ibov += x
        media_ret_ibov = media_ret_ibov/(vet_ret_ibov.__len__())
        
        #calculo da media do retorno da acao
        media_ret_acao = 0
        for x in vet_ret_acao:
            media_ret_acao += x
        media_ret_acao = media_ret_acao/(vet_ret_acao.__len__())
        
        print('retorno med acao:',media_ret_acao)
        print('retorno med ibov:',media_ret_ibov)
        
        #calculo da Covariancia entre a acao e o ibov
        for x in range (len_ret_acao):
            COV += ((vet_ret_acao[x]-media_ret_acao) * (vet_ret_ibov[x]-media_ret_ibov))
        COV = COV/(len_ret_acao) 
        
        print ('covariancia=',COV)
        
        #calculo da Variancia do ibov
        for x in range (len_ret_ibov):
            VAR += (vet_ret_ibov[x]-media_ret_ibov)**2
        VAR = VAR/(len_ret_ibov-1)
        
        print ('variancia=', VAR)
        
        #calculo do Beta
        Beta = COV/VAR
        Beta = float(Beta)
        
        print ("beta",cod_acao,'Periodo',dia_inicio,'a',dia_fim, Beta)
        
    
        #inicializa var Re -- Retorno esperado
        Re = 0
        #inicializa var Rf -- Retorno livre de Risco (taxa SELIC)
        Rf = (4/100)
        #inicializa var Rm -- Retorno médio do mercado (Bovespa)
        Rm = (25/100)
    
        #calculo do CAPM
        Re = Rf+(Beta*(Rm-Rf))
    
        print ("Retorno Esperado (CAPM) de",cod_acao,"=", Re*100)   
         
        
        #Gera grafico comparativo retorno acao x ibov
        plt.plot((vet_dia_ret),vet_ret_ibov)
        plt.plot((vet_dia_ret),vet_ret_acao)
        plt.title('Retrono '+cod_acao+' x IBOV peridodo'+dia_inicio+' a '+dia_fim)
        plt.xlabel ('Periodo')
        plt.ylabel ('Retorno (%)')
        plt.legend(['IBOV', cod_acao], loc=2)
        plt.show()

        
        
        """
        #Geracao do grafico do Beta
        x = np.array(vet_ret_acao)
        y = np.array(vet_ret_ibov)
        x = (np.float_(x))
        y = (np.float_(y))        
        
        plt.plot(x,y, 'o')
        
        m, b = np.polyfit(x, y, 1)
        
        plt.plot(x, m*x + b)
        plt.title('Beta '+cod_acao+' periodo '+dia_inicio+' a '+dia_fim)
        """
       
  

    except (Exception, psycopg2.Error) as error :
        print ("Erro de conexao com o banco de dados PostgreSQL", error)
    finally:
        #fechando a conexao com o banco de dados
            if(connection):
                cursor.close()
                connection.close()
                print("Conexao com o banco de dados PostgreSQL fechada")  


start = time.time()


calcula_capm()



end = time.time()

print("\n\n\ntempo de processamento total: ", (end - start),"segundos")

