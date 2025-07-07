import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializa o Firebase (caminho do seu JSON de credenciais)
cred = credentials.Certificate("ajudaclick10-firebase-adminsdk-foyn8-e7e1c25575.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Dados fictícios
pacientes = [
    {"name": "João da Silva", "age": 30},
    {"name": "Maria Oliveira", "age": 25},
    {"name": "Carlos Souza", "age": 40},
    {"name": "Ana Paula Lima", "age": 35},
    {"name": "Bruno Costa", "age": 28},
]

profissionais = [
    {"name": "Dr. Pedro Henrique"},
    {"name": "Dra. Larissa Martins"},
    {"name": "Dr. Rafael Dias"},
    {"name": "Dra. Juliana Alves"},
    {"name": "Dr. Lucas Pereira"},
]

# Adiciona pacientes
for p in pacientes:
    db.collection("patients").add(p)

# Adiciona profissionais
for p in profissionais:
    db.collection("professionals").add(p)

# Adiciona consultas e prontuários
for i in range(5):
    appointment = {
        "patient_name": pacientes[i % len(pacientes)]["name"],
        "professional_name": profissionais[i % len(profissionais)]["name"],
        "date": datetime.now().isoformat()
    }
    db.collection("appointments").add(appointment)

    record = {
        "patient_name": pacientes[i % len(pacientes)]["name"],
        "description": f"Prontuário automático {i + 1}",
        "created_at": datetime.now().isoformat()
    }
    db.collection("records").add(record)

print("Firestore populado com sucesso!")
