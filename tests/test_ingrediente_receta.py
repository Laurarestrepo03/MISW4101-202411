import unittest

from faker import Faker
import random

from src.modelo.ingrediente import Ingrediente
from src.modelo.ingrediente import IngredienteReceta
from src.modelo.receta import Receta
from src.modelo.declarative_base import Session, Base
from src.logica.LogicaRecetario import LogicaRecetario


class IngredienteRecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.LogicaRecetario = LogicaRecetario()
        self.data_factory = Faker()

    def tearDown(self):
        self.logica = None
        # Borrar todos los datos de cada tabla
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())

        # Aplicar los cambios
        self.session.commit()

        self.session.close()

    def test_dar_ingredientes_receta(self):

        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        consulta1 = self.LogicaRecetario.dar_ingredientes_receta(receta.id)

        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()

        cantidad = random.randint(1, 100)
        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)

        consulta2 = self.LogicaRecetario.dar_ingredientes_receta(receta.id)
        self.assertGreater(len(consulta2), len(consulta1))

    def test_comprobar_orden_dar_ingredientes_receta(self):
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 1000), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        num_ingredientes = 5
        temp_nombre = ''
        for i in range(num_ingredientes):
            if i == 2:
                nombre_ingrediente = temp_nombre
            else:
                nombre_ingrediente = self.data_factory.unique.word()
            unidad = self.data_factory.unique.word()
            valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
            sitioCompra = self.data_factory.city()
            self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

            ingrediente = self.session.query(Ingrediente).order_by(Ingrediente.id.desc()).first()
            cantidad = random.randint(1, 100)

            self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)

            temp_nombre = nombre_ingrediente

        lista_ingredientes = self.LogicaRecetario.dar_ingredientes_receta(receta.id)

        for i in range(len(lista_ingredientes) - 1):
            ingrediente_actual = lista_ingredientes[i]
            siguiente_ingrediente = lista_ingredientes[i + 1]

            if ingrediente_actual["ingrediente"] == siguiente_ingrediente["ingrediente"]:
                self.assertLessEqual(ingrediente_actual["unidad"], siguiente_ingrediente["unidad"])
            else:
                self.assertLessEqual(ingrediente_actual["ingrediente"], siguiente_ingrediente["ingrediente"])

    def test_agregar_ingrediente_receta(self):
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()

        cantidad = random.randint(1, 100)

        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)

        nombres_ingredientes_receta = [ingrediente_receta["ingrediente"] for ingrediente_receta in
                                       self.LogicaRecetario.dar_ingredientes_receta(receta.id)]

        self.assertIn(nombre_ingrediente, nombres_ingredientes_receta)

    def test_agregar_ingrediente_receta_con_cantidad_incorrecta(self):

        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()

        cantidad = ""

        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)

        nombres_ingredientes_receta = [ingrediente_receta["ingrediente"] for ingrediente_receta in
                                       self.LogicaRecetario.dar_ingredientes_receta(receta.id)]

        self.assertNotIn(nombre_ingrediente, nombres_ingredientes_receta)

    def test_agregar_ingrediente_receta_repetido(self):
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()

        cantidad = random.randint(1, 100)

        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)  # Primera vez
        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)  # Segunda vez

        nombres_ingredientes_receta = [ingrediente_receta["ingrediente"] for ingrediente_receta in
                                       self.LogicaRecetario.dar_ingredientes_receta(receta.id)]

        self.assertEqual(len(nombres_ingredientes_receta), 1)

    def test_editar_ingrediente_receta(self):

        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()

        cantidad = random.randint(1, 100)
        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)

        nueva_cantidad = random.randint(1, 100)

        ingrediente_receta = self.session.query(IngredienteReceta).filter(IngredienteReceta.receta_id == receta.id,
                                                                          IngredienteReceta.ingrediente_id == ingrediente.id).first()

        self.LogicaRecetario.editar_ingrediente_receta(ingrediente_receta.id, receta.__dict__, ingrediente.__dict__, nueva_cantidad)

        consulta = self.LogicaRecetario.dar_ingrediente_receta(ingrediente_receta.id)
        self.assertNotEqual(consulta['cantidad'], cantidad)
        self.assertEqual(consulta['cantidad'], nueva_cantidad)
    
    def test_editar_ingrediente_receta_con_cantidad_incorrecta(self):
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()

        cantidad = random.randint(1, 100)
        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente.__dict__, cantidad)

        nueva_cantidad = ""

        ingrediente_receta = self.session.query(IngredienteReceta).filter(IngredienteReceta.receta_id == receta.id,
                                                                          IngredienteReceta.ingrediente_id == ingrediente.id).first()

        self.LogicaRecetario.editar_ingrediente_receta(ingrediente_receta.id, receta.__dict__, ingrediente.__dict__, nueva_cantidad)

        consulta = self.LogicaRecetario.dar_ingrediente_receta(ingrediente_receta.id)
        self.assertEqual(consulta['cantidad'], cantidad)
        self.assertNotEqual(consulta['cantidad'], nueva_cantidad)

    def test_editar_ingrediente_receta_con_nuevo_ingrediente(self):
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        nombre_ingrediente1 = self.data_factory.unique.word()
        unidad1 = self.data_factory.unique.word()
        valor1 = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra1 = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente1, unidad1, valor1, sitioCompra1)

        ingrediente1 = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente1).first()

        cantidad = random.randint(1, 100)
        self.LogicaRecetario.agregar_ingrediente_receta(receta.__dict__, ingrediente1.__dict__, cantidad)

        ingrediente_receta = self.session.query(IngredienteReceta).filter(IngredienteReceta.receta_id == receta.id,
                                                                          IngredienteReceta.ingrediente_id == ingrediente1.id).first()
        
        consulta1 = self.LogicaRecetario.dar_ingrediente_receta(ingrediente_receta.id)
        self.assertEqual(consulta1['ingrediente_id'], ingrediente1.id)

        nombre_ingrediente2 = self.data_factory.unique.word()
        unidad2 = self.data_factory.unique.word()
        valor2 = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra2 = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente2, unidad2, valor2, sitioCompra2)

        ingrediente2 = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente2).first()

        self.LogicaRecetario.editar_ingrediente_receta(ingrediente_receta.id, receta.__dict__, ingrediente2.__dict__, cantidad)

        consulta2 = self.LogicaRecetario.dar_ingrediente_receta(ingrediente_receta.id)

        self.assertNotEqual(consulta2['ingrediente_id'], ingrediente1.id)
        self.assertEqual(consulta2['ingrediente_id'], ingrediente2.id)


