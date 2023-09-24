import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import string

directory = os.path.dirname(__file__)
path = os.path.join(directory, "serviceAccountKey.json")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def SecurityCodeCommand():
    global top
    global Label
    global SecurityCodeButton
    global EnigmaCodeButton
    global AccessButton
    def ConfirmCode():
        Code = EntryCodeSecurity.get()
        if Code != "":
            codeaccessDOC = db.collection("Crypta").document("Code")
            codesecurity = {"code": Code}
            codeaccessDOC.set(codesecurity)
            messagebox.showinfo("Successfully", f"Code : {Code}")
        else:
            messagebox.showerror("Error", "Insert Code")
    def RandomCode():
        codeaccessDOC = db.collection("Crypta").document("Code")
        characters = string.ascii_letters + string.digits
        random_code = ''.join(random.choice(characters) for _ in range(10))
        code = {"code": random_code}
        codeaccessDOC.set(code)
        messagebox.showinfo("Successfully", f"Code : {random_code}")

    def Back():
        Confirm.destroy()
        EntryCodeSecurity.destroy()
        Random.destroy()
        BBack.destroy()
        MainApp()
    doc = db.collection("Crypta").document("Code")
    data = doc.get()
    code = data.to_dict()

    code = code.get("code", "")

    Label.configure(text="Security Code")
    SecurityCodeButton.destroy()
    EnigmaCodeButton.destroy()
    AccessButton.destroy()

    Confirm = tk.Button(top)
    Confirm.place(relx=0.303, rely=0.556, height=31, width=187)
    Confirm.configure(compound='left')
    Confirm.configure(disabledforeground="#a3a3a3")
    Confirm.configure(foreground="#000000")
    Confirm.configure(highlightbackground="#d9d9d9")
    Confirm.configure(highlightcolor="black")
    Confirm.configure(pady="0")
    Confirm.configure(text='''Confirm''')
    Confirm.configure(command=ConfirmCode)

    EntryCodeSecurity = tk.Entry(top)
    EntryCodeSecurity.place(relx=0.316, rely=0.46, height=30, relwidth=0.366)
    EntryCodeSecurity.configure(background="white")
    EntryCodeSecurity.configure(disabledforeground="#a3a3a3")
    EntryCodeSecurity.configure(font="TkFixedFont")
    EntryCodeSecurity.configure(foreground="#000000")
    EntryCodeSecurity.configure(insertbackground="black")
    EntryCodeSecurity.insert(END, code)

    Random = tk.Button(top)
    Random.place(relx=0.303, rely=0.632, height=31, width=187)
    Random.configure(compound='left')
    Random.configure(disabledforeground="#a3a3a3")
    Random.configure(foreground="#000000")
    Random.configure(highlightbackground="#d9d9d9")
    Random.configure(highlightcolor="black")
    Random.configure(pady="0")
    Random.configure(text='''Random''')
    Random.configure(command=RandomCode)

    BBack = tk.Button(top)
    BBack.place(relx=0.303, rely=0.709, height=31, width=187)
    BBack.configure(compound='left')
    BBack.configure(disabledforeground="#a3a3a3")
    BBack.configure(foreground="#000000")
    BBack.configure(highlightbackground="#d9d9d9")
    BBack.configure(highlightcolor="black")
    BBack.configure(pady="0")
    BBack.configure(text='''Back''')
    BBack.configure(command=Back)

def EnigmaCodeCommand():
    try:
        combineDB = db.collection("CombineCrypta").document("Huruf")
        docTransF = db.collection("CombineCrypta").document("TranslateCrypta")
        WhisperChat = db.collection("Crypta").document("WhisperChat")

        chat_data = WhisperChat.get().to_dict().get("oldmessage", "")
        docTransFF = docTransF.get()
        translateF = docTransFF.to_dict()

        combineFDB = combineDB.get()
        combineF = combineFDB.to_dict()

        alphabet = """abcdefghijklmnopqrstuvwxyz1234567890`~!@\"'#$%^&*()-_=+[{]}\\|;:,<.>/?ABCDEFGHIJKLMNOPQRSTUVWXYZ """

        kalimatasli = ""
        for huruf in chat_data:
            translate = translateF.get(huruf, huruf)
            kalimatasli += translate

        list_karakter = list(alphabet)
        random.shuffle(list_karakter)
        hasil_acak = ''.join(list_karakter)
        Combine = (dict(zip(alphabet, list_karakter)))
        CombineTranslate = (dict(zip(list_karakter, alphabet)))

        combineDB.set(Combine)
        docTransF.set(CombineTranslate)

        combineDB = db.collection("CombineCrypta").document("Huruf")
        combineFDB = combineDB.get()
        combineF = combineFDB.to_dict()
        newcombine = ""
        for huruf in kalimatasli:
            combine = combineF.get(huruf, huruf)
            newcombine += combine

        data = WhisperChat.get()
        idchat = data.to_dict()
        idchat = idchat.get("IDChat", 0)

        newconfigure = {
            "oldmessage": newcombine,             
            "IDChat": idchat
        }
        WhisperChat.set(newconfigure)

        chat_data = WhisperChat.get().to_dict().get("oldmessage", "")
        docTransFF = docTransF.get()
        translateF = docTransFF.to_dict()

        kalimatasli = ""
        for huruf in chat_data:
            translate = translateF.get(huruf, huruf)
            kalimatasli += translate

        messagebox.showinfo("Successfully", "Enigma Changes")
    except:
        messagebox.showerror("Error", "Enigma Failed To Change")
def AccessCommand():
    global top
    global Label
    global SecurityCodeButton
    global EnigmaCodeButton
    global AccessButton

    def ConfirmAccess():
        Access = combobox.get()
        Version = EntryVersion.get()
        Message = EntryMessage.get()


        if Access == "" or Version == "" or Message == "":
            messagebox.showerror("Error", "Failed To Change Configure")
        try:
            if Access == "Block":
                newconfigureAccess = 0 

            elif Access == "Open":
                newconfigureAccess = 1
            document = db.collection("Crypta").document("Access")
            newconfigure = {
                "access": newconfigureAccess,
                "version": Version,
                "showerror": Message
            }
            document.set(newconfigure)
            messagebox.showinfo("Successfully", "Configure Change")
        except:
            messagebox.showerror("Error", "Failed To Change Configure")

    def BackCommand():
        Label.destroy()
        combobox.destroy()
        selected_label.destroy()
        AccessLabel.destroy()
        EntryVersion.destroy()
        LabelVersion.destroy()
        LabelMessage.destroy()
        EntryMessage.destroy()
        Confirm.destroy()
        BBack.destroy()
        MainApp()
    document = db.collection("Crypta").document("Access")
    doc = document.get()
    access = doc.to_dict()
    accesscrypta = access.get("access", "")
    version = access.get("version", "")
    error = access.get("showerror", "")

    if accesscrypta == 1:
        textbombox = "Open"
    elif accesscrypta == 0:
        textbombox = "Block"

    Label.configure(text="Access Control")
    SecurityCodeButton.destroy()
    EnigmaCodeButton.destroy()
    AccessButton.destroy()

    combobox = tk.StringVar()
    items = ["Open", "Block"]

    combobox = ttk.Combobox(top, values=items, state="readonly")
    combobox.set(textbombox)
    combobox.place(relx=0.358, rely=0.383,height=30, relwidth=0.282)

    combobox.bind("<<ComboboxSelected>>")

    selected_label = tk.Label(top, text="")
    selected_label.pack()

    AccessLabel = tk.Label(top, text='Access')
    AccessLabel.place(relx=0.253, rely=0.402, height=11, width=44)
    AccessLabel.configure(background="#ffffff", foreground="#000000")

    EntryVersion = tk.Entry(top)
    EntryVersion.place(relx=0.358, rely=0.46, height=30, relwidth=0.282)
    EntryVersion.configure(background="white", foreground="#000000")
    EntryVersion.insert(END, version)

    LabelVersion = tk.Label(top, text='Version')
    LabelVersion.place(relx=0.253, rely=0.479, height=11, width=44)
    LabelVersion.configure(background="#ffffff", foreground="#000000")

    LabelMessage = tk.Label(top, text='Message')
    LabelMessage.place(relx=0.24, rely=0.543, height=21, width=54)
    LabelMessage.configure(background="#ffffff", foreground="#000000")

    EntryMessage = tk.Entry(top)
    EntryMessage.place(relx=0.358, rely=0.536, height=30, relwidth=0.282)
    EntryMessage.insert(END, error)

    Confirm = tk.Button(top, text='Confirm', bg='#ffffff', fg='#000000', command=ConfirmAccess)
    Confirm.place(relx=0.295, rely=0.628, height=31, width=187)

    BBack = tk.Button(top, text='Back', bg='#ffffff', fg='#000000', command=BackCommand)
    BBack.place(relx=0.295, rely=0.708, height=31, width=187)


def MainApp():
    global top
    global Label
    global SecurityCodeButton
    global EnigmaCodeButton
    global AccessButton

    top.geometry("475x522+719+237")
    top.configure(background="#ffffff")
    top.configure(highlightbackground="#d9d9d9")
    top.configure(highlightcolor="black")
    menubar = tk.Menu(top, font="TkMenuFont", bg='#d9d9d9', fg='#000000')
    top.configure(menu=menubar)

    Label = tk.Label(top, text='Admin Control', anchor='w', bg='#ffffff', fg='#000000', compound='left', font=("arial", 30))
    Label.place(relx=0.236, rely=0.113, height=100, width=474)

    SecurityCodeButton = tk.Button(top, text='Security Code', compound='left', fg='#000000', bg='beige', padx=0, pady=0, command=SecurityCodeCommand)
    SecurityCodeButton.place(relx=0.316, rely=0.345, height=44, width=177)

    EnigmaCodeButton = tk.Button(top, text='Enigma Code', compound='left', fg='#000000', bg='beige', padx=0, pady=0, command=EnigmaCodeCommand)
    EnigmaCodeButton.place(relx=0.316, rely=0.458, height=44, width=177)

    AccessButton = tk.Button(top, text='Access', compound='left', foreground='#000000', background='beige', disabledforeground='#a3a3a3', highlightbackground='#d9d9d9', highlightcolor='black', pady='0', command=AccessCommand)
    AccessButton.place(relx=0.316, rely=0.575, height=44, width=177)


def GuiApp():
    global top
    global CodeInput
    global LabelSecurityCode
    global ConfirmButton
    global WarningLabel
    def SecurityCheck():
        global CodeInput
        global LabelSecurityCode
        global ConfirmButton
        global WarningLabel
        CodeInputEntry = CodeInput.get()
        if CodeInputEntry == "MIMIW":
            CodeInput.destroy()
            LabelSecurityCode.destroy()
            ConfirmButton.destroy()
            WarningLabel.destroy()
            MainApp()
        else:
            WarningLabel.configure(text='''Wrong Code!!!''')
    top = tk.Tk()
    top.geometry("475x522+719+237")
    top.title("Admin Control")
    top.configure(background="#ffffff")
    top.configure(highlightbackground="#d9d9d9")
    top.configure(highlightcolor="black")
    menubar = tk.Menu(top, font="TkMenuFont", bg='#d9d9d9', fg='#000000')
    top.configure(menu=menubar)

    CodeInput = tk.Entry(top, background="white", disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black", selectbackground="#c4c4c4", selectforeground="black", show="*")
    CodeInput.place(relx=0.35, rely=0.467, relwidth=0.3, height=30)

    LabelSecurityCode = tk.Label(top, text='Security Code', bg="#ffffff", fg="#000000", anchor='w')
    LabelSecurityCode.place(relx=0.415, rely=0.406)

    ConfirmButton = tk.Button(top, text='Confirm', bg='beige', fg='black', command=SecurityCheck)
    ConfirmButton.place(relx=0.35, rely=0.594, relwidth=0.3)

    WarningLabel = tk.Label(top, text="", background="#ffffff", foreground="#ff0000")
    WarningLabel.place(relx=0.415, rely=0.543, height=21, width=84)

    top.mainloop()

if __name__ == "__main__":
    GuiApp()