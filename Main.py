import imaplib
import email
from arduino import light
from mails import *
from tkinter import*
from tkinter import messagebox
master = Tk()
master.geometry("400x400")
master.title("Mailing Bot")

#global
space = None
x=0
g=0



def server():
    global unseen
    global server
    with open("email.txt")as my_file:
        email = my_file.readlines()
        server = imaplib.IMAP4_SSL('imap.gmail.com')  
        server.login(email[0], email[1])  
        server.select('Inbox')     
    #ALL unseen emails
        __,server_data= server.search(None,'UNSEEN')
        unseen = [mail for mail in (server_data[0].split())]


def specific():
    global g
    with open("address.txt")as my_file_address:# reads the file
        book=my_file_address.readlines()
        print(book)
        books= book[0].split()
    global  server 
    for z in range(0,(len(books))):#len(book) 
        __,client= server.search(None,f'FROM {books[z]}')#Look for one email address at a time in the inbox
        checking= [a for a in client[0].split()]#Turns all the mail found on that email address (inbox) into a list


        for a in range (0,len(unseen)):#Filters through all the unseen mail to see if it matches one of the address
            if (unseen[a] in checking) and g ==0 :
                light('COM4','7') #arduino lights will come on,// the ports might have to be switched and the pin depending on the user
                messagebox.showinfo("New Mail!","New Mail!!")
                light('COM4','7')
                g+=1 #ensures the message box only happens ones
                break #breaks out of main loop
            else:
                continue
          
    master.after(10000, specific)#repeats the func in the backgroun every 10 sec
   
def anymail():
    global x
    global unseen
    try:
        unseen[0]
        messagebox.showinfo("Hey","You Have Pending Mail")
        light('COM4','7')
    except:
        if x == 0:
            messagebox.showinfo("Hey","You NO Have Pending Mail")
            x+=1
        master.after(1000,server)
        master.after(10000, anymail)
    
def addlist ():
    global space 
    name = (space.get())
    print(name)
    my_file_address= open("address.txt","a")
    my_file_address.write(" "+name)
    messagebox.showinfo("Alert",f"{name} has been entered")

def closewindow():
    exit()

def add():
    add = Toplevel()
    add.geometry("400x400")
    
    global name
    global space
    space= Entry(add,width= 50)
    space.pack()
    name=space.get()
    
    address = Button(add,text='Add people here',command=addlist).pack()

    texit= Button(add,text='Exit',command=add.destroy).pack()

def reset_variable():
    global g 
    g= 0
    global a 
    a = 0




















def exiting():
    mexit = Button(master,text='Exit',command=closewindow)
    mexit.pack()

def list():
    list = Button(master,text='Add People',command=add)
    list.pack()

def any_unseen():
    any_unseen = Button(master,text='Unseen Mail', command = anymail).pack()

def specific_unseen():
    specific_unseen = Button(master,text='Specific Mail', command =specific).pack()

def reset():
    reset = Button(master,text='Reset', command =reset_variable).pack()

server()
list()
specific_unseen()
any_unseen()
reset()
exiting()
mainloop()     
    








    

