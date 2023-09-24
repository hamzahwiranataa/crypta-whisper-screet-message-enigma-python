import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
import os
import tkinter as tk
import firebase_admin
import threading
from firebase_admin import credentials, firestore
from tkinter import messagebox
import time

directory = os.path.dirname(__file__)
path = os.path.join(directory, "data\service\service.json")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def SendText():
    global EntrySendMessage
    global CheckName

    Message = EntrySendMessage.get()
    Message = str(Message)

    if Message != "":
        docCrypta = db.collection("CombineCrypta").document("Combine")
        docCrypt = docCrypta.get()
        datacrypta = docCrypt.to_dict()
        CryptaExt = ""
        for huruf in Message:
            crypta = datacrypta.get(huruf, huruf) 
            CryptaExt += crypta

        CryptaCodeName = ""
        for huruf in CheckName:
            crypta = datacrypta.get(huruf, huruf) 
            CryptaCodeName += crypta

        doc_ref = db.collection("Crypta").document("WhisperChat")

        sendtextstyledefault = " : "
        sendtextstyle = ""
        for huruf in sendtextstyledefault:
            crypta = datacrypta.get(huruf, huruf)
            sendtextstyle += crypta

        doc = doc_ref.get()
        idchat = doc.to_dict()
        idchat = idchat.get("IDChat", "")
        existing_data = doc_ref.get().to_dict()

        ChatIDUpdate = int(idchat) + 1
        ChatIDUpdate = str(ChatIDUpdate)

        oldmessage = doc.to_dict()
        oldmessage = oldmessage.get("oldmessage", "")   
        addmessage = (f"{oldmessage}{CryptaCodeName}{sendtextstyle}{CryptaExt}\n")
        new_chat = {
            ChatIDUpdate : f"{CryptaCodeName}{sendtextstyle}{CryptaExt}",
            "IDChat" : ChatIDUpdate,
            "oldmessage" : addmessage
        }

        existing_data.update(new_chat)

        doc_ref.set(existing_data)
        EntrySendMessage.delete(0, END)
    
def main():
    global top
    global tray
    global SendText
    global CheckName
    global EntrySendMessage

    def ChatReciver():
        nextchat = 1

        doc_ref = db.collection("Crypta").document("WhisperChat")
        doc = doc_ref.get()
        data = doc.to_dict()
        idchat = data.get("IDChat", 0)
        idchat = int(idchat)
        nextchat = nextchat + idchat

        while True:
            doc = doc_ref.get()
            data = doc.to_dict()
            idchat = data.get("IDChat", 0)
            idchat = int(idchat)
            
            if idchat >= nextchat:
                chat_data = data.get(str(idchat), "")

                doctranslate = db.collection("CombineCrypta").document("TranslateCrypta")
                doc = doctranslate.get()
                datatranslate = doc.to_dict()
                kalimat_asli = ""

                for huruf in chat_data:
                    translate = datatranslate.get(huruf, huruf) 
                    kalimat_asli += translate

                MessageBox.configure(state="normal")
                MessageBox.insert(tk.END, kalimat_asli + "\n")
                MessageBox.configure(state="disabled")
                
                nextchat = idchat + 1

            time.sleep(0.7)


    doctranslate = db.collection("CombineCrypta").document("TranslateCrypta")
    doc = doctranslate.get()
    datatranslate = doc.to_dict()
    
    doc_ref = db.collection("Crypta").document("WhisperChat")
    doc = doc_ref.get()
    data = doc.to_dict()
    chatwhisper = data.get("oldmessage", "")

    kalimat_asli = ""
    for huruf in chatwhisper:
        translate = datatranslate.get(huruf, huruf)
        kalimat_asli += translate

    chat = kalimat_asli

    top = tk.Tk()
    top.geometry("592x786+671+120")
    top.title("Crypta Whisper")
    top.configure(background="#ffffff")
    top.configure(highlightbackground="#d9d9d9")
    top.configure(highlightcolor="black")

    MessageBox = tk.Text(top, background="white", font="TkTextFont", foreground="black", wrap="word")
    MessageBox.place(relx=0.017, rely=0.064, relheight=0.855, relwidth=0.961)
    MessageBox.insert(tk.END, chat)
    MessageBox.configure(state="disabled")

    scrollbar = tk.Scrollbar(top, command=MessageBox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    MessageBox.config(yscrollcommand=scrollbar.set)

    EntrySendMessage = tk.Entry(top, background="white", font="TkFixedFont", foreground="black")
    EntrySendMessage.place(relx=0.017, rely=0.94, height=34, relwidth=0.75)

    ButtonSend = tk.Button(top, text='Send', background="#ffffff", foreground="#000000", command=SendText)
    ButtonSend.place(relx=0.777, rely=0.94, height=34, width=117)

    CodeNameText = tk.Label(top, text='Code Name : ' + CheckName, background="#ffffff", foreground="#000000")
    CodeNameText.place(relx=0.017, rely=0.013, height=31, width=172)

    menubar = tk.Menu(top,font="TkMenuFont",bg="#d9d9d9",fg="#000000")
    top.configure(menu = menubar)
    recivechat = threading.Thread(target=ChatReciver)
    recivechat.daemon = True
    recivechat.start()

    top.mainloop()

def InputCodeName():
    global Label1
    global CodeNameEntry
    global PasswordNext
    def PasswordCheck():
        global Nameloweer
        document_ref = db.collection("CryptaCodeName").document(Nameloweer)
        doc = document_ref.get()
        data = doc.to_dict()
        CheckName = data.get("name", "")
        CheckPassword = data.get("password", "")

        global PasswordEntry
        Password = PasswordEntry.get()

        if Password == "":
            messagebox.showerror("Error", "Password Kosong")

        else:
            if CheckPassword != "":
                if Password == CheckPassword:
                    root.destroy()
                    main()
                else:
                    messagebox.showerror("Error", "Password Salah")

            elif CheckPassword == "":
                updatepassword = {
                    "name" : CheckName,
                    "password" : Password,
                    "access" : 1
                }
                db.collection("CryptaCodeName").document(CheckName).set(updatepassword)
                root.destroy()
                main()

    def CodeNameNext():
        global Name
        global Label1
        global CodeNameEntry
        global Nameloweer

        Name = CodeNameEntry.get()
        Nameloweer = Name.lower()

        if Name != "":
            try:
                global CheckPassword
                global CheckName
                document_ref = db.collection("CryptaCodeName").document(Nameloweer)
                doc = document_ref.get()
                data = doc.to_dict()
                CheckName = data.get("name", "")
                CheckPassword = data.get("password", "")
                CheckAccses = data.get("access", "")
                if CheckName:
                    if CheckAccses != 0:
                        global PasswordEntry
                        Label1.configure(text="Password")
                        CodeNameEntry.destroy()
                        Button1.destroy()

                        PasswordEntry = tk.Entry(root, show="*", background="white", disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000", insertbackground="black")
                        PasswordEntry.place(relx=0.191, rely=0.446, height=30, relwidth=0.615)

                        ConfirmPassword = tk.Button(root, text="Confirm", activebackground="beige", activeforeground="black", background="#ffffff", compound='left' , disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", command=PasswordCheck)
                        ConfirmPassword.place(relx=0.338, rely=0.606, height=34, width=97)

                    else:
                        messagebox.showwarning("Info", "Nama Ini Tidak Memiliki Akses")

            except:
                NewName = {
                    "name" : f"{Name}",
                    "password" : "",
                    "access" : 0
                }
                db.collection("CryptaCodeName").document(Nameloweer).set(NewName)
                messagebox.showwarning("Info", "Nama Ini Tidak Memiliki Akses")
            
                
    root = tk.Tk()
    root.geometry("299x231+820+410")
    root.title("Crypta Security")
    root.configure(background="#ffffff")

    Label1 = tk.Label(root, text="Code Name", anchor='w', background="#ffffff", compound='left', disabledforeground="#a3a3a3", foreground="#000000")
    Label1.place(relx=0.375, rely=0.346, height=17, width=74)

    CodeNameEntry = tk.Entry(root, background="white", disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000", insertbackground="black")
    CodeNameEntry.place(relx=0.191, rely=0.446, height=30, relwidth=0.615)

    Button1 = tk.Button(root, text="Confirm", activebackground="beige", activeforeground="black", background="#ffffff", compound='left' , disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", command=CodeNameNext)
    Button1.place(relx=0.338, rely=0.606, height=34, width=97)

    warning_label = tk.Label(root, text="", fg="red")
    warning_label.pack()

    root.resizable(False, False)
    root.mainloop()

bgcolor = '#d9d9d9'  # X11 color: 'gray85'
fgcolor = '#000000'  # X11 color: 'black'

def maingui():
    global CodeInput
    global WarningLabel
    def SecurityCheck():
        global WarningLabel
        global CodeInput
        CodeMy = CodeInput.get()
        document_ref = db.collection("Crypta").document("Code")
        doc = document_ref.get()
        try:
            data = doc.to_dict()
            code = data.get("code", "")

            if code != CodeMy:
                WarningLabel.configure(text='''Wrong Code!!!''')
                    
            else:
                top.destroy()
                InputCodeName()

        except:
            WarningLabel.configure(text='''Wrong Code!!!''')
    top = tk.Tk()
    top.geometry("342x411+789+311")
    top.title("Crypta Security")
    top.configure(background="#ffffff")
    top.configure(highlightbackground="#d9d9d9")
    top.configure(highlightcolor="black")

    menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg=fgcolor)
    top.configure(menu=menubar)

    CodeInput = tk.Entry(top, background="white", disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black", selectbackground="#c4c4c4", selectforeground="black", show="*")
    CodeInput.place(relx=0.202, rely=0.467, height=30, relwidth=0.596)


    LabelSecurityCode = tk.Label(top, text='Security Code', bg='#ffffff', fg='#000000')
    LabelSecurityCode.place(relx=0.377, rely=0.406, height=20, width=84)

    ConfirmButton = tk.Button(top, text='Confirm', bg='beige', fg='black', command=SecurityCheck)
    ConfirmButton.place(relx=0.313, rely=0.594, height=24, width=127)

    WarningLabel = tk.Label(top, text="", background="#ffffff", foreground="#ff0000")
    WarningLabel.place(relx=0.377, rely=0.543, height=21, width=84)


    top.resizable(False, False)
    top.mainloop()

if __name__ == "__main__":
    maingui()