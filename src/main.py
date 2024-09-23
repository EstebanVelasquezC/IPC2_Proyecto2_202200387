# main.py

from maquina import Maquina, LineaProduccion

# Crear una máquina de ensamblaje
maquina = Maquina("Máquina A")

# Crear líneas de producción
linea1 = LineaProduccion("Línea 1")
linea2 = LineaProduccion("Línea 2")

# Agregar líneas a la máquina
maquina.agregar_linea(linea1)
maquina.agregar_linea(linea2)

# Agregar componentes a las líneas de producción
maquina.agregar_componente("Línea 1", "Componente A1")
maquina.agregar_componente("Línea 1", "Componente A2")
maquina.agregar_componente("Línea 2", "Componente B1")

# Mostrar las líneas y sus componentes
maquina.mostrar_lineas()
