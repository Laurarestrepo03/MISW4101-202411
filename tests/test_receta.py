import unittest
import math
import os
from faker import Faker
import random
from src.modelo.receta import Receta
from src.modelo.ingrediente import Ingrediente
from src.modelo.declarative_base import Session, Base
from src.logica.LogicaRecetario import LogicaRecetario


class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.LogicaRecetario = LogicaRecetario()
        self.data_factory = Faker()

        # Recetas para prueba:
        receta = 0

    def tearDown(self):
        self.logica = None
        # Borrar todos los datos de cada tabla
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())

        # Aplicar los cambios
        self.session.commit()

        self.session.close()

    def test_dar_recetas(self):
        consulta1 = self.LogicaRecetario.dar_recetas()
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = self.data_factory.random_digit_not_null()
        calorias_receta = round(random.uniform(1, 1000), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)
        consulta2 = self.LogicaRecetario.dar_recetas()
        self.assertGreater(len(consulta2), len(consulta1))

    def test_crear_receta(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # Verificar que la lista esté ordenada alfabéticamente por nombre
        for i in range(len(recetas) - 1):
            self.assertLessEqual(recetas[i]["nombre"], recetas[i + 1]["nombre"])

    def test_crear_receta_nombre_incorrecto(self):
        # Primero se prueba con un nombre vacio:
        nombre = ""
        self.__test_nombres_incorrectos(nombre)

        # Ahora se prueba con un nombre que no es alfanumerico:
        nombre = self.data_factory.random_number(digits=1)
        self.__test_nombres_incorrectos(nombre)

    def __test_nombres_incorrectos(self, receta):
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos incorrectos
        receta_uno = self.LogicaRecetario.crear_receta(
            receta,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # No se debe crear la receta:
        self.assertFalse(receta_uno)

        # Debe generarse un mensaje de error:
        self.assertNotEqual(
            self.LogicaRecetario.validar_crear_editar_receta(-1, receta, tiempo, personas, calorias, preparacion, self.LogicaRecetario.EVENTO_AGREGAR_RECETA),
            "")

        # Verificar que la receta NO esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertNotIn(receta, nombres_recetas)

    def test_crear_receta_tiempo_incorrecto(self):
        # Primero se prueba con un tiempo vacio:
        tiempo = ""
        self.__test_tiempo_incorrectos(tiempo)

        # Ahora se prueba con un tiempo que no es string:
        tiempo = self.data_factory.random_number(digits=1)
        self.__test_tiempo_incorrectos(tiempo)

        # Ahora se prueba con un tiempo que es un string inválido
        tiempo = self.data_factory.sentence()
        self.__test_tiempo_incorrectos(tiempo)

    def __test_tiempo_incorrectos(self, tiempo):
        nombre = self.data_factory.unique.word()
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos incorrectos
        receta_uno = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # No se debe crear la receta:
        self.assertFalse(receta_uno)

        # Debe generarse un mensaje de error:
        self.assertNotEqual(
            self.LogicaRecetario.validar_crear_editar_receta(-1, nombre, tiempo, personas, calorias, preparacion, self.LogicaRecetario.EVENTO_AGREGAR_RECETA), "")

        # Verificar que la receta NO esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertNotIn(nombre, nombres_recetas)

    def test_crear_receta_personas_incorrecto(self):
        # Primero se prueba con número de personas vacio:
        personas = ""
        self.__test_personas_incorrectos(personas)

        # Ahora se prueba con un número de personas que es un string, en lugar de un número:
        personas = self.data_factory.sentence()
        self.__test_personas_incorrectos(personas)

    def __test_personas_incorrectos(self, personas):
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos incorrectos
        receta_uno = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # No se debe crear la receta:
        self.assertFalse(receta_uno)

        # Debe generarse un mensaje de error:
        self.assertNotEqual(
            self.LogicaRecetario.validar_crear_editar_receta(-1, nombre, tiempo, personas, calorias, preparacion, self.LogicaRecetario.EVENTO_AGREGAR_RECETA), "")

        # Verificar que la receta NO esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertNotIn(nombre, nombres_recetas)

    def test_crear_receta_calorias_incorrecto(self):
        # Primero se prueba con número de calorias vacio:
        calorias = ""
        self.__test_calorias_incorrectas(calorias)

        # Ahora se prueba con un número de calorias que es un string, en lugar de un número:
        calorias = self.data_factory.sentence()
        self.__test_calorias_incorrectas(calorias)

    def __test_calorias_incorrectas(self, calorias):
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos incorrectos
        receta_uno = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # No se debe crear la receta:
        self.assertFalse(receta_uno)

        # Debe generarse un mensaje de error:
        self.assertNotEqual(
            self.LogicaRecetario.validar_crear_editar_receta(-1, nombre, tiempo, personas, calorias, preparacion, self.LogicaRecetario.EVENTO_AGREGAR_RECETA), "")

        # Verificar que la receta NO esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertNotIn(nombre, nombres_recetas)

    def test_crear_receta_preparacion_incorrecto(self):
        # Primero se prueba con un nombre vacio:
        preparacion = ""
        self.__test_preparacion_incorrectos(preparacion)

        # Ahora se prueba con una preparación que no es alfanumerico:
        preparacion = self.data_factory.random_number(digits=1)
        self.__test_preparacion_incorrectos(preparacion)

    def __test_preparacion_incorrectos(self, preparacion):
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)

        # Intentar crear la receta con los datos incorrectos
        receta_uno = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # No se debe crear la receta:
        self.assertFalse(receta_uno)

        # Debe generarse un mensaje de error:
        self.assertNotEqual(
            self.LogicaRecetario.validar_crear_editar_receta(-1, nombre, tiempo, personas, calorias, preparacion, self.LogicaRecetario.EVENTO_AGREGAR_RECETA),
            "")

        # Verificar que la receta NO esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertNotIn(nombre, nombres_recetas)

    def test_crear_receta_nombre_existente(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()  # Genera un nombre de receta único
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos incorrectos
        receta_uno = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar que la receta se creó correctamente
        self.assertTrue(receta_uno)

        # Intentar crear otra receta con el mismo nombre
        resultado_creacion_repetida = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar que la creación de la receta repetida ha fallado
        self.assertFalse(resultado_creacion_repetida)

        # Verificar que el nombre de la receta esté presente exactamente una vez en la lista de recetas.
        # Es decir que no se agrega la receta repetida
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]

        cuenta_receta = nombres_recetas.count(nombre)
        self.assertEqual(cuenta_receta, 1)


    def test_editar_receta(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta:
        nombre_nuevo_receta = self.data_factory.unique.word()
        self.LogicaRecetario.editar_receta(id_receta, nombre_nuevo_receta, tiempo, personas, calorias, preparacion)

        # Como el nombre es nuevo y unico se espera que el nombre de la receta sea el nuevo nombre:
        self.assertEqual(self.LogicaRecetario.dar_receta(id_receta)['nombre'], nombre_nuevo_receta)

    def test_editar_receta_nombre_repetido(self):
        # Generar datos aleatorios para la receta 1:
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Generar datos aleatorios para otra receta 2:
        nombre_2 = self.data_factory.unique.word()
        tiempo_2 = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_2 = self.data_factory.random_digit_not_null()
        calorias_2 = round(random.uniform(1, 1000), 2)
        preparacion_2 = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion_2 = self.LogicaRecetario.crear_receta(
            nombre_2,
            tiempo_2,
            personas_2,
            calorias_2,
            preparacion_2
        )

        # Verificar si las recetas se crearon correctamente
        self.assertTrue(resultado_creacion)
        self.assertTrue(resultado_creacion_2)

        # Verificar que las recetas esten en la lista de recetas después de ser creadas
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)
        self.assertIn(nombre_2, nombres_recetas)

        # ID de la receta 1 creada en el orden de recetas ordenado (para simular a la interfaz)
        id_receta_1 = next((i for i in range(len(recetas)) if recetas[i]["nombre"] == nombre), None)

        # Ahora se edita la receta 1 con un nombre ya existente de la receta 2:
        resultado = self.LogicaRecetario.editar_receta(id_receta_1, nombre_2, tiempo, personas, calorias, preparacion)

        # No se debe poder editar:
        self.assertEqual(resultado, False)

        # Verificar que el nombre de la receta esté presente exactamente una vez en la lista de recetas.
        # Es decir que no se agrega la receta que se edito con nombre repetido:
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]

        # Solo debe existir una sola receta con el nombre de la Receta 2. No debe estar duplicado:
        cuenta_receta = nombres_recetas.count(nombre_2)
        self.assertEqual(cuenta_receta, 1)


    def test_editar_receta_con_valores_vacios(self):

        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta con valores vacíos:
        nombre_nuevo_receta = ""  # Nombre vacío
        tiempo_nuevo = ""  # Tiempo vacío
        personas_nuevo = None  # Personas vacío
        calorias_nuevo = None  # Calorías vacío
        preparacion_nuevo = ""  # Preparación vacía

        # Intentar editar la receta con valores vacíos
        resultado_edicion = self.LogicaRecetario.editar_receta(id_receta, nombre_nuevo_receta, tiempo_nuevo,
                                                               personas_nuevo, calorias_nuevo, preparacion_nuevo)

        # Verificar que la receta no se haya editado si los valores de edición son vacíos
        self.assertFalse(resultado_edicion)

        # Verificar que los valores de la receta original no hayan cambiado en la base de datos
        receta_editada = self.session.query(Receta).filter_by(id=id_receta).first()
        self.assertEqual(receta_editada.nombre, nombre)
        self.assertEqual(receta_editada.tiempo, tiempo)
        self.assertEqual(receta_editada.personas, personas)
        self.assertEqual(receta_editada.calorias, calorias)
        self.assertEqual(receta_editada.preparacion, preparacion)

    def test_editar_receta_personas_incorrectas(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta con un número de personas incorrecto:
        nuevas_personas = self.data_factory.unique.word()
        resultado = self.LogicaRecetario.editar_receta(id_receta, nombre, tiempo, nuevas_personas, calorias, preparacion)

        # No se debe poder editar:
        self.assertEqual(resultado, False)

        # Verificar que los valores de la receta original no hayan cambiado en la base de datos
        receta_editada = self.session.query(Receta).filter_by(id=id_receta).first()
        self.assertEqual(receta_editada.nombre, nombre)
        self.assertEqual(receta_editada.tiempo, tiempo)
        self.assertEqual(receta_editada.personas, personas)
        self.assertEqual(receta_editada.calorias, calorias)
        self.assertEqual(receta_editada.preparacion, preparacion)

    def test_editar_receta_nombre_incorrecto(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word() # Nombre como número
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta con un nombre que es un número:
        nombre_numero = self.data_factory.random_number(digits=4)
        resultado = self.LogicaRecetario.editar_receta(id_receta, nombre_numero, tiempo, personas, calorias,
                                                       preparacion)

        # No se debe poder editar:
        self.assertEqual(resultado, False)

        # Verificar que los valores de la receta original no hayan cambiado en la base de datos
        receta_editada = self.session.query(Receta).filter_by(id=id_receta).first()
        self.assertEqual(receta_editada.nombre, nombre)
        self.assertEqual(receta_editada.tiempo, tiempo)
        self.assertEqual(receta_editada.personas, personas)
        self.assertEqual(receta_editada.calorias, calorias)
        self.assertEqual(receta_editada.preparacion, preparacion)

    def test_editar_receta_calorias_negativas(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta con calorías negativas:
        nuevas_calorias = round(random.uniform(-1000, -1), 2)
        resultado = self.LogicaRecetario.editar_receta(id_receta, nombre, tiempo, personas, nuevas_calorias, preparacion)

        # No se debe poder editar:
        self.assertEqual(resultado, False)

        # Verificar que los valores de la receta original no hayan cambiado en la base de datos
        receta_editada = self.session.query(Receta).filter_by(id=id_receta).first()
        self.assertEqual(receta_editada.nombre, nombre)
        self.assertEqual(receta_editada.tiempo, tiempo)
        self.assertEqual(receta_editada.personas, personas)
        self.assertEqual(receta_editada.calorias, calorias)
        self.assertEqual(receta_editada.preparacion, preparacion)

    def test_editar_receta_tiempo_palabras(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta con tiempo compuesto por palabras:
        tiempo_palabras = self.data_factory.text()
        resultado = self.LogicaRecetario.editar_receta(id_receta, nombre, tiempo_palabras, personas, calorias,
                                                       preparacion)

        # No se debe poder editar:
        self.assertEqual(resultado, False)

        # Verificar que los valores de la receta original no hayan cambiado en la base de datos
        receta_editada = self.session.query(Receta).filter_by(id=id_receta).first()
        self.assertEqual(receta_editada.nombre, nombre)
        self.assertEqual(receta_editada.tiempo, tiempo)
        self.assertEqual(receta_editada.personas, personas)
        self.assertEqual(receta_editada.calorias, calorias)
        self.assertEqual(receta_editada.preparacion, preparacion)

    def test_editar_receta_preparacion_numero(self):
        # Generar datos aleatorios para la receta
        nombre = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()

        # Intentar crear la receta con los datos aleatorios
        resultado_creacion = self.LogicaRecetario.crear_receta(
            nombre,
            tiempo,
            personas,
            calorias,
            preparacion
        )

        # Verificar si la receta se creó correctamente
        self.assertTrue(resultado_creacion)

        # Verificar que la receta esté en la lista de recetas después de ser creada
        recetas = self.LogicaRecetario.dar_recetas()
        nombres_recetas = [receta["nombre"] for receta in recetas]
        self.assertIn(nombre, nombres_recetas)

        # ID de la receta creada:
        receta_bd = self.session.query(Receta).filter_by(nombre=nombre).first()
        id_receta = receta_bd.id

        # Ahora se edita la receta con preparación que es un número:
        preparacion_numero_nueva = str(self.data_factory.random_number(digits=4))
        resultado = self.LogicaRecetario.editar_receta(id_receta, nombre, tiempo, personas, calorias,
                                                       preparacion_numero_nueva)

        # No se debe poder editar:
        self.assertEqual(resultado, False)

        # Verificar que los valores de la receta original no hayan cambiado en la base de datos
        receta_editada = self.session.query(Receta).filter_by(id=id_receta).first()
        self.assertEqual(receta_editada.nombre, nombre)
        self.assertEqual(receta_editada.tiempo, tiempo)
        self.assertEqual(receta_editada.personas, personas)
        self.assertEqual(receta_editada.calorias, calorias)
        self.assertEqual(receta_editada.preparacion, preparacion) 

    def test_preparar_receta(self):
        nombre_receta = self.data_factory.unique.word()
        tiempo = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas = self.data_factory.random_digit_not_null()
        calorias = round(random.uniform(1, 1000), 2)
        preparacion = self.data_factory.text()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo, personas, calorias, preparacion)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente1 = self.data_factory.unique.word()
        unidad1 = self.data_factory.unique.word()
        valor1 = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra1 = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente1, unidad1, valor1, sitioCompra1)

        ingrediente1 = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente1).first()

        cantidad1 = random.randint(1, 100)

        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente1.__dict__, cantidad1)

        nombre_ingrediente2 = self.data_factory.unique.word()
        unidad2 = self.data_factory.unique.word()
        valor2 = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra2 = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente2, unidad2, valor2, sitioCompra2)

        ingrediente2 = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente2).first()

        cantidad2 = random.randint(1, 100)

        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente2.__dict__, cantidad2)

        personas = random.randint(1, 100)

        # Tiempo total de preparación de la receta:
        tiempo_receta = receta.tiempo.split(":")
        horas, mins, segs = int(tiempo_receta[0]), int(tiempo_receta[1]), int(tiempo_receta[2])
        total_segundos = horas*3600 + mins*60 + segs

        if personas < receta.personas:
            tiempo_preparacion = total_segundos - ((receta.personas - personas)/(2*receta.personas)) * total_segundos
        else:
            tiempo_preparacion = (personas//receta.personas)*(2*(total_segundos/3))
        
        n_horas = int(tiempo_preparacion // 3600)
        segs_restantes = tiempo_preparacion % 3600
        n_mins = int(segs_restantes // 60)
        n_segs =  int(segs_restantes % 60)

        tiempo_nuevo = '{:02d}:{:02d}:{:02d}'.format(n_horas, n_mins, n_segs)

        preparacion_test = {
            "receta" : nombre_receta,
            "personas": personas,
            "calorias": receta.calorias,
            "tiempo_preparacion": tiempo_nuevo}

        cantidad_prep_ing_1 = math.ceil((cantidad1 * personas) / receta.personas)
        precio_prep_ing_1 = cantidad_prep_ing_1 * ingrediente1.valor

        ing_prep1 = {"nombre": ingrediente1.nombre, 
                     "unidad": ingrediente1.unidad, 
                     "cantidad": cantidad_prep_ing_1,
                     "valor": precio_prep_ing_1}

        cantidad_prep_ing_2 = math.ceil((cantidad2 * personas) / receta.personas)
        precio_prep_ing_2 = cantidad_prep_ing_2 * ingrediente2.valor
        
        ing_prep2 = { "nombre": ingrediente2.nombre,
                     "unidad": ingrediente2.unidad, 
                     "cantidad": cantidad_prep_ing_2,
                     "valor": precio_prep_ing_2}


        ing = self.LogicaRecetario.dar_ingredientes()

        id_ing_1 = next((i for i in range(len(ing)) if ing[i]["nombre"] == nombre_ingrediente1 and ing[i]["unidad"] == unidad1),
             None)

        id_ing_2 = next((i for i in range(len(ing)) if ing[i]["nombre"] == nombre_ingrediente2 and ing[i]["unidad"] == unidad2),
                        None)

        if id_ing_1 < id_ing_2:
            ings_preparacion = [ing_prep1, ing_prep2]
        else:
            ings_preparacion = [ing_prep2, ing_prep1]


        preparacion_test["costo"] = precio_prep_ing_1 + precio_prep_ing_2

        preparacion_test["datos_ingredientes"] = ings_preparacion

        preparacion_logica = self.LogicaRecetario.dar_preparacion(receta.id, personas)

        self.assertEqual(preparacion_test, preparacion_logica)








