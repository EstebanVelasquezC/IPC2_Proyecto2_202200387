# producto.py

from tda import ListaEnlazada

class Componente:
    """Clase que representa un componente que será ensamblado."""
    
    def __init__(self, nombre, tiempo_ensamblaje, condiciones_especiales=None):
        self.nombre = nombre
        self.tiempo_ensamblaje = tiempo_ensamblaje  # Tiempo en segundos
        self.condiciones_especiales = condiciones_especiales or []  # Lista de condiciones especiales

    def __str__(self):
        return f"{self.nombre} (Tiempo: {self.tiempo_ensamblaje}s)"

class Producto:
    """Clase que representa un producto que será ensamblado."""
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.componentes = ListaEnlazada()  # Lista enlazada de componentes para ensamblar el producto.

    def agregar_componente(self, componente):
        """Agrega un componente necesario para ensamblar el producto."""
        self.componentes.agregar(componente)

    def mostrar_componentes(self):
        """Muestra los componentes del producto."""
        print(f"Componentes del producto '{self.nombre}':")
        self.componentes.mostrar()
