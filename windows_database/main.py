from materiales import *
from functions import *
from dat_functions import *


month = "junio"

database = f"C:/Materiales/database_{month}.db"



df, fecha = open_file_cmd()
df = combinar_material(df, fecha)

#print(df)