from models.interfaces import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Enum, func, INT
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enums import TransactionStatusEnum, TransactionTypeEnum
from sqlalchemy.orm import relationship


class TransactionModel(BaseModel):
    __tablename__ = "tbl_transactions"
    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_type = Column('transaction_type', Enum(TransactionTypeEnum))
    owner_wallet_id = Column('owner_wallet_id', UUID(as_uuid=True), ForeignKey('tbl_token_wallets.id'))
    owner_wallet = relationship('TokenWalletModel', lazy='joined', back_populates='transactions')
    product_id = Column('product_id', ForeignKey('tbl_products.id'))
    product = relationship('InterfaceProductModel', lazy='joined', back_populates='transaction')
    total_token_price = Column('amount', INT)
    status = Column('status', Enum(TransactionStatusEnum), default=TransactionStatusEnum.CREATED)
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())
    deleted_at = Column("deleted_at", DateTime, nullable=True)

    def as_dict(self):
        return {
            "id": str(self.id),
            "transaction_type": self.transaction_type.value,
            "owner_wallet_id": str(self.owner_wallet_id),
            "product_id": str(self.product_id),
            "total_token_price": str(self.total_token_price),
            "status": self.status.value,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "deleted_at": str(self.deleted_at)
        }