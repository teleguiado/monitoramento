import socket
import datetime
from ping.aux_fun import grava, calculate_time
import time

def alternate_IP_PORT(IP, PORT):
    # to ping a particular IP
    try:
        socket.setdefaulttimeout(5)
          
        # if data interruption occurs for 3
        # seconds, <except> part will be executed
  
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET: address family
        # SOCK_STREAM: type for TCP
  
        host = IP
        port = PORT
  
        server_address = (host, port)
        s.connect(server_address)
  
    except OSError as error:
        return False
        # function returns false value
        # after data interruption
  
    else:
        s.close()
        # closing the connection after the
        # communication with the server is completed
        return True
    
def ping(IP): #resolvo problema de portas
    if alternate_IP_PORT(IP, 80):
        return True
    elif alternate_IP_PORT(IP, 135):
        return True
    elif alternate_IP_PORT(IP, 139):
        return True
    elif alternate_IP_PORT(IP, 445):
        return True
    else:
        return False
    
def general_ping(ID, NICK, IP, unit_tip, acronym, queue):
    while True:
        if ping(IP): #pinga e testa reconexao se estiver disponivel
            tempo_conexao = datetime.datetime.now()
            data_conexao = tempo_conexao.strftime("%d/%m/%Y as %H:%M:%S")
            temp_print = (f"A unidade {NICK} conectou-se no dia {data_conexao}")
            print(temp_print)
            grava(temp_print, NICK) #gera log e grava
            while ping(IP) == True:
                queue.put((ID, NICK, unit_tip, acronym, "ON"))
                time.sleep(20) #vai esperar 10 segundos e vai recomeçar o while
                
        else:
            tempo_desconexao = datetime.datetime.now()
            data_conexao = tempo_desconexao.strftime("%d/%m/%Y as %H:%M:%S")
            temp_print = (f"A unidade {NICK} desconectou-se no dia {data_conexao}")
            print(temp_print)
            grava(temp_print, NICK) #gera log e grava
            while not ping(IP): # esse laço vai prender o a execução ate que a conexão com o ip seja reestabelecida
                queue.put((ID, NICK, unit_tip, acronym, "OFF"))
                time.sleep(20)

            tempo_conexao = datetime.datetime.now()
            time_desconect = (f"Tempo de desconexão {calculate_time(tempo_desconexao, tempo_conexao)}")
            grava(time_desconect, NICK)
            print(time_desconect)
            
