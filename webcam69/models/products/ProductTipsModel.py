from models.interfaces import InterfaceProductModel
from sqlalchemy import Column, ForeignKey, func, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ProductTipsModel(InterfaceProductModel):
    __tablename__ = "tbl_product_tips"

    id = Column('id', UUID(as_uuid=True), ForeignKey('tbl_products.id'), primary_key=True)
    recipient_wallet_id = Column(
        'recipient_wallet_id', UUID(as_uuid=True), ForeignKey('tbl_token_wallets.id')
    )
    recipient_wallet = relationship('TokenWalletModel', lazy='joined', back_populates='product_tips')
    deleted_at = Column("deleted_at", DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'ProductTips'
    }