'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
import math
from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.ingrediente import Ingrediente
from src.modelo.ingrediente import IngredienteReceta
from src.modelo.receta import Receta
from src.modelo.declarative_base import engine, Base, session
from sqlalchemy import asc
from sqlalchemy import desc
import re
from sqlalchemy import and_


class LogicaRecetario(FachadaRecetario):
    EVENTO_AGREGAR_RECETA = 0

    EVENTO_EDITAR_RECETA = 1

    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_recetas(self):
        # Equivale a poner en SQL: SELECT * FROM receta ORDER BY receta ASC:
        recetas = [elem.__dict__ for elem in session.query(Receta).order_by(asc(Receta.nombre)).all()]
        return recetas

    def dar_receta(self, id_receta):
        # Es la lista de recetas ordenadas por nombre:
        recetas = self.dar_recetas()
        try:
            return recetas[id_receta]
        except:
            return recetas[id_receta - 1]

    def validar_crear_editar_receta(self, id_receta, nombre, tiempo, personas, calorias, preparacion, modo):
        mensaje_error = ""
        # Expresión regular para el formato de hora "HH:MM:SS"
        patron = r'^\d{2}:\d{2}:\d{2}$'

        # Comprobar si la receta para agregar ya existe en las recetas:
        receta_existente = session.query(Receta).filter_by(nombre=nombre).first()
        if receta_existente is not None:
            recetas = self.dar_recetas()
            id_repetido = next((i for i in range(len(recetas)) if recetas[i]["nombre"] == receta_existente.nombre),
                               None)

        # Comprobar que sean numeros:
        try:
            if nombre == "":
                mensaje_error = "El nombre de la receta no puede tener un valor vacio"
            elif (not isinstance(nombre, str)) or (nombre.isdigit()):
                mensaje_error = "El nombre de la receta debe ser un valor de cadena de caracteres"
            elif tiempo == "":
                mensaje_error = "El tiempo de la receta no puede estar vacio"
            elif (not isinstance(tiempo, str)) or (not re.match(patron, tiempo)):
                mensaje_error = "El tiempo de la receta no tiene el formato correcto"
            elif personas == "":
                mensaje_error = "El número de personas de la receta no puede estar vacio"
            elif int(personas) <= 0:
                mensaje_error = "El número de personas de la receta debe ser un numero positivo mayor que 0."
            elif calorias == "":
                mensaje_error = "El número de calorias de la receta no puede estar vacio"
            elif float(calorias) <= 0:
                mensaje_error = "El número de calorias de la receta debe ser un numero positivo mayor que 0."
            elif receta_existente:
                if modo == self.EVENTO_AGREGAR_RECETA or (
                        modo == self.EVENTO_EDITAR_RECETA and id_receta != id_repetido):
                    mensaje_error = f"Ya existe una receta con el nombre '{nombre}'"
            elif preparacion == "":
                mensaje_error = "La preparacion de la receta no puede tener un valor vacio"
            elif (not isinstance(preparacion, str)) or (preparacion.isdigit()):
                mensaje_error = "La preparacion de la receta debe ser un valor de cadena de caracteres"
        except ValueError as e:
            if "int" in str(e):
                mensaje_error = "El número de personas debe ser un valor numérico"
            if "float" in str(e):
                mensaje_error = "El número de calorias debe ser un valor numérico"
            return mensaje_error
        return mensaje_error

    def crear_receta(self, nombre, tiempo, personas, calorias, preparacion):
        if self.validar_crear_editar_receta(-1, nombre, tiempo, personas, calorias, preparacion,
                                            self.EVENTO_AGREGAR_RECETA) == "":
            recetaNueva = Receta(nombre=nombre, tiempo=tiempo, personas=personas, calorias=calorias,
                                 preparacion=preparacion)
            session.add(recetaNueva)
            session.commit()
            return True
        else:
            return False

    def editar_receta(self, id_receta, nombre, tiempo, personas, calorias, preparacion):
        """
           Método para editar una receta existente en el recetario

        Args:
        id_receta (int): El identificador único de la receta a editar en la lista de recetas ordenadas.
        nombre (str): El nuevo nombre de la receta.
        tiempo (int): El nuevo tiempo de preparación de la receta en minutos.
        personas (int): El nuevo número de personas para las que está destinada la receta.
        calorias (int): El nuevo valor calórico de la receta.
        preparacion (str): Los nuevos pasos de preparación de la receta.
        modo (int): El modo del metodo borrar o editar.

        Returns:
        bool: True si la receta se editó exitosamente, False si no se encontró la receta con el ID dado.
        """
        receta = self.dar_receta(id_receta)
        id_orig = receta['id']
        busqueda = receta
        if busqueda:
            if self.validar_crear_editar_receta(id_receta, nombre, tiempo, personas, calorias, preparacion,
                                                modo=self.EVENTO_EDITAR_RECETA) == "":
                # Receta anterior:
                receta = session.query(Receta).filter_by(id=id_orig).first()
                receta.nombre = nombre
                receta.tiempo = tiempo
                receta.personas = personas
                receta.calorias = calorias
                receta.preparacion = preparacion
                session.commit()
                return True
            else:
                return False
        else:
            return False

    def eliminar_receta(self, id_receta):
        del self.recetas[id_receta]

    def dar_ingredientes(self):
        # Equivale a en SQL poner: SELECT * FROM ingrediente ORDER BY nombre ASC, unidad ASC, sitioCompra ASC:
        ingredientes = [elem.__dict__ for elem in session.query(Ingrediente).order_by(
            asc(Ingrediente.nombre),
            asc(Ingrediente.unidad),
            asc(Ingrediente.sitioCompra)).all()]
        return ingredientes

    def dar_ingrediente(self, id_ingrediente):
        ingredientes = self.dar_ingredientes()
        try:
            return ingredientes[id_ingrediente]
        except:
            return ingredientes[id_ingrediente - 1]

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra, modo, id_ingrediente):
        mensaje_error = ""

        # Comprobar si la receta para agregar ya existe en las recetas:
        ingrediente_existente = session.query(Ingrediente).filter(
            and_(Ingrediente.nombre == nombre, Ingrediente.unidad == unidad)).first()

        if id_ingrediente != -1:  # Solo entra a este if en modo edicion
            id_db = self.dar_ingrediente(id_ingrediente)['id']

        # Comprobar que sean numeros:
        try:
            if nombre == "":
                mensaje_error = "El nombre del ingrediente no puede tener un valor vacio"
            elif (not isinstance(nombre, str)) or (nombre.isdigit()):
                mensaje_error = "El nombre del ingrediente debe ser un valor de cadena de caracteres"
            elif unidad == "":
                mensaje_error = "La unidad del ingrediente no puede estar vacio"
            elif (not isinstance(unidad, str)) or (unidad.isdigit()):
                mensaje_error = "La unidad del ingrediente debe ser un valor de cadena de caracteres"
            elif valor == "":
                mensaje_error = "El valor de la unidad del ingrediente no puede estar vacio"
            elif float(valor) <= 0:
                mensaje_error = "El valor de la unidad del ingrediente debe ser un numero positivo mayor que 0."
            elif sitioCompra == "":
                mensaje_error = "El sitio de compra del ingrediente no puede estar vacio"
            elif (not isinstance(sitioCompra, str)) or (sitioCompra.isdigit()):
                mensaje_error = "El sitio de compra del ingrediente debe ser un valor de cadena de caracteres"
            elif ingrediente_existente:
                if modo == "crear" or (modo == "editar" and ingrediente_existente.id != id_db):
                    mensaje_error = f"Ya existe un ingrediente con el nombre '{nombre}' y la unidad '{unidad}'"
        except ValueError as e:
            mensaje_error = "El valor de la unidad debe ser un número"
            return mensaje_error
        return mensaje_error

    def crear_ingrediente(self, nombre, unidad, valor, sitioCompra):
        if self.validar_crear_editar_ingrediente(nombre, unidad, valor, sitioCompra, "crear", -1) == "":
            ingredienteNuevo = Ingrediente(nombre=nombre, unidad=unidad, valor=valor, sitioCompra=sitioCompra)
            session.add(ingredienteNuevo)
            session.commit()
            return True
        else:
            return False

    def editar_ingrediente(self, id_ingrediente, nombre, unidad, valor, sitioCompra):
        id_ingrediente = self.dar_ingrediente(id_ingrediente)['id']
        busqueda = self.dar_ingrediente(id_ingrediente)
        if busqueda:
            if self.validar_crear_editar_ingrediente(nombre, unidad, valor, sitioCompra, "editar",
                                                     id_ingrediente) == "":
                ingrediente = session.query(Ingrediente).filter(Ingrediente.id == id_ingrediente).first()
                ingrediente.nombre = nombre
                ingrediente.unidad = unidad
                ingrediente.valor = valor
                ingrediente.sitioCompra = sitioCompra
                session.commit()
                return True
            else:
                return False
        else:
            return False

    def eliminar_ingrediente(self, id_ingrediente):
        try:
            # Buscar el ingrediente por su id
            ingrediente = self.dar_ingrediente(id_ingrediente)

            # Datos del ingrediente:
            nombre_ingrediente = ingrediente['nombre']
            unidad = ingrediente['unidad']
            valor = ingrediente['valor']
            sitioCompra = ingrediente['sitioCompra']

            ingrediente = session.query(Ingrediente).filter(
                and_(
                    Ingrediente.nombre == nombre_ingrediente,
                    Ingrediente.unidad == unidad,
                    Ingrediente.valor == valor,
                    Ingrediente.sitioCompra == sitioCompra
                )
            ).first()

            # ID del ingrediente de la base de datos:
            id_ingrediente = ingrediente.id

            # Si se encontró el ingrediente, eliminarlo de la base de datos
            if ingrediente:
                # Si el ingrediente está asociado a una receta NO se puede eliminar:
                existe = session.query(IngredienteReceta).filter(
                    IngredienteReceta.ingrediente_id == id_ingrediente).all()
                if not existe:
                    session.delete(ingrediente)
                    session.commit()
                    return True
            return False
        except:
            return False

    def dar_ingredientes_receta(self, id_receta):
        id_receta = self.dar_receta(id_receta)['id']
        ingredientes_bd = session.query(Ingrediente).filter(
            Ingrediente.recetas.any(Receta.id.in_([id_receta]))).order_by(
            asc(Ingrediente.nombre),
            asc(Ingrediente.unidad),
            asc(Ingrediente.sitioCompra)).all()
        ingredientes = []
        for elem in ingredientes_bd:
            cantidad = session.query(IngredienteReceta).filter(and_(IngredienteReceta.ingrediente_id == elem.id,
                                                                    IngredienteReceta.receta_id == id_receta)).first().cantidad
            ingredientes.append({'ingrediente': elem.nombre, 'unidad': elem.unidad, 'cantidad': cantidad})
        return ingredientes

    def dar_ingrediente_receta(self, id_ingrediente_receta):
        ing_receta = session.query(IngredienteReceta).filter(
            IngredienteReceta.id == id_ingrediente_receta).first().__dict__
        return ing_receta

    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        if self.validar_crear_editar_ingReceta(receta, ingrediente, cantidad, "agregar", -1) == "":
            receta = session.query(Receta).filter(Receta.nombre == receta['nombre']).first()
            ingrediente = session.query(Ingrediente).filter(
                and_(Ingrediente.nombre == ingrediente['nombre'], Ingrediente.unidad == ingrediente['unidad'])).first()

            if ingrediente is not None and receta is not None:
                ingrediente_receta = IngredienteReceta(
                    ingrediente_id=ingrediente.id,  # ID del ingrediente
                    receta_id=receta.id,  # ID de la receta
                    cantidad=cantidad  # Cantidad del ingrediente en la receta
                )
                session.add(ingrediente_receta)

                # receta.ingredientes.append(ingrediente)
                session.commit()
                return True
            else:
                return False
        else:
            return False

    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        id_ingrediente_receta = self.dar_ingrediente_receta(id_ingrediente_receta)['id']
        busqueda = self.dar_ingrediente_receta(id_ingrediente_receta)

        if busqueda:
            if self.validar_crear_editar_ingReceta(receta, ingrediente, cantidad, "editar",
                                                   id_ingrediente_receta) == "":
                ing_receta = session.query(IngredienteReceta).filter(
                    IngredienteReceta.id == id_ingrediente_receta).first()
                ing_receta.receta_id = receta['id']
                ing_receta.ingrediente_id = ingrediente['id']
                ing_receta.cantidad = cantidad
                session.commit()
                return True
            else:
                return False
        else:
            return False

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        indice_en_receta = 0
        iteracion = 0
        for ingrediente_receta in self.ingredientes_recetas:
            if ingrediente_receta['receta'] == receta['receta']:
                if indice_en_receta == id_ingrediente_receta:
                    del self.ingredientes_recetas[iteracion]

                indice_en_receta += 1

            iteracion += 1

    def validar_crear_editar_ingReceta(self, receta, ingrediente, cantidad, modo, id_ingrediente_receta):
        mensaje_error = ""
        receta_busc = session.query(Receta).filter(Receta.nombre == receta['nombre']).first()
        ingrediente_busc = session.query(Ingrediente).filter(and_(Ingrediente.nombre == ingrediente['nombre'],
                                                                  Ingrediente.unidad == ingrediente['unidad'])
                                                             ).first()
        ingrediente_receta_existente = session.query(IngredienteReceta).filter(
            and_(IngredienteReceta.ingrediente_id == ingrediente_busc.id,
                 IngredienteReceta.receta_id == receta_busc.id)).first()
        if id_ingrediente_receta != -1:  # Solo entra a este if en modo edicion
            id_db = self.dar_ingrediente_receta(id_ingrediente_receta)['id']

        try:
            if cantidad == "":
                mensaje_error = "La cantidad no puede ser vacio."
            elif int(cantidad) <= 0:
                mensaje_error = "La cantidad debe ser un número positivo."
            elif ingrediente_receta_existente:
                if modo == "agregar" or (modo == "editar" and ingrediente_receta_existente.id != id_db):
                    mensaje_error = f"El ingrediente {ingrediente_busc.nombre} ya está asociado a la receta {receta_busc.nombre}"
        except ValueError:
            mensaje_error = "La cantidad debe ser un número"
            return mensaje_error
        return mensaje_error

    def dar_preparacion(self, id_receta, cantidad_personas):
        receta = self.dar_receta(id_receta)
        id_orig = receta['id']
        if receta:

            # Tiempo de preparación total de la receta:
            tiempo_receta = receta['tiempo'].split(":")

            horas, mins, segs = int(tiempo_receta[0]), int(tiempo_receta[1]), int(tiempo_receta[2])

            total_segundos = horas * 3600 + mins * 60 + segs

            if cantidad_personas < receta['personas']:
                tiempo_preparacion = total_segundos - (
                        (receta['personas'] - cantidad_personas) / (2 * receta['personas'])) * total_segundos
            else:
                tiempo_preparacion = (cantidad_personas // receta['personas']) * (2 * (total_segundos / 3))

            n_horas = int(tiempo_preparacion // 3600)
            segs_restantes = tiempo_preparacion % 3600
            n_mins = int(segs_restantes // 60)
            n_segs = int(segs_restantes % 60)

            tiempo_nuevo = '{:02d}:{:02d}:{:02d}'.format(n_horas, n_mins, n_segs)

            # Ingredientes de la preparación de la receta:
            ingredientes = session.query(Ingrediente).filter(
                Ingrediente.recetas.any(Receta.id.in_([id_orig]))).order_by(
                asc(Ingrediente.nombre),
                asc(Ingrediente.unidad),
                asc(Ingrediente.sitioCompra)).all()
            ingredientes_preparacion = []
            costo_total = 0
            # Se recorren los ingredientes ordenados:
            for ingrediente in ingredientes:
                # Cantidad de la asociación de receta - ingrediente:
                asociacion = session.query(IngredienteReceta).filter(IngredienteReceta.receta_id == id_orig,
                                                                     IngredienteReceta.ingrediente_id == ingrediente.id).first()
                cantidad_prep_ing = math.ceil((asociacion.cantidad * cantidad_personas) / receta['personas'])
                precio_prep_ing = cantidad_prep_ing * ingrediente.valor
                ing_act = {"nombre": ingrediente.nombre,
                           "unidad": ingrediente.unidad,
                           "cantidad": cantidad_prep_ing,
                           "valor": precio_prep_ing}
                ingredientes_preparacion.append(ing_act)

                costo_total += precio_prep_ing

            # Diccionario con el resultado:
            preparacion = {"receta": receta['nombre'],
                           "personas": cantidad_personas, "calorias": receta['calorias'],
                           "tiempo_preparacion": tiempo_nuevo,
                           "costo": costo_total,
                           "datos_ingredientes": ingredientes_preparacion}

            return preparacion
