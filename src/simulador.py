# simulador.py

from maquina import Maquina, LineaProduccion
from producto import Producto
from tda import ListaEnlazada
import time

class Simulador:
    """Clase que simula el proceso de ensamblaje de productos en una máquina."""
    
    def __init__(self, maquina):
        self.maquina = maquina
        self.productos = ListaEnlazada()  # Lista enlazada para almacenar los productos.
        self.productos_ensamblados = 0

    def agregar_producto(self, producto):
        """Agrega un producto a la simulación."""
        self.productos.agregar(producto)

    def ensamblar_producto(self, producto):
        """Simula el ensamblaje de un producto en la máquina."""
        print(f"\nIniciando el ensamblaje del producto '{producto.nombre}' en la máquina '{self.maquina.nombre}'...")
        actual_linea = self.maquina.lineas.cabeza
        actual_componente = producto.componentes.cabeza
        while actual_linea is not None and actual_componente is not None:
            print(f"Ensamblando en {actual_linea.dato.nombre}:")
            self.ensamblar_linea(actual_linea.dato, actual_componente.dato)
            actual_linea = actual_linea.siguiente
            actual_componente = actual_componente.siguiente
        self.productos_ensamblados += 1
        self.mostrar_producto_ensamblado(producto)

    def ensamblar_linea(self, linea, componente):
        """Simula el ensamblaje de un componente en una línea específica."""
        componentes = linea.componentes.cabeza
        while componentes is not None:
            if componentes.dato.nombre == componente.nombre:
                if self.verificar_condiciones(componente):
                    print(f"- Componente: {componentes.dato} ensamblado correctamente.")
                    time.sleep(componentes.dato.tiempo_ensamblaje)  # Simular tiempo de ensamblaje
                else:
                    print(f"- Componente {componente.nombre} no puede ser ensamblado debido a condiciones especiales.")
                return
            componentes = componentes.siguiente
        print(f"- Componente {componente.nombre} no encontrado en la línea '{linea.nombre}'.")

    def verificar_condiciones(self, componente):
        """Verifica si se cumplen las condiciones especiales para ensamblar el componente."""
        # Aquí podrías implementar condiciones especiales, por simplicidad asumimos que siempre se cumplen
        return True

    def mostrar_producto_ensamblado(self, producto):
        """Muestra el total de productos ensamblados."""
        print(f"Producto '{producto.nombre}' ensamblado en la máquina '{self.maquina.nombre}'. Total de productos ensamblados: {self.productos_ensamblados}")

    def ensamblar_todos_productos(self):
        """Simula el ensamblaje de todos los productos en la lista."""
        actual = self.productos.cabeza
        while actual is not None:
            self.ensamblar_producto(actual.dato)
            actual = actual.siguiente
