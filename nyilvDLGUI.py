import time
import requests
import re
import os
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def limitKariSzam(*args):
    value = kariszam.get()
    if len(value) > 4: kariszam.set(value[:4])

def browse_button():
    hova = filedialog.askdirectory()
    if hova == "":
        folder_path.set('Még nincs kiválasztva')
    else:
        folder_path.set(hova)
        lbl4.config(fg="green")

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def printtext():
    kari = e.get()
    hova = lbl4.cget("text")
    if hova != "Még nincs kiválasztva" and kari != "":
        uzenet.set('Letöltés folyamatban, várjál türelemmel, szólok ha kész...')
        lbl1.update_idletasks()
        letoltes(kari, hova)
    else:
        messagebox.showerror("Hú, baj van", 'Hát az van, hogy vagy a karakterszámot vagy a könyvtárat nem adtad meg. Kalandod itt véget ér :-( de ne add fel, próbáld újra!')

def letoltes(kari, hova):
    tfdlheader = {'User-Agent': 'Nyilvanos fordulo letolto 1.0'}
    r = requests.get('http://beholder.hu/?m=tf&in=karakter.php&karakter=TF' + kari, headers=tfdlheader)
    
    forcsik = re.findall('(\d*\..forduló)', r.text)
    reinforcsik = re.findall('Reinkarnálás előtti fordulók', r.text)
	
    if len(forcsik) > 0:
        createFolder(hova + '/' + kari + '/')    
        forcsik = [s.replace('. forduló', '') for s in forcsik]
    
        for forcsi in forcsik:
            r = requests.get('http://www.beholder.hu/?m=tf&in=fordulo20.php&karakter=TF' + kari + '&fordulo=' + forcsi, headers=tfdlheader)
            file = open(hova + '/' + kari + '/' + kari + '-' + forcsi + '.html', "wb")
            file.write(r.content)
            file.close()
        uzenet.set(kari + ' karakter nyilvános fordulói letöltve (' + str(len(forcsik)) + ' forduló)')
    
    if len(reinforcsik) > 0:
        rein = requests.get('http://beholder.hu/?m=tf&in=karakter.php&karakter=TF' + kari + '&reinkarnalt=1', headers=tfdlheader)
        reinforcsik = re.findall('(\d*\..forduló)', rein.text)
        if len(reinforcsik) > 0:
            createFolder(hova + '/' + kari + 'reink/')
            reinforcsik = [s.replace('. forduló', '') for s in reinforcsik]
            
            for forcsi in reinforcsik:
                r = requests.get('http://www.beholder.hu/?m=tf&in=fordulo20.php&karakter=TF' + kari + '&fordulo=' + forcsi + '&reinkarnalt=1', headers=tfdlheader)
                file = open(hova + '/' + kari + 'reink/' + kari + '-' + forcsi + '.html', "wb")
                file.write(r.content)
                file.close()
            uzenet.set(kari + ' reinkarnált karakter nyilvános fordulói letöltve (' + str(len(reinforcsik)) + ' forduló)')

    messagebox.showinfo("Info", 'Oké készen vagyunk!')
    root.destroy()

root = Tk()
root.title('TF nyilvános forduló letöltő csodacucc')
root.geometry("500x200")
root.resizable(0,0)

lbl1 = Label(root,text='Írd ide a karakterszámát annak a karakternek, akinek a nyilvános fordulóit le akarod tölteni:')
lbl1.grid(row=0, columnspan=2)

kariszam = StringVar()
kariszam.trace('w', limitKariSzam)

e = Entry(root,width=4,textvariable=kariszam)
e.grid(row=1, columnspan=2)
e.focus_set()

lbl2 = Label(root,text='Válaszd ki a könyvtárat ahova menteni akarod a fordulókat:')
lbl2.grid(row=2, columnspan=2)

folder_path = StringVar()
folder_path.set('Még nincs kiválasztva')

button2 = Button(text="Könyvtár kiválasztása", command=browse_button)
button2.grid(row=3, columnspan=2)

lbl3 = Label(root,text='Kiválasztott könyvtár: ')
lbl3.grid(row=4, column=0)
lbl4 = Label(root,textvariable=folder_path, fg="red", anchor=W, width=25)
lbl4.grid(row=4, column=1)

b = Button(root,text='Oké, mehet!',command=printtext)
b.grid(row=5, columnspan=2, padx=10, pady=10)

uzenet = StringVar()
lbl5 = Label(root,textvariable=uzenet, anchor=W)
lbl5.grid(row=6, columnspan=2)

root.mainloop()
