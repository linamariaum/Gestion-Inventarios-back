# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.base_class import Base

# class Client(Base):
#     __tablename__ = "clients"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     password_hash = Column(String)

#     inventory = relationship("Inventory", back_populates="client")
