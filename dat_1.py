import sqlite3
import pandas as pd
from tkinter import filedialog as fd
import datetime


def create_maintable():
    connection = sqlite3.connect("/home/luis/Documents/Python/database/database.db")
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
        initialdir="/home/luis/Documents/Python/database",
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
    ar = input("Area: ")
    df = df.assign(area=ar)
    fecha = [int(i) for i in input("fecha: ").split("-")]
    date = datetime.datetime(fecha[0], fecha[1], fecha[2])
    mes = date.strftime("%B")
    date = date.strftime("%Y-%m-%d")
    date = str(date)
    df = df.assign(fecha=date)
    df = df.assign(mes=mes)
    return df


def inser_into_main(df):
    df = df.to_numpy().tolist()
    connection = sqlite3.connect(
        "/home/luis/Documents/Python/database/database.db"
    )
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
        df,
    )

    connection.commit()
    connection.close()


create_maintable()

df = open_file()

df = format_info(df)

inser_into_main(df)
