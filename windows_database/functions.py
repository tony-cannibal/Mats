import pandas as pd
from tkinter import filedialog as fd
import datetime
import numpy as np
from pathlib import Path
import os




home_dir = Path.home()

temp = 'C:/Materiales/temp.csv'

path = f'{home_dir}\\Documents\\P3\\database\\Materiales\\'

cols = [
    'id',
    'maquina',
    'codigo',
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


def format_info(df, fecha):
    maquinas = pd.read_csv('maquinas.csv')
    df = pd.merge(df, maquinas, on='Maquina', how='left')
    date = datetime.datetime(fecha[0], fecha[1], fecha[2])
    df = df.assign(fecha=str(date.strftime("%Y-%m-%d")))
    df = df.assign(mes=meses[date.strftime("%B")])
    # df.to_csv('input.csv', index=False)
    df = df.rename(columns={
        'Maquina':'maquina', 'Nombre del material':'nombre', 'Codigo del material':'codigo', 
        'Cantidad':'cantidad', 'Unidad':'unidad', 'Area':'area'
    })
    print(df)
    return df, date

def open_file_cmd():
    os.system('cls')
    print('Que fecha quieres introducir?. ')
    dir_list = os.listdir(path)
    f_list = {}
    for i in dir_list:
        print(f'{i} - {i[-7:-5]}')
        f_list[i[-7:-5]]=i
    dec = input()
    file = f_list[dec]
    df = pd.read_excel(f"{home_dir}\Documents\P3\database\Materiales\{file}")
    fecha = [int(i) for i in file[:-5].split("-")]
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
            return df, fecha
        except ValueError:
            print("File could not be read.")



def combinar_material(df, date):
    df['concatenado'] = df['area'] + '+' + df['codigo'] + '+' + df['unidad']
    excedente_anterior = os.path.exists(temp)
    if excedente_anterior == True:
        fecha_anterior = pd.read_csv(temp)
        fecha_anterior['concatenado'] = fecha_anterior['area'] + '+' + fecha_anterior['codigo'] + '+' + fecha_anterior['unidad']
        all_mats = pd.concat([df,  fecha_anterior], axis=0)
        all_mats.to_csv('all_mats.csv', index=False)
        concatenado = all_mats.concatenado.unique()
    else:
        concatenado = df.concatenado.unique()
    cantidad_total = [ df[df['concatenado'] == i ]['cantidad'].sum()  for i in concatenado ]
    comb = pd.DataFrame(list(zip(concatenado, cantidad_total)), columns=['concatenado', 'total ordenado'])
    comb[['area','codigo', 'unidad']]=comb.concatenado.str.split('+',expand=True)
    # Here we are checking for the extra and we are first checking if a file with extr exists
    if excedente_anterior == False:
        comb = comb.assign(excedente_anterior=0)
        comb['ordenado neto'] = comb['total ordenado']
    else:
        fecha_anterior = pd.read_csv(temp)
        comb = pd.merge(comb, fecha_anterior[['concatenado', 'excedente']], on='concatenado', how='left')
        comb.rename(columns={'excedente':'excedente anterior'}, inplace=True)
        comb = comb.fillna(0)
        comb['ordenado neto'] = np.where((
            comb['total ordenado']-comb['excedente anterior'])<0,
            comb['excedente anterior'] - comb['total ordenado'],
            comb['total ordenado'] - comb['excedente anterior'])
    moq = pd.read_csv('moq.csv')
    comb = pd.merge(comb, moq[['codigo', 'pkg']], on='codigo', how='left')
    comb['cantidad de pkg'] = (comb['ordenado neto'] / comb['pkg']).apply(np.ceil)
    comb['excedente'] = (comb['cantidad de pkg'] * comb['pkg']) - comb['ordenado neto']
    comb =comb.assign(fecha=date)
    # comb = comb.assign(Fecha=meses[str(date.strftime("%Y-%m-%d")))]
    comb = comb.reindex(
        columns=['concatenado',
                 'fecha', 'area', 'codigo', 'excedente anterior', 'total ordenado',
                 'ordenado neto', 'unidad', 'pkg', 'cantidad de pkg', 'excedente'])
    comb = comb.fillna(0)
    comb.to_csv(temp, index=False)
    comb.to_csv('result.csv', index=False) 
    #print(comb)
    return comb