from models.interfaces import InterfaceProductModel
from sqlalchemy import Column, ForeignKey, func, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime


class ProductRefillModel(InterfaceProductModel):
    __tablename__ = "tbl_refill_products"

    id = Column('id', UUID(as_uuid=True), ForeignKey('tbl_products.id'), primary_key=True)
    token_package_id = Column(
        'token_package_id',
        ForeignKey('tbl_token_packages.id'),
    )
    token_package = relationship('TokenPackageModel', back_populates='product_refill', lazy='joined')
    payment_id = Column('payment_id', String)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())
    deleted_at = Column("deleted_at", DateTime, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'ProductRefill'
    }