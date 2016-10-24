import time
from bs4 import BeautifulSoup
import requests
import os
import mysql.connector
import traceback

def connect() :
        try:
            return mysql.connector.connect(user='admin', password='root', host='db4free.net', database='pystebin')
        except Exception, err:
            traceback.print_exc()
            time.sleep(10000)
            print('Nao foi possivel conectar ao banco! Tentando conectar novamente')
            time.sleep(3)
            connect()

class main():

    if not os.path.exists('Downloads') : # cria a pastinha downloads se nao existir :D
        os.makedirs('Downloads')
    
    t = 0 # contador de downs
    nome_do_arquivo = '' # nome do arquivo pra verificar se o get foi duplicado [ como to pegando de 3 em 3 seg pode ser que alguem nao enviou nesse tempo ]
    
    while True:

        conexao = connect()
        cursor = conexao.cursor()

        r = requests.get('http://pastebin.com/archive') # Vai na url de arquivos, descobri que apos um tempo pegando
        # o pastebin da ban, mas eu consegui pegar pelo public paste ali do canto :D !

        bs = BeautifulSoup(r.content,'lxml').findAll('a')
           
        if len(bs) == 2 : 
            print('Nao foi possivel conectar no pastebin, provavalmente seu ip foi banido.')
            continue

        id = bs[10].attrs.itervalues().next() # cata o nome gerado do site pela tag a
        link = 'http://pastebin.com' + id # link final
           
        split = str(id).split('/') # tira o / do link ex: /AbCdEfG123

        if nome_do_arquivo == str(split[1]) :
            for k in range(1,4):
                print('Ninguem mandou algo novo ainda, tentando novamente' + '.'*k)
                
            time.sleep(3) # 3 segundos pra ver se alguem mandou algo novo
            continue # ignora tudo abaixo e recomeca o loop

        nome_do_arquivo = str(split[1]) # pega o atual nome do arquivo
        
        r = requests.get(link)  # faz um novo get no link recebido

        tbl = BeautifulSoup(r.content, 'lxml').findAll('li') # pega as tags li

        conteudo_arquivo = ''
        
        for i in range(18,len(tbl)) : # loopzera pra pegar todo conteudo do arquivo do site
            if(len(tbl[i].contents) > 0) :
                if(len(tbl[i].contents[0]) > 0) :
                    conteudo_arquivo += ''.join((tbl[i].contents[0].contents[0]).encode('utf-8').strip())
                    conteudo_arquivo +='\n'

        if len(conteudo_arquivo) > 0 : # checa se o arquivo foi valido pra download

            query = ("INSERT INTO pystebin (nome_arquivo, conteudo) VALUES (%(var1)s, %(var2)s)")
            query_data = {'var1': nome_do_arquivo, 'var2': conteudo_arquivo,}
            cursor.execute(query,query_data)
            conexao.commit()
            cursor.close()
            conexao.close()

            t = t+1

        #gran fenale

        print('===========================================================')
        print('dh.18@msn.com or tone@elitedev.com.br')
        print('===========================================================')
        print('Pastebin public pastes grabber - by Tone - Elite Dev 2016')
        print('===========================================================')
        print('Arquivos baixados: ' + str(t))
        print('===========================================================')
                
        time.sleep(3) # 3 segundex - 1 segundo levei ban de ip no cloud kkkk
