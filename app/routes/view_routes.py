from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import app.firebase_service as db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Listar usuários
@router.get("/views/users", response_class=HTMLResponse)
async def list_users(request: Request):
    users = db.get_all_users()
    return templates.TemplateResponse("list_users.html", {"request": request, "users": users})

# Listar pacientes
@router.get("/views/pacientes", response_class=HTMLResponse)
async def list_pacientes(request: Request):
    pacientes = db.get_all_pacientes()
    return templates.TemplateResponse("list_pacientes.html", {"request": request, "pacientes": pacientes})

# Listar profissionais
@router.get("/views/profissionais", response_class=HTMLResponse)
async def list_profissionais(request: Request):
    profissionais = db.get_all_profissionais()
    return templates.TemplateResponse("list_profissionais.html", {"request": request, "profissionais": profissionais})

# Listar agendamentos
@router.get("/views/agendamentos", response_class=HTMLResponse)
async def list_agendamentos(request: Request):
    agendamentos = db.get_all_agendamentos()
    return templates.TemplateResponse("list_agendamentos.html", {"request": request, "agendamentos": agendamentos})

# Listar prontuários
@router.get("/views/prontuarios", response_class=HTMLResponse)
async def list_prontuarios(request: Request):
    prontuarios = db.get_all_prontuarios()
    return templates.TemplateResponse("list_prontuarios.html", {"request": request, "prontuarios": prontuarios})
