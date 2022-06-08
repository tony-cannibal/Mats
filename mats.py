import pandas as pd
import os.path

def check_file():
    file = os.path.exists('C:/Users/YR PROD ORDER/AppData/Materiales/Mayo.csv')
    column_names = ['Maquina', 'Codigo del material', 'Nombre del material',
                    'Cantidad', 'Unidad', 'Area', 'Fecha','Mes']
    if file == False:
        df = pd.DataFrame(columns = column_names)
        df.to_csv('C:/Users/YR PROD ORDER/AppData/Materiales/Mayo.csv')
    else:
        df = pd.read_csv('C:/Users/YR PROD ORDER/AppData/Materiales/Mayo.csv')
    return df
