from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime
from datetime import datetime

class Profit(Base):

    __tablename__ = "profit"

    id = Column(Integer, primary_key=True)
    companyName = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    drink = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)



    def __init__(self, companyName, quantity, drink):
        self.companyName = companyName
        self.quantity = quantity
        self.drink = drink
        self.date_created = datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['companyName'] = self.companyName
        dict['quantity'] = self.quantity
        dict['drink'] = self.drink
        dict['date_created'] =self.date_created

        return dict
