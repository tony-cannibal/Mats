from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pandas as pd
import datetime


# Wee need to use this class to set up variables so that
# we can return data from functions called from tkinter
# buttons. This is so we dont use global variables.
class CustomVarable:
    def __init__ (self):
        self.returnedVariable = None
    def returnVariable (self, x):
        self.returnedVariable = x

def callback():
    filename= fd.askopenfilename(
        initialdir='C:/Users/YR PROD ORDER/',
        title='Open A File',
        filetype=(('xlsx files', '*.xlsx'), ('All Files', '*.*'))
        ) 
    if filename:
        try:
            filename = r'{}'.format(filename)
            df = pd.read_excel(filename)
            my_label.config(text='File Read Correctly')
        except ValueError:
            my_label.config(text='File Could Not Be Read!')
    df = df.assign(area='M2')
    date = datetime.datetime(2022, 6, 8)
    df = df.assign(fecha=date)
    df = df.assign(mes=date.strftime('%B'))
    return df

def save_file(data_f):
    print(data_f.returnedVariable)
    data_f.returnedVariable.to_csv('C:/Users/YR PROD ORDER/Documents/test.csv')

def button_call():
    save_file(data_f)

# Here we are creating an instance of our CustomVariable class
# so that we can use it later on to get data from button callbacks
my_variable = CustomVarable()

root = Tk()
root.geometry('400x400')    

data_f = []

my_button = Button(root, text='Click to Open File', command=lambda:my_variable.returnVariable(callback()))
my_button.pack(pady=10)

save_button = Button(root, text='To CSV', command=lambda:save_file(my_variable ))
save_button.pack()

my_label = Label(root, text='')
my_label.pack()

root.mainloop()
