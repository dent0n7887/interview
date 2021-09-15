from models.interfaces import BaseModel
from sqlalchemy import Column, INT, String
from sqlalchemy.orm import relationship


class TokenPackageModel(BaseModel):
    __tablename__ = "tbl_token_packages"
    id = Column("id", INT, primary_key=True, autoincrement=True)
    name = Column('name', String)
    token_amount = Column('token_amount', INT)
    token_price = Column('token_price', INT)
    product_refill = relationship('ProductRefillModel', back_populates='token_package')

    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "token_amount": str(self.token_amount),
            "token_price": str(self.token_price),
        }