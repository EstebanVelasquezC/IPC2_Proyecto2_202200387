
from maquina import Maquina, LineaProduccion
from simulador import Simulador
from producto import Producto
from producto import Componente

# Crear una máquina de ensamblaje
maquina = Maquina("Máquina A")

# Crear líneas de producción
linea1 = LineaProduccion("Línea 1")
linea2 = LineaProduccion("Línea 2")

# Agregar líneas a la máquina
maquina.agregar_linea(linea1)
maquina.agregar_linea(linea2)

# Agregar componentes a las líneas de producción con tiempos de ensamblaje y condiciones especiales
maquina.agregar_componente("Línea 1", "Componente A1", 2)
maquina.agregar_componente("Línea 1", "Componente A2", 3)
maquina.agregar_componente("Línea 2", "Componente B1", 1)

# Mostrar las líneas y sus componentes
maquina.mostrar_lineas()

# Crear el simulador
simulador = Simulador(maquina)

# Crear y agregar productos al simulador
producto1 = Producto("Producto 1")
producto1.agregar_componente(Componente("Componente A1", 2))
producto1.agregar_componente(Componente("Componente B1", 1))

producto2 = Producto("Producto 2")
producto2.agregar_componente(Componente("Componente A2", 3))

# Agregar los productos al simulador
simulador.agregar_producto(producto1)
simulador.agregar_producto(producto2)

# Mostrar componentes de los productos
producto1.mostrar_componentes()
producto2.mostrar_componentes()

# Ensamblar todos los productos
simulador.ensamblar_todos_productos()
