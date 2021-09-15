from models.interfaces import BaseModel
from sqlalchemy import Column, INT, String, Float


class TokenRateModel(BaseModel):
    __tablename__ = "tbl_token_rates"
    id = Column("id", INT, primary_key=True, autoincrement=True)
    currency = Column('currency', String(5), unique=True)
    rate = Column('rate', Float)

    def as_dict(self):
        return {
            "id": str(self.id),
            "currency": self.currency,
            "rate": str(self.rate),
        }
