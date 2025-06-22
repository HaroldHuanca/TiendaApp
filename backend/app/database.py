from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión
DATABASE_URL = "mariadb+mariadbconnector://root:@localhost:3306/tiendadb"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase de ayuda para manejar la conexión
class DatabaseManager:
    def __enter__(self):
        self.session = SessionLocal()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()