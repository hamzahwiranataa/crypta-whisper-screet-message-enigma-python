import os.path
import firebase_admin
from firebase_admin import credentials, firestore
import random
import time
import os

directory = os.path.dirname(__file__)
path = os.path.join(directory, "serviceAccountKey.json")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()

while True:
    combineDB = db.collection("CombineCrypta").document("EnigmaCode")
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
    time.sleep(300)