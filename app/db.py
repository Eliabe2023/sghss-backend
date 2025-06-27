import firebase_admin
from firebase_admin import credentials, firestore

cred_path = os.path.join(os.getcwd(), "ajudaclick10-firebase-adminsdk-foyn8-e7e1c25575.json")

if not os.path.exists(cred_path):
    raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {cred_path}")

db = firestore.client()
