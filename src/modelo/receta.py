from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tiempo = Column(String)
    personas = Column(Integer)
    calorias = Column(Float)
    preparacion = Column(String)
    ingredientes = relationship('Ingrediente', secondary='ingrediente_receta')
