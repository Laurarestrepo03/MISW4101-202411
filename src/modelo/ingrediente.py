from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base


# Modelo de un ingrediente:
class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    unidad = Column(String)
    valor = Column(Float)
    sitioCompra = Column(String)
    recetas = relationship('Receta', secondary='ingrediente_receta')

class IngredienteReceta(Base):
    __tablename__ = 'ingrediente_receta'

    id = Column(Integer, primary_key=True)

    ingrediente_id = Column(
        Integer,
        ForeignKey('ingrediente.id'))

    receta_id = Column(
        Integer,
        ForeignKey('receta.id'))
    
    cantidad = Column(Integer)


