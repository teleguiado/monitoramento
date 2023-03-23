import os
import datetime
import csv

def grava(conexao, name_unit):
    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    arquivo = f"{data_atual}.csv"
    caminho = os.path.join(os.getcwd(),"log", name_unit)
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    caminho_completo = os.path.join(caminho, arquivo)
    arquivo_exite = os.path.isfile(caminho_completo)
     
    with open(caminho_completo, "a", newline='') as file:
        fieldnames = [name_unit]
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        if not arquivo_exite:
            writer.writeheader()
        conexao = conexao.rstrip(",")
        writer.writerow({fieldnames[0]: conexao})
        
def calculate_time(start, stop):
    
    # calculating unavailabilty
    # time and converting it in seconds
    difference = stop - start
    seconds = float(str(difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]
