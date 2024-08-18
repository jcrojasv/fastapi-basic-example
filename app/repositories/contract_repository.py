from sqlalchemy.orm import Session
from config.database import SessionLocal
from models import contract_model
from contextlib import contextmanager

@contextmanager
def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


class ContractRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_contracts(self, name: str = None, nature: str = None, project: str = None, page: int = 1, page_size: int = 10):
        query = self.db.query(contract_model.Contract)

        if name:
            query = query.filter(contract_model.Contract.name.like(f"%{name}%"))
        if nature:
            query = query.filter(contract_model.Contract.nature.like(f"%{nature}%"))
        if project:
            query = query.filter(contract_model.Contract.project.like(f"%{project}%"))

        total = query.count()
        contracts = query.offset((page - 1) * page_size).limit(page_size).all()

        return contracts, total