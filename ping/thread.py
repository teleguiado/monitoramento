from ping.ping import general_ping as GP
from ping.db_status import db_status as DB
import threading as THR
import queue
import time
import app

result_queue = queue.Queue()
data_units = []


def db_veiifcation():
    app.cursor_units.execute("SELECT * FROM units") 
    app.total_unit_and_data = app.cursor_units.fetchall()        
        
def serve_ping():
    app.data_for_ping.clear() 
    for unit in data_units:# trata os dados para ser pingado e depois disponibilizar junto a API
        name_unit = unit[10]
        globals()[name_unit] = []
        globals()[name_unit].append(unit[0]) #ID
        globals()[name_unit].append(unit[2]) #NICK 
        globals()[name_unit].append(unit[4]) #unit_tip
        globals()[name_unit].append(unit[9]) #IP
        globals()[name_unit].append(unit[10]) #acronym
        app.data_for_ping.append(globals()[name_unit])
        
        T = THR.Thread(target=GP, args=(unit[0], unit[2], unit[9], unit[4], unit[10], result_queue)) #cria uma thread para cada unidade 
        T.start()
        
    while True: #este laço atualiza os estatus da unidade a cada 60s a API para uso do cliente
        temp_value = []
        temp_value.clear()
        while len(temp_value) < len(app.data_for_ping):
            value = result_queue.get()
            temp_value.append(value)
        DB(temp_value)
        time.sleep(60)
        
def system_ping():
    while True:
        global data_units
        if len(data_units) == 0:  #adiciona primeira carga de dados a lista
            data_units = app.total_unit_and_data
            serve_ping()

        db_veiifcation()    
        if len(data_units) < len(app.total_unit_and_data): # Verifica se esta faltando algo no array temp_values
            different = [element for element in app.total_unit_and_data if element not in data_units] # econtra o que esta faltando e adiciona a var different
            for value in different:
                data_units.append(value)
            serve_ping()
              
        elif len(data_units) > len(app.total_unit_and_data): # tira algo execedente da lista
            different = [element for element in data_units if element not in app.total_unit_and_data]
            for value in different:
                data_units.pop(value)
            serve_ping()

        else:
            time.sleep(60)
            continue
            
