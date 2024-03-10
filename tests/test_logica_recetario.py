import unittest

from src.logica.LogicaRecetario import LogicaRecetario

class LogicaRecetarioTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaRecetario()
        
    def tearDown(self):
        self.logica = None
        
    # def test_dar_receta(self):
    #     receta = self.logica.recetas[0]
    #     self.assertEqual(receta["nombre"], "Ajiaco")


