import sqlite3
from functions import cols
import pandas as pd





def deploy_database(database):
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS input
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Maquina TEXT,
    Codigo_del_material TEXT,
    Nombre_del_maetrial TEXT,
    Cantidad REAL, Unidad TEXT,
    area TEXT, fecha TEXT, mes TEXT
    )"""
    )
    connection.commit()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS materiales_combinados
    (
    fecha TEXT, 
    area TEXT,
    codigo TEXT PRIMARY KEY,
    excedente_anterior TEXT,
    total_ordenado REAL, 
    ordenado_neto REAL,
    unidad TEXT, 
    pkg REAL, 
    cantidad_de_pkg REAL,
    excedente REAL
    )"""
    )
    connection.commit()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS materiales_totales
    (
    area TEXT,
    codigo TEXT PRIMARY KEY,
    excedente_anterior TEXT,
    total_ordenado REAL,
    ordenado_neto REAL,
    unidad TEXT, 
    pkg REAL, 
    cantidad_de_pkg REAL,
    excedente REAL
    )"""
    )
    connection.commit()
    connection.close()

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

def get_master(database):
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