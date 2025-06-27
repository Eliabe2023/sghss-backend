from app.database.database import Base, engine
from app.models import user  # vamos criar esse arquivo a seguir

# Cria todas as tabelas
print("⏳ Criando o banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Banco de dados criado com sucesso.")
