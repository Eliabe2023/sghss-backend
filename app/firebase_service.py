import firebase_admin
from firebase_admin import credentials, firestore

# Inicialização do Firebase (garante que só inicialize uma vez)
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            "C:/Users/ELIABE/Desktop/TRABALHO FINAL/sghss-backend-limpo/ajudaclick10-firebase-adminsdk-foyn8-e7e1c25575.json"
        )
        firebase_admin.initialize_app(cred)
        print("✅ Firebase inicializado com sucesso.")
    else:
        print("ℹ Firebase já estava inicializado.")
    db = firestore.client()
except Exception as e:
    print(f"❌ Erro ao inicializar Firebase: {e}")
    db = None

# ---------------- USERS ----------------
def get_all_users():
    try:
        users_ref = db.collection("users").stream()
        return [u.to_dict() | {"id": u.id} for u in users_ref]
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []

def get_user_by_id(user_id):
    try:
        doc = db.collection("users").document(user_id).get()
        return doc.to_dict() | {"id": doc.id} if doc.exists else None
    except Exception as e:
        print(f"Erro ao buscar usuário {user_id}: {e}")
        return None

def add_user(user):
    try:
        return db.collection("users").add(user)
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")
        return None

def delete_user(user_id):
    try:
        db.collection("users").document(user_id).delete()
    except Exception as e:
        print(f"Erro ao excluir usuário {user_id}: {e}")

# ---------------- PACIENTES ----------------
def get_all_pacientes():
    try:
        pacientes_ref = db.collection("pacientes").stream()
        return [p.to_dict() | {"id": p.id} for p in pacientes_ref]
    except Exception as e:
        print(f"Erro ao listar pacientes: {e}")
        return []

def get_paciente(paciente_id):
    try:
        doc = db.collection("pacientes").document(paciente_id).get()
        return doc.to_dict() | {"id": doc.id} if doc.exists else None
    except Exception as e:
        print(f"Erro ao buscar paciente {paciente_id}: {e}")
        return None

def get_paciente_por_cpf(cpf):
    try:
        query = db.collection("pacientes").where(filter=("cpf", "==", cpf)).stream()
        return [p.to_dict() | {"id": p.id} for p in query]
    except Exception as e:
        print(f"Erro ao buscar paciente por CPF {cpf}: {e}")
        return []

def add_paciente(nome, idade, cpf):
    try:
        return db.collection("pacientes").add({
            "nome": nome,
            "idade": idade,
            "cpf": cpf
        })
    except Exception as e:
        print(f"Erro ao adicionar paciente: {e}")
        return None

def update_paciente(paciente_id, nome, idade, cpf):
    try:
        db.collection("pacientes").document(paciente_id).update({
            "nome": nome,
            "idade": idade,
            "cpf": cpf
        })
    except Exception as e:
        print(f"Erro ao atualizar paciente {paciente_id}: {e}")

def delete_paciente(paciente_id):
    try:
        db.collection("pacientes").document(paciente_id).delete()
    except Exception as e:
        print(f"Erro ao excluir paciente {paciente_id}: {e}")

# ---------------- PROFISSIONAIS ----------------
def get_all_profissionais():
    try:
        prof_ref = db.collection("profissionais").stream()
        return [p.to_dict() | {"id": p.id} for p in prof_ref]
    except Exception as e:
        print(f"Erro ao listar profissionais: {e}")
        return []

def get_profissional(profissional_id):
    try:
        doc = db.collection("profissionais").document(profissional_id).get()
        return doc.to_dict() | {"id": doc.id} if doc.exists else None
    except Exception as e:
        print(f"Erro ao buscar profissional {profissional_id}: {e}")
        return None

def get_profissional_por_crm(crm):
    try:
        query = db.collection("profissionais").where(filter=("crm", "==", crm)).stream()
        return [p.to_dict() | {"id": p.id} for p in query]
    except Exception as e:
        print(f"Erro ao buscar profissional por CRM {crm}: {e}")
        return []

def add_profissional(nome, especialidade, crm):
    try:
        return db.collection("profissionais").add({
            "nome": nome,
            "especialidade": especialidade,
            "crm": crm
        })
    except Exception as e:
        print(f"Erro ao adicionar profissional: {e}")
        return None

def update_profissional(profissional_id, nome, especialidade, crm):
    try:
        db.collection("profissionais").document(profissional_id).update({
            "nome": nome,
            "especialidade": especialidade,
            "crm": crm
        })
    except Exception as e:
        print(f"Erro ao atualizar profissional {profissional_id}: {e}")

def delete_profissional(profissional_id):
    try:
        db.collection("profissionais").document(profissional_id).delete()
    except Exception as e:
        print(f"Erro ao excluir profissional {profissional_id}: {e}")

# ---------------- CONSULTAS ----------------
def get_all_consultas():
    try:
        consultas_ref = db.collection("consultas").stream()
        return [c.to_dict() | {"id": c.id} for c in consultas_ref]
    except Exception as e:
        print(f"Erro ao listar consultas: {e}")
        return []

def add_consulta(paciente_id, profissional_id, data, horario):
    try:
        return db.collection("consultas").add({
            "paciente_id": paciente_id,
            "profissional_id": profissional_id,
            "data": data,
            "horario": horario
        })
    except Exception as e:
        print(f"Erro ao adicionar consulta: {e}")
        return None

def delete_consulta(consulta_id):
    try:
        db.collection("consultas").document(consulta_id).delete()
    except Exception as e:
        print(f"Erro ao excluir consulta {consulta_id}: {e}")

# ---------------- PRONTUÁRIOS ----------------
def get_all_prontuarios():
    try:
        pront_ref = db.collection("prontuarios").stream()
        return [p.to_dict() | {"id": p.id} for p in pront_ref]
    except Exception as e:
        print(f"Erro ao listar prontuários: {e}")
        return []

def add_prontuario(paciente_id, descricao, data):
    try:
        return db.collection("prontuarios").add({
            "paciente_id": paciente_id,
            "descricao": descricao,
            "data": data
        })
    except Exception as e:
        print(f"Erro ao adicionar prontuário: {e}")
        return None

def delete_prontuario(prontuario_id):
    try:
        db.collection("prontuarios").document(prontuario_id).delete()
    except Exception as e:
        print(f"Erro ao excluir prontuário {prontuario_id}: {e}")
