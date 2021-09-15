from models import BaseModel
from sqlalchemy import Column, Integer, DateTime, func
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class TokenWalletModel(BaseModel):
    __tablename__ = 'tbl_token_wallets'
    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column("user_id", UUID(as_uuid=True))
    balance = Column("balance", Integer, default=0)
    transactions = relationship('TransactionModel', back_populates='owner_wallet')
    product_tips = relationship('ProductTipsModel', back_populates='recipient_wallet')
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())
    deleted_at = Column("deleted_at", DateTime, nullable=True)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "balance": self.balance,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }