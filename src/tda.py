# tda.py

class Nodo:
    """Clase Nodo para representar un elemento en la lista enlazada."""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    """Implementación básica de una lista enlazada."""
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        """Verifica si la lista está vacía."""
        return self.cabeza is None

    def agregar(self, dato):
        """Agrega un nuevo nodo con el dato al final de la lista."""
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def mostrar(self):
        """Muestra los elementos de la lista."""
        actual = self.cabeza
        while actual is not None:
            print(actual.dato, end=' -> ')
            actual = actual.siguiente
        print('None')
