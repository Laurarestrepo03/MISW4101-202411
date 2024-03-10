import sys
from src.vista.InterfazRecetario import App_Recetario
from src.logica.LogicaRecetario import LogicaRecetario

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = LogicaRecetario()

    app = App_Recetario(sys.argv, logica)
    sys.exit(app.exec_())