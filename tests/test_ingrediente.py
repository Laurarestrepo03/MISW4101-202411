import unittest

from faker import Faker
from sqlalchemy import func
import random

from src.modelo.ingrediente import Ingrediente
from src.modelo.declarative_base import Session, Base
from src.logica.LogicaRecetario import LogicaRecetario
from src.modelo.receta import Receta


class IngredienteTestCase(unittest.TestCase):

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

    def test_dar_ingredientes(self):
        consulta1 = self.LogicaRecetario.dar_ingredientes()
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        consulta2 = self.LogicaRecetario.dar_ingredientes()
        self.assertGreater(len(consulta2), len(consulta1))

    def test_comprobar_orden_dar_ingredientes(self):
        # Crear una lista de ingredientes aleatorios
        num_ingredientes = 5
        temp_nombre = ''
        for i in range(num_ingredientes):
            # Algunos tienen el mismo nombre (1 y 2):
            if i == 2:
                nombre_ingrediente = temp_nombre
            # Algunos tienen el mismo nombre y unidad (3 y 4):
            else:
                nombre_ingrediente = self.data_factory.unique.word()
            unidad = self.data_factory.unique.word()
            valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
            sitioCompra = self.data_factory.city()
            self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

            temp_nombre = nombre_ingrediente

        # Obtener la lista de ingredientes
        lista_ingredientes = self.LogicaRecetario.dar_ingredientes()

        # Verificar que la lista de ingredientes esté ordenada por nombre, unidad y sitio de compra de forma descendente
        for i in range(len(lista_ingredientes) - 1):
            ingrediente_actual = lista_ingredientes[i]
            siguiente_ingrediente = lista_ingredientes[i + 1]

            # Si el nombre es igual debe estar ordenado por unidad:
            if ingrediente_actual["nombre"] == siguiente_ingrediente["nombre"]:
                # Si el nombre y unidad es igual debe estar ordenado por sitio de compra:
                if ingrediente_actual["unidad"] == siguiente_ingrediente["unidad"]:
                    self.assertLessEqual(ingrediente_actual["sitioCompra"], siguiente_ingrediente["sitioCompra"])
                else:
                    self.assertLessEqual(ingrediente_actual["unidad"], siguiente_ingrediente["unidad"])
            else:
                self.assertLessEqual(ingrediente_actual["nombre"], siguiente_ingrediente["nombre"])

    def test_crear_ingrediente_mismo_nombre_y_unidad(self):
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        ingrediente = self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        self.assertEqual(ingrediente, False)

    def test_crear_ingrediente_con_valores_vacios(self):
        nombre_ingrediente = ""
        unidad = ""
        valor = ""
        sitioCompra = ""
        ingrediente = self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        self.assertEqual(ingrediente, False)

    def test_crear_ingrediente_con_valor_incorrecto(self):
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.unique.word()
        sitioCompra = self.data_factory.city()
        ingrediente = self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        self.assertEqual(ingrediente, False)

    def test_editar_ingrediente(self):
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente,
                                                             Ingrediente.unidad == unidad).first()
        id = ingrediente.id
        nuevo_nombre = self.data_factory.unique.word()
        self.LogicaRecetario.editar_ingrediente(id, nuevo_nombre, unidad, valor, sitioCompra)
        consulta = self.LogicaRecetario.dar_ingrediente(id)
        self.assertNotEqual(consulta['nombre'], nombre_ingrediente)
        self.assertEqual(consulta['nombre'], nuevo_nombre)

    def test_editar_ingrediente_con_valores_vacios(self):
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente,
                                                             Ingrediente.unidad == unidad).first()
        id = ingrediente.id
        nuevo_nombre = ""
        self.LogicaRecetario.editar_ingrediente(id, nuevo_nombre, unidad, valor, sitioCompra)
        consulta = self.LogicaRecetario.dar_ingrediente(id)
        self.assertEqual(consulta['nombre'], nombre_ingrediente)
        self.assertNotEqual(consulta['nombre'], nuevo_nombre)

    def test_editar_ingrediente_con_valor_incorrecto(self):
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente,
                                                             Ingrediente.unidad == unidad).first()
        id = ingrediente.id
        nuevo_valor = ""
        self.LogicaRecetario.editar_ingrediente(id, nombre_ingrediente, unidad, nuevo_valor, sitioCompra)
        consulta = self.LogicaRecetario.dar_ingrediente(id)
        self.assertEqual(consulta['valor'], valor)
        self.assertNotEqual(consulta['valor'], nuevo_valor)

    def test_eliminar_ingrediente(self):
        # 1. Configurar el estado inicial
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        # ID simulando la lista ordenada de la interfaz:
        ingredientes = self.LogicaRecetario.dar_ingredientes()
        id_ingrediente = next((i for i in range(len(ingredientes)) if ingredientes[i]["nombre"] == nombre_ingrediente), None)

        # ID real:
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente,
                                                             Ingrediente.unidad == unidad,
                                                             Ingrediente.valor == valor,
                                                             Ingrediente.sitioCompra == sitioCompra).first()
        id_ingrediente = ingrediente.id

        # 2. Ejecutar la acción donde se va a eliminar el ingrediente:
        resultado = self.LogicaRecetario.eliminar_ingrediente(id_ingrediente)
        self.assertEqual(resultado, True)

        # 3. Verificar el resultado
        ingrediente_eliminado = self.session.query(Ingrediente).filter_by(id=id_ingrediente).first()
        self.assertIsNone(ingrediente_eliminado, "El ingrediente no ha sido eliminado correctamente")

    def test_eliminar_ingrediente_inexistente(self):
        # 1. Configurar el estado inicial
        nombre_ingrediente = self.data_factory.unique.word()
        unidad = self.data_factory.unique.word()
        valor = self.data_factory.pyfloat(min_value=1, max_value=1000)
        sitioCompra = self.data_factory.city()
        self.LogicaRecetario.crear_ingrediente(nombre_ingrediente, unidad, valor, sitioCompra)

        # ID inexistente en el recetario. Se trae el número de ingredientes existentes en la base de datos
        # y se le suma uno para asegurarse que siempre sea un ID inexistente.
        conteo_ingredientes = self.session.query(func.count()).select_from(Ingrediente).scalar()
        id_ingrediente_inexistente = conteo_ingredientes + 1

        # 2. Ejecutar la acción donde se va a eliminar el ingrediente:
        resultado = self.LogicaRecetario.eliminar_ingrediente(id_ingrediente_inexistente)
        self.assertEqual(resultado, False)

        # ID real:
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente,
                                                             Ingrediente.unidad == unidad,
                                                             Ingrediente.valor == valor,
                                                             Ingrediente.sitioCompra == sitioCompra).first()
        id_ingrediente = ingrediente.id

        # 3. Verificar el resultado
        ingrediente_eliminado = self.session.query(Ingrediente).filter_by(id=id_ingrediente).first()
        self.assertIsNotNone(ingrediente_eliminado, "El ingrediente se elimino pero no deberia ser eliminado")

    def test_eliminar_ingrediente_asociado_a_receta(self):
        # Info de la receta:
        nombre_receta = self.data_factory.unique.word()
        tiempo_receta = "0" + str(self.data_factory.random_number(digits=1)) + ":0" + str(
            self.data_factory.random_number(digits=1)) + ":0" + str(self.data_factory.random_number(digits=1))
        personas_receta = random.randint(1, 20)
        calorias_receta = round(random.uniform(0, 100), 2)
        preparacion_receta = self.data_factory.sentence()
        self.LogicaRecetario.crear_receta(nombre_receta, tiempo_receta, personas_receta, calorias_receta,
                                          preparacion_receta)

        receta = self.session.query(Receta).filter(Receta.nombre == nombre_receta).first()

        # Info del ingrediente:
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

        # ID del ingrediente simulando la lista ordenada de la interfaz:
        ingredientes = self.LogicaRecetario.dar_ingredientes()
        id_ingrediente = next((i for i in range(len(ingredientes)) if ingredientes[i]["nombre"] == nombre_ingrediente),
                              None)

        # 2. Ejecutar la acción donde se va a eliminar el ingrediente:
        resultado = self.LogicaRecetario.eliminar_ingrediente(id_ingrediente)
        self.assertEqual(resultado, False)

        # ID real:
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente,
                                                             Ingrediente.unidad == unidad,
                                                             Ingrediente.valor == valor,
                                                             Ingrediente.sitioCompra == sitioCompra).first()
        id_ingrediente = ingrediente.id

        # 3. Verificar el resultado
        ingrediente_eliminado = self.session.query(Ingrediente).filter_by(id=id_ingrediente).first()
        self.assertIsNotNone(ingrediente_eliminado, "El ingrediente se elimino pero no debería ser eliminado")


