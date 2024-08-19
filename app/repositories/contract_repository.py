from sqlalchemy.orm import Session
from config.database import SessionLocal
from models import contract_model
from contextlib import contextmanager
from schemas.contract_schema import ContractSearchParams

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

    def get_contracts(self, params: ContractSearchParams):
        query = self.db.query(contract_model.Contract)

        if params.search:
            search_term = f"%{params.search}%"
            query = query.filter(
                contract_model.Contract.name.like(search_term) |
                contract_model.Contract.nature.like(search_term) |
                contract_model.Contract.project.like(search_term)
            )

        if params.name:
            query = query.filter(contract_model.Contract.name.like(f"%{params.name}%"))
        if params.nature:
            query = query.filter(contract_model.Contract.nature.like(f"%{params.nature}%"))
        if params.project:
            query = query.filter(contract_model.Contract.project.like(f"%{params.project}%"))

        total = query.count()
        contracts = query.offset((params.page - 1) * params.page_size).limit(params.page_size).all()

        return contracts, total