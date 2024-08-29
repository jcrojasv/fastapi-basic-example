import uuid
import logging
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError
from config.aws import s3_client, AWS_S3_BUCKET
from schemas.contract_schema import ContractCreate, ContractResponse
from models.contract_model import Contract as ContractModel
from repositories.contract_repository import ContractRepository
from schemas.contract_schema import ContractSearchParams


class ContractService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ContractRepository(db)
        self.logger = logging.getLogger(__name__)


    def get_contracts(self, params: ContractSearchParams):
        try:
            self.logger.info(f"[ContractService] Getting contracts with params: {params}")
            contracts, total = self.repository.get_contracts(params)
            return contracts, total
        except Exception as e:
            self.logger.error("[ContractService] An error occurred while fetching contracts", exc_info=True)
            raise HTTPException(status_code=500, detail="An error occurred while fetching contracts")


    def create_contract_with_file(self, contract_data: ContractCreate, file: UploadFile) -> ContractResponse:
        try:
            self.logger.info(f"[ContractService] Creating contract: {contract_data}")

            file_url = self.upload_file_to_s3(file)
            contract_instance = ContractModel(
                name=contract_data.name,
                nature=contract_data.nature,
                project=contract_data.project,
                path=file_url
            )
            saved_contract = self.repository.create_contract(contract_instance)

            self.logger.info(f"[ContractService] Contract created successfully: {saved_contract.id}")

            return ContractResponse.from_orm(saved_contract)
        except Exception as e:
            self.logger.error("[ContractService] An error occurred while creating the contract", exc_info=True)
            raise


    def upload_file_to_s3(self, file: UploadFile) -> str:
        try:
            self.logger.info(f"[ContractService] Init Uploading file to S3")
            s3_file_path = f"contracts/{self.generate_file_name(file)}"
            self.logger.info(f"[ContractService] Uploading file to S3: {s3_file_path}")
            s3_client.upload_fileobj(file.file, AWS_S3_BUCKET, s3_file_path)
            self.logger.info(f"[ContractService] File uploaded to S3 successfully: {s3_file_path}")
        except ClientError as e:
            self.logger.error("[ContractService] File upload to S3 failed", exc_info=True)
            raise HTTPException(status_code=500, detail="File upload to S3 failed.")

        return f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{s3_file_path}"

    def generate_file_name (self, file: UploadFile) -> str:
        try:
            self.logger.info(f"[ContractService] Generating unique file name for: {file.filename}")
            file_extension = file.filename.split(".")[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            return unique_filename
        except ClientError as e:
            self.logger.error("[ContractService] An error occurred while generating file name", exc_info=True)
            raise HTTPException(status_code=500, detail="An error occurred while generating file name.")

    def get_contract_by_id(self, contract_id: int) -> ContractResponse:
        try:
            self.logger.info(f"[ContractService] Getting contract by ID: {contract_id}")
            contract = self.repository.get_contract_by_id(contract_id)
            if contract is None:
                raise HTTPException(status_code=404, detail="Contract not found")
            return ContractResponse.from_orm(contract)
        except HTTPException as e:
            raise e
        except Exception as e:
            self.logger.error("[ContractService] An error occurred while getting the contract", exc_info=True)
            raise HTTPException(status_code=500, detail="An error occurred while getting the contract")

    def delete_contract(self, contract_id: int) -> bool:
        try:
            self.logger.info(f"[ContractService] Deleting contract by ID: {contract_id}")
            deleted = self.repository.delete_contract(contract_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Contract not found")
            self.logger.info(f"[ContractService] Contract deleted successfully: {contract_id}")
            return True
        except HTTPException as e:
            raise e
        except Exception as e:
            self.logger.error("[ContractService] An error occurred while deleting the contract", exc_info=True)
            raise HTTPException(status_code=500, detail="An error occurred while deleting the contract")