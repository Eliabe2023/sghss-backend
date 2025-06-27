import firebase_admin
from firebase_admin import credentials, firestore
import os

# Verifica se o app já foi inicializado para evitar ValueError
if not firebase_admin._apps:
    cred_path = os.path.join(os.getcwd(), "ajudaclick10-firebase-adminsdk-foyn8-e7e1c25575.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
