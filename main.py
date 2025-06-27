from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importações dos módulos de rotas
from app.routes import user_routes
from app.routes import patient_routes
from app.routes import professional_routes
from app.routes import appointment_routes
from app.routes import record_routes

app = FastAPI()

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de teste
@app.get("/")
def root():
    return {"message": "A API está rodando"}

# Inclusão das rotas
app.include_router(user_routes.router)
app.include_router(patient_routes.router)
app.include_router(professional_routes.router)
app.include_router(appointment_routes.router)
app.include_router(record_routes.router)

# python -m uvicorn main:app --reload para rodar a api