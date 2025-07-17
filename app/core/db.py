from sqlmodel import create_engine, Session, select

from app.core.config import settings
from app.models.rol_model import Rol

class Database():
    def __init__(self):
        
        if not hasattr(self.__class__, '_engine'):
            self.__class__._engine = create_engine(settings.db_url)
        self._engine = self.__class__._engine
        
        
    def get_db(self):
        db = Session(self._engine)
        try:
            yield db
        finally:
            db.close()
            
    def init_db(self):
        with Session(self._engine) as session:
            roles = session.exec(select(Rol)).all()
            
            if not roles:
                session.add(Rol(nombre='user'))
                session.add(Rol(nombre='admin'))
                session.commit()

database = Database()
db = database.get_db
