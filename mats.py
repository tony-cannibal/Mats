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


    df_1 = pd.read_excel('C:/Users/YR PROD ORDER/Desktop/MATERIALES/P/M2/m2 2022.06.06.xlsx')
    df_2 = pd.read_excel('C:/Users/YR PROD ORDER/Desktop/MATERIALES/P/M2/m2 2022.06.07.xlsx')

    concatenated = pd.concat([df_1, df_2], axis=0)

    concatenated.to_excel('C:/Users/YR PROD ORDER/Desktop/MATERIALES/P/M2/concatenated.xlsx', index=False)                         
