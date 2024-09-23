# maquina.py

from tda import ListaEnlazada
from producto import Componente

class Maquina:
    """Clase que representa una máquina de ensamblaje."""
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.lineas = ListaEnlazada()  # Usamos una lista enlazada para las líneas de producción.

    def agregar_linea(self, linea):
        """Agrega una nueva línea de producción."""
        self.lineas.agregar(linea)
    
    def agregar_componente(self, nombre_linea, nombre_componente, tiempo_ensamblaje, condiciones_especiales=None):
        """Agrega un componente a una línea de producción específica."""
        componente = Componente(nombre_componente, tiempo_ensamblaje, condiciones_especiales)
        actual = self.lineas.cabeza
        while actual is not None:
            if actual.dato.nombre == nombre_linea:
                actual.dato.componentes.agregar(componente)
                return
            actual = actual.siguiente
        print(f"Línea '{nombre_linea}' no encontrada en la máquina '{self.nombre}'")

    def mostrar_lineas(self):
        """Muestra las líneas de producción y sus componentes."""
        print(f"Líneas de producción en la máquina '{self.nombre}':")
        actual = self.lineas.cabeza
        while actual is not None:
            print(f"- Línea: {actual.dato.nombre}")
            actual.dato.mostrar_componentes()
            actual = actual.siguiente

class LineaProduccion:
    """Clase que representa una línea de producción dentro de una máquina."""
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.componentes = ListaEnlazada()  # Usamos una lista enlazada para los componentes.

    def mostrar_componentes(self):
        """Muestra los componentes de la línea."""
        print(f"  Componentes de la línea '{self.nombre}':")
        self.componentes.mostrar()

