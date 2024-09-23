#!/usr/bin/env python

#importa todas das bibliotecas python a serem utilizadas
import socket 
import thread
import sys
import time
import warnings
warnings.filterwarnings('ignore')

PORT = 5022         #Porta do servidor
idLocal = 8001        #id do peer local
menorId = 8001        #lider pela perspectiva do peer
sleepTime = 2       #tempo entre cada heartbeat

#Funcao que e chamada no inicio da execucao, na qual o peer 
#proativamente busca na lista de hosts local, e com essa informacao,
#ele tenta realizar uma conexao com os peers dessa lista.


def tryConnection(): 
    global idLocal
    global menorId
    meuHost = socket.gethostname() # armazena o proprio nome
    fileName = 'log'+meuHost+'.txt'
    log_file = open(fileName,"w")
    sys.stdout = log_file
    print 'Eu sou',meuHost 

    file = open('hosts.txt', 'r') # abre o arquivo de hosts    
    for line in file: #para cada linha na lista de hosts
        words = line.split(); #remove espaco entre informacoes
        if meuHost != words[0]: # se o nome do host da lista nao e o mesmo do host local
            HOST = words[0]     # Endereco IP do Servidor
            PORT = 5022     # Porta que o Servidor esta
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria socket tcp
            dest = (HOST, PORT) #Atribui um host e uma porta ao destino
            if tcp.connect_ex(dest) == 0: #se a conexao obteve sucesso, cria 2 threads (1 para enviar e 1 para receber)
                print 'Estabeleci conexao com', words[0]
                print 'meu lider e', menorId,' e o novo id e',words[1] 
                if(int(words[1]) < menorId): #compara se o lider esta certo
                    menorId = int(words[1])
                    print 'troquei o lider para', words[0] 

                thread.start_new_thread(conectadoReciever, tuple([tcp, HOST])) #inicia threads de entrada e saida
                thread.start_new_thread(conectadoSender, tuple([tcp, HOST]))

        else: #se o host da lista e o mesmo do host local

            idLocal = int(words[1]) #obtem id local
           
            print 'meu lider e',words[0],'e o novo id e',words[1] 
            if(idLocal < menorId):
                menorId = idLocal
                print 'Eu,',words[0],'sou o lider' # supoe que o local e o lider
    file.close()

def conectadoSender(con, remoto):
    global menorId
    global sleepTime
    msg = str(menorId) #transforma o menor id em string e envia como mensagem. Serve como o heartbeat
    while msg <> '\x18':
            print '//////////////////////////////////////////////////////////'
            print 'Enviando HeartBeat <3'
            con.send (msg)
            time.sleep(sleepTime)
            msg = str(menorId)
            
    thread.exit()

def conectadoReciever(con, remoto):
    print 'Conectado com', remoto
    global menorId
    while True:
        msg = con.recv(1024) #recebe 1KB
        if not msg: break
        print 'Recebi HeartBeat de',remoto,'<3'
        if(int(msg) < menorId): #se recebi um menorId de outro peer que e menor que o local
            menorId = int(msg)
            print 'Troquei o lider para :',menorId 


    #print 'Finalizando conexao com',remoto
    global idLocal
    menorId = idLocal #assume que o local e o lider
    print '/////////////////////URGENTE//////////////////'
    print 'Preparando-se para a votacao, pois alguem caiu :('
    con.close()
    thread.exit()




tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = ('', PORT)

tcp2.bind(orig)
tcp2.listen(1)

#MODO ATIVO
thread.start_new_thread(tryConnection, tuple([]))

#MODO PASSIVO
while True:
    con, remoto = tcp2.accept()

    temp = socket.gethostbyaddr(remoto[0]);
    nome = temp[0]
    achouPonto = nome.find('.')
    if achouPonto > -1:
        nome = nome[0:achouPonto] #obtem apenas os 3 primeiros digitos do nome, pois se obtido a partir de  socket.gethostbyaddr(remoto[0]), devolve com o sufixo .localc3sl
    
    print 'Conexao recebida e efetuada com' , nome

    thread.start_new_thread(conectadoReciever, tuple([con, nome]))
    thread.start_new_thread(conectadoSender, tuple([con, nome]))

tcp2.close()
