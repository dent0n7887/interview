from models.interfaces import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class InterfaceProductModel(BaseModel):
    __tablename__ = "tbl_products"

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product = Column(String)
    transaction = relationship('TransactionModel', back_populates='product')

    __mapper_args__ = {"polymorphic_on": product, 'with_polymorphic': '*'}