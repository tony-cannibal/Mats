##################################
# These are my imported libraries
import  sqlite3
import pandas as pd
from tkinter import filedialog as fd
import datetime
import numpy as np
from pathlib import Path
import os.path


##################################
# these are my global variables
home_dir = Path.home()
database = 'C:/Materiales/db_1.db'
temp = 'C:/Materiales/temp.csv'
cols = [
    'id',
    'maquina',
    'codigo del material',
    'nombre del material',
    'cantidad',
    'unidad',
    'area',
    'fecha',
    'mes'
    ]
meses = {
    'January':'Enero',
    'February':'Febrero',
    'March':'Marzo',
    'April':'Abril',
    'May':'Mayo',
    'June':'Junio',
    'July':'Julio',
    'August':'Agosto',
    'September':'Septiembre',
    'October':'Octubre',
    'November':'Noviembre',
    'Dicember':'Diciembre'
    }

maquinas  =  {
    'A001':'Corte M1', 'A002':'Corte M1', 'A003':'Corte M1',
    'A004':'Corte M1', 'A005':'Corte M1', 'A006':'Corte M1',
    'A007':'Corte M1', 'A008':'Corte M1', 'A009':'Corte M1',
    'A010':'Corte M1', 'A011':'Corte M1', 'A012':'Corte M1',
    }


##################################
# these are my functions
def create_main_table(database):
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS materiales
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Maquina TEXT,
    Codigo_del_material TEXT,
    Nombre_del_maetrial TEXT,
    Cantidad REAL,
    Unidad TEXT,
    area TEXT,
    fecha TEXT,
    mes TEXT
    )"""
    )
    connection.commit()
    connection.close()

def format_info(df, fecha):
    maquinas = pd.read_csv('maquinas.csv')
    df = pd.merge(df, maquinas, on='Maquina', how='left')
    date = datetime.datetime(fecha[0], fecha[1], fecha[2])
    df = df.assign(Fecha=str(date.strftime("%Y-%m-%d")))
    df = df.assign(mes=meses[date.strftime("%B")])
    df.to_csv('input.csv', index=False)
    return df, date

def open_file_cmd():
    file = input('Que fecha quieres introducir?. ')
    df = pd.read_excel(f"{home_dir}\Documents\P3\database\Materiales\{file}.xlsx")
    fecha = [int(i) for i in file.split("-")]
    df, fecha = format_info(df, fecha)    
    return df, fecha
    

def open_file():
    file_dir = fd.askopenfilename(
        initialdir=f"{home_dir}\Documents\P3\database",
        title="Open A File",
        filetypes=(("xlsx files", "*.xlsx"), ("All Files", "*.*")),
        )
    if file_dir:
        try:
            file_dir = r"{}".format(file_dir)
            df = pd.read_excel(file_dir)
            filename = file_dir[-15:-5]
            fecha = [int(i) for i in filename.split("-")]
            df = format_info(df, fecha)
            # print(df)
            return df, fecha
        except ValueError:
            print("File could not be read.")


def insert_into_main(df, database):
    df = df.to_numpy().tolist()
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.executemany(
        """
        INSERT INTO materiales (Maquina,
        Codigo_del_material,
        Nombre_del_maetrial,
        Cantidad, Unidad,
        area, fecha,
        mes) VALUES (?,?,?,?,?,?,?,?)
        """,
        df
    )
    connection.commit()
    connection.close()


def get_master():
    data = []
    conn = sqlite3.connect(database)
    c = conn.cursor()
    for i in c.execute('SELECT * FROM materiales'):
        data.append(i)
    conn.close()
    df = pd.DataFrame(data, columns=cols)
    df.to_csv('master_data.csv', index=False)
    print(df)
    return df


def combinar_material(df, date):
    df['concatenado'] = df['Area'] + '+' + df['Codigo del material'] + '+' + df['Unidad']
    excedente_anterior = os.path.exists(temp)
    if excedente_anterior == True:
        fecha_anterior = pd.read_csv(temp)
        fecha_anterior['concatenado'] = fecha_anterior['Area'] + '+' + fecha_anterior['Codigo del material'] + '+' + fecha_anterior['Unidad']
        all_mats = pd.concat([df,  fecha_anterior], axis=0)
        all_mats.to_csv('all_mats.csv', index=False)
        concatenado = all_mats.concatenado.unique()
    else:
        concatenado = df.concatenado.unique()
    cantidad_total = [ df[df['concatenado'] == i ]['Cantidad'].sum()  for i in concatenado ]
    comb = pd.DataFrame(list(zip(concatenado, cantidad_total)), columns=['concatenado', 'Total ordenado'])
    comb[['Area','Codigo del material', 'Unidad']]=comb.concatenado.str.split('+',expand=True)

    # Here we are checking for the extra and we are first checking if a file with extr exists
    if excedente_anterior == False:
        comb = comb.assign(excedente_anterior=0)
        comb['Ordenado neto'] = comb['Total ordenado']
    else:
        fecha_anterior = pd.read_csv(temp)
        comb = pd.merge(comb, fecha_anterior[['concatenado', 'Excedente']], on='concatenado', how='left')
        comb.rename(columns={'Excedente':'Excedente anterior'}, inplace=True)
        comb = comb.fillna(0)
        comb['Ordenado neto'] = np.where((comb['Total ordenado']-comb['Excedente anterior'])<0, comb['Excedente anterior'] - comb['Total ordenado'], comb['Total ordenado'] - comb['Excedente anterior'],)

    moq = pd.read_csv('moq.csv')
    comb = pd.merge(comb, moq[['Codigo del material', 'Pkg']], on='Codigo del material', how='left')
    comb['Cantidad de pkg'] = (comb['Ordenado neto'] / comb['Pkg']).apply(np.ceil)
    comb['Excedente'] = (comb['Cantidad de pkg'] * comb['Pkg']) - comb['Ordenado neto']
    comb =comb.assign(fecha=date)
    comb = comb.reindex(columns=['concatenado', 'fecha', 'Area', 'Codigo del material', 'Excedente anterior',
                                 'Total ordenado', 'Ordenado neto', 'Unidad', 'Pkg', 'Cantidad de pkg', 'Excedente'])
    comb = comb.fillna(0)
    comb.to_csv(temp, index=False)
    comb.to_csv('result.csv', index=False) 
    #print(comb)
    return comb


###################################
# The code gets excecuted here

run =1
while run ==1:
    
    choice = int(input('What do you want to do. '))
    if choice == 1:
        carga, date = open_file_cmd()
        combinar_material(carga, date)
        print(carga)
    elif choice == 2:
        print('Something else')
    elif choice ==3:
        run = 0
        print('adios')


#combinado = combinar_material(req)
