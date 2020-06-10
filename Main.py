import imaplib
import email
import pyttsx3
from arduino import light
from mails import *
from tkinter import*
from tkinter import messagebox
from googletrans import Translator
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
        
def read():
    global server
    speaker = pyttsx3.init()
    speaker.setProperty('rate',155)
        server.select('Inbox')
        __,mail = server.select('Inbox') 
        __,search = server.search(None, 'UNSEEN')
        num = [x for x in search[0].split()]
        for x in range(0,len(num)):  
            __,data = server.fetch(num[x],'(RFC822)')
            ___,message=data[0]
            unencoded_message = email.message_from_bytes(message)# turns the data into bytes for it to be interpreted 
            for part in unencoded_message.walk():#iterates through different parts of the email(subparts)
                if(part.get_content_type()=='text/plain'):#when text/plain is found than the message is printed
                    speaker.say(unencoded_message['From'])
                    translator = Translator()
                    result = translator.translate(part.get_payload(),src='en', dest='hi')
                    messagebox.showinfo(unencoded_message['From'],result.text)
                    speaker.say(f"says {part.get_payload()}")
                    speaker.runAndWait()
                    speaker.stop()
    
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
    mexit = Button(master,text='Exit',command=closewindow,width=10).pack()

def list():
    list = Button(master,text='Add People',command=add,width=10).pack()

def any_unseen():
    any_unseen = Button(master,text='Unseen Mail', command = anymail,width=10).pack()

def specific_unseen():
    specific_unseen = Button(master,text='Specific Mail', command =specific,width=10).pack()

def reset():
    reset = Button(master,text='Reset', command =reset_variable,width=10).pack()

def reading():
    reading = Button(master,text='Read', command =read,width=10).pack()


server()
list()
specific_unseen()
any_unseen()
reset()
reading()
exiting()
mainloop()  
    








    

