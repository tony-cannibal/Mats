##################################
# These are my imported libraries
import  sqlite3
import pandas as pd
from tkinter import filedialog as fd
import datetime
import numpy as np
from pathlib import Path
from pathlib import Path


##################################
# these are my global variables
home_dir = Path.home()
database = 'C:/Materiales/db_1.db'
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


##################################
# these are my functions
def create_maintable(database):
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute(
        """
    CREATE TABLE materiales
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


def open_file():
    filename = fd.askopenfilename(
        initialdir=f"{home_dir}\Desktop\MATERIALES\P",
        title="Open A File",
        filetypes=(("xlsx files", "*.xlsx"), ("All Files", "*.*")),
    )
    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_excel(filename)
            print("File Read Correctly")
            return df
        except ValueError:
            print("File could not be read.")


def format_info(df):
    maquinas = pd.read_csv('maquinas.csv')
    df = pd.merge(df, maquinas, on='Maquina', how='left')
    # ar = input("Area: ")
    # df = df.assign(area=ar)
    fecha = [int(i) for i in input("fecha: ").split("-")]
    date = datetime.datetime(fecha[0], fecha[1], fecha[2])
    mes = date.strftime("%B")
    df = df.assign(fecha=str(date.strftime("%Y-%m-%d")))
    df = df.assign(mes=mes)
    df.to_csv('df.csv', index=False)
    return df


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
    #df.to_csv('master_data.csv', index=False)
    #print(df)
    return df


def combinar_material(df):
    moq = pd.read_csv('moq.csv')
    df['concatenado'] = df['area'] + '+' + df['codigo del material'] + '+' + df['fecha'] + '+' + df['unidad']
    concatenado = df.concatenado.unique()
    cantidad_total = [ df[df['concatenado'] == i ]['cantidad'].sum()  for i in concatenado ]
    comb = pd.DataFrame(list(zip(concatenado, cantidad_total)), columns=['concatenado', 'total ordenado'])
    comb[['area','codigo del material', 'fecha', 'unidad']]=comb.concatenado.str.split('+',expand=True)
    comb = comb.drop('concatenado', axis=1)
    comb = pd.merge(comb, moq[['codigo del material', 'packing']], on='codigo del material', how='left')
    comb['cantidad de pkg'] = (comb['total ordenado'] / comb['packing']).apply(np.ceil)
    comb['excedente'] = (comb['cantidad de pkg'] * comb['packing']) - comb['total ordenado']
    comb = comb.reindex(columns=['fecha',  'area','codigo del material',  'total ordenado', 'unidad',
       'packing', 'cantidad de pkg', 'excedente'])
    comb = comb.fillna(0)
    comb.to_csv('combinado.csv', index=False) 
    #print(comb)
    return comb


###################################
# The code gets excecuted here
materiales = format_info(open_file())
print(materiales)

