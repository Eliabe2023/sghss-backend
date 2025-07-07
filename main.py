from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import (
    user_routes,
    patient_routes,
    professional_routes,
    appointment_routes,
    record_routes,
    view_routes
)

from app import firebase_service as db

app = FastAPI()

# Arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usuário admin padrão
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
session = {}

# ----------------------------
# Login e Dashboard
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if session.get("user"):
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        session["user"] = {"username": username}
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Credenciais inválidas."})

@app.get("/logout")
def logout():
    session.pop("user", None)
    return RedirectResponse("/")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": session["user"]})

@app.get("/api/status")
async def status():
    return {"message": "A API está rodando"}

# ----------------------------
# Pacientes
# ----------------------------
@app.get("/pacientes", response_class=HTMLResponse)
async def listar_pacientes(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    pacientes = db.get_all_pacientes()
    return templates.TemplateResponse("pacientes.html", {"request": request, "pacientes": pacientes, "user": session["user"]})

@app.get("/pacientes/novo", response_class=HTMLResponse)
async def novo_paciente_form(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    return templates.TemplateResponse("novo_paciente.html", {"request": request, "user": session["user"]})

@app.post("/pacientes/novo")
async def cadastrar_paciente(nome: str = Form(...), idade: int = Form(...), cpf: str = Form(...)):
    db.add_paciente(nome, idade, cpf)
    return RedirectResponse("/pacientes", status_code=303)

@app.get("/pacientes/editar/{paciente_id}", response_class=HTMLResponse)
async def editar_paciente_form(request: Request, paciente_id: str):
    if not session.get("user"):
        return RedirectResponse("/")
    paciente = db.get_paciente(paciente_id)
    return templates.TemplateResponse("editar_paciente.html", {"request": request, "paciente": paciente, "user": session["user"]})

@app.post("/pacientes/editar/{paciente_id}")
async def editar_paciente(paciente_id: str, nome: str = Form(...), idade: int = Form(...), cpf: str = Form(...)):
    db.update_paciente(paciente_id, nome, idade, cpf)
    return RedirectResponse("/pacientes", status_code=303)

@app.get("/pacientes/excluir/{paciente_id}")
async def excluir_paciente(paciente_id: str):
    db.delete_paciente(paciente_id)
    return RedirectResponse("/pacientes", status_code=303)

# ----------------------------
# Profissionais
# ----------------------------
@app.get("/profissionais", response_class=HTMLResponse)
async def listar_profissionais(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    profissionais = db.get_all_profissionais()
    return templates.TemplateResponse("profissionais.html", {"request": request, "profissionais": profissionais, "user": session["user"]})

@app.get("/profissionais/novo", response_class=HTMLResponse)
async def novo_profissional_form(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    return templates.TemplateResponse("novo_profissional.html", {"request": request, "user": session["user"]})

@app.post("/profissionais/novo")
async def cadastrar_profissional(nome: str = Form(...), especialidade: str = Form(...), crm: str = Form(...)):
    db.add_profissional(nome, especialidade, crm)
    return RedirectResponse("/profissionais", status_code=303)

@app.get("/profissionais/editar/{profissional_id}", response_class=HTMLResponse)
async def editar_profissional_form(request: Request, profissional_id: str):
    if not session.get("user"):
        return RedirectResponse("/")
    profissional = db.get_profissional(profissional_id)
    return templates.TemplateResponse("editar_profissional.html", {"request": request, "profissional": profissional, "user": session["user"]})

@app.post("/profissionais/editar/{profissional_id}")
async def editar_profissional(profissional_id: str, nome: str = Form(...), especialidade: str = Form(...), crm: str = Form(...)):
    db.update_profissional(profissional_id, nome, especialidade, crm)
    return RedirectResponse("/profissionais", status_code=303)

@app.get("/profissionais/excluir/{profissional_id}")
async def excluir_profissional(profissional_id: str):
    db.delete_profissional(profissional_id)
    return RedirectResponse("/profissionais", status_code=303)

# ----------------------------
# Consultas
# ----------------------------
@app.get("/consultas", response_class=HTMLResponse)
async def listar_consultas(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    consultas = db.get_all_consultas()
    return templates.TemplateResponse("consultas.html", {"request": request, "consultas": consultas, "user": session["user"]})

@app.get("/consultas/novo", response_class=HTMLResponse)
async def nova_consulta_form(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    pacientes = db.get_all_pacientes()
    profissionais = db.get_all_profissionais()
    return templates.TemplateResponse("nova_consulta.html", {"request": request, "pacientes": pacientes, "profissionais": profissionais, "user": session["user"]})

@app.post("/consultas/novo")
async def cadastrar_consulta(paciente_id: str = Form(...), profissional_id: str = Form(...), data: str = Form(...), horario: str = Form(...)):
    db.add_consulta(paciente_id, profissional_id, data, horario)
    return RedirectResponse("/consultas", status_code=303)

@app.get("/consultas/excluir/{consulta_id}")
async def excluir_consulta(consulta_id: str):
    db.delete_consulta(consulta_id)
    return RedirectResponse("/consultas", status_code=303)

# ----------------------------
# Prontuários
# ----------------------------
@app.get("/prontuarios", response_class=HTMLResponse)
async def listar_prontuarios(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    prontuarios = db.get_all_prontuarios()
    return templates.TemplateResponse("prontuarios.html", {"request": request, "prontuarios": prontuarios, "user": session["user"]})

@app.get("/prontuarios/novo", response_class=HTMLResponse)
async def novo_prontuario_form(request: Request):
    if not session.get("user"):
        return RedirectResponse("/")
    pacientes = db.get_all_pacientes()
    return templates.TemplateResponse("novo_prontuario.html", {"request": request, "pacientes": pacientes, "user": session["user"]})

@app.post("/prontuarios/novo")
async def cadastrar_prontuario(paciente_id: str = Form(...), descricao: str = Form(...), data: str = Form(...)):
    db.add_prontuario(paciente_id, descricao, data)
    return RedirectResponse("/prontuarios", status_code=303)

@app.get("/prontuarios/excluir/{prontuario_id}")
async def excluir_prontuario(prontuario_id: str):
    db.delete_prontuario(prontuario_id)
    return RedirectResponse("/prontuarios", status_code=303)

# ----------------------------
# Rotas externas
# ----------------------------
app.include_router(user_routes.router)
app.include_router(patient_routes.router)
app.include_router(professional_routes.router)
app.include_router(appointment_routes.router, prefix="/appointments")
app.include_router(record_routes.router, prefix="/records")
app.include_router(view_routes.router)

for route in app.routes:
    print("ROTA REGISTRADA:", route.path)
