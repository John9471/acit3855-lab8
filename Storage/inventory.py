from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime
from datetime import datetime

class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    contents = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)



    def __init__(self, name, contents, price):
        self.name = name
        self.contents = contents
        self.price = price
        self.date_created = datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['contents'] = self.contents
        dict['price'] = self.price
        dict['date_created'] =self.date_created

        return dict