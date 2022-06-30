from materiales import *
from functions import *
from dat_functions import *
import os

month = "junio"

database = f"C:/Materiales/database_{month}.db"

run = True
os.system('cls')
print('Bienvenido\n')
os.system('pause')
while run == True:
    os.system('cls')
    
    print('''
Que deseas hacer?\n
Crear Base de Datos : 1
Introducir Material : 2
Entregar Material   : 3 
Bajar Actualidad    : 4
Salir               : 5\n
    ''')
   
    choice = input()
    if choice == '1':
        os.system('cls')

        deploy_database(database)

        print('\n')
        os.system('pause')
        
    elif choice == '2':
        os.system('cls')
        print('Do chice 2\n')
        os.system('pause')
    
    elif choice == '3':
        entregar = True
        while entregar == True:
            os.system('cls')
            print('Do choice 3\n')
            os.system('pause')
    
    elif choice == '4':
        os.system('cls')
        print('Do choice 4\n')
        os.system('pause')
    
    elif choice == '5':
        os.system('cls')
        print('Adios\n')
        os.system('pause')
        run = False
    
    else:
        os.system('cls')
        print('Esa no es una opcion valida.')
        print('Vuelve a elegir\n')
        os.system('pause')