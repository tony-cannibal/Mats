from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pandas as pd
import datetime



def callback():
    global data_f
    
    filename= fd.askopenfilename(initialdir='C:/Users/YR PROD ORDER/',
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
    data_f = df

def save_file():
    data_f.to_csv('C:/Users/YR PROD ORDER/Documents/test.csv')

def button_call():
    save_file(data_f)



root = Tk()
root.geometry('400x400')    


my_button = Button(root, text='Click to Open File', command=callback)
my_button.pack(pady=10)

save_button = Button(root, text='To CSV', command=save_file)
save_button.pack()

my_label = Label(root, text='')
my_label.pack()

root.mainloop()
