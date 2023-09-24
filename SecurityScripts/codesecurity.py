import firebase_admin
from firebase_admin import credentials, firestore
import random
import time
import os
import string

directory = os.path.dirname(__file__)
path = os.path.join(directory, "serviceAccountKey.jso")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()

while True:
    db = firestore.client()
    codeaccessDOC = db.collection("Crypta").document("Code")

    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(10))
    code = {"code": random_code}
    codeaccessDOC.set(code)
    print(str(random_code))
    time.sleep(3600)