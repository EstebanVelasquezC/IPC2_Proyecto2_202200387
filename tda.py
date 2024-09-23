class Nodo:
    def __init__(self, valor):
        self.valor = valor  # Almacena el valor del nodo
        self.siguiente = None  # Inicializa el puntero al siguiente nodo

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  # Inicializa la cabeza de la lista
        self.tamano = 0  # Contador de nodos en la lista

    def insertar(self, valor):
        nuevo_nodo = Nodo(valor)  # Crea un nuevo nodo
        if self.cabeza is None:  # Si la lista está vacía
            self.cabeza = nuevo_nodo  # El nuevo nodo se convierte en la cabeza
        else:
            actual = self.cabeza
            while actual.siguiente:  # Recorre hasta el final de la lista
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo  # Agrega el nuevo nodo al final
        self.tamano += 1  # Incrementa el tamaño de la lista

    def eliminar(self, valor):
        """Elimina el primer nodo que contiene el valor especificado."""
        actual = self.cabeza
        anterior = None
        while actual is not None:
            if actual.valor == valor:  # Si se encuentra el valor
                if anterior is None:  # Si es el primer nodo
                    self.cabeza = actual.siguiente  # Cambia la cabeza
                else:
                    anterior.siguiente = actual.siguiente  # Salta el nodo a eliminar
                self.tamano -= 1  # Decrementa el tamaño
                return True  # Retorna True si se eliminó
            anterior = actual
            actual = actual.siguiente
        print(f"Valor {valor} no encontrado en la lista.")  # Mensaje si no se encuentra
        return False  # Retorna False si no se encontró el valor

    def eliminar_posicion(self, posicion):
        """Elimina el nodo en la posición especificada (0-indexed)."""
        if posicion < 0 or posicion >= self.tamano:
            raise IndexError("Posición fuera de rango")
        
        actual = self.cabeza
        anterior = None
        for _ in range(posicion):
            anterior = actual
            actual = actual.siguiente

        if anterior is None:  # Si se elimina el primer nodo
            self.cabeza = actual.siguiente  # Cambia la cabeza
        else:
            anterior.siguiente = actual.siguiente  # Salta el nodo a eliminar

        self.tamano -= 1  # Decrementa el tamaño
        return True  # Retorna True si se eliminó

    def recorrer(self):
        """Generador que recorre la lista y devuelve los valores uno a uno."""
        actual = self.cabeza
        while actual:
            yield actual.valor  # Usa yield para retornar los valores
            actual = actual.siguiente

    def obtener_tamano(self):
        return self.tamano  # Retorna el tamaño actual de la lista

    def esta_vacia(self):
        return self.tamano == 0  # Verifica si la lista está vacía

    def __str__(self):
        if self.esta_vacia():
            return "Lista vacía"
        resultado = ""
        actual = self.cabeza
        while actual:
            resultado += str(actual.valor) + " -> "
            actual = actual.siguiente
        return resultado + "None"  # Indica el final de la lista

    def obtener_nodo(self, posicion):
        """Obtiene el nodo en una posición específica (0-indexed)"""
        if posicion < 0 or posicion >= self.tamano:
            raise IndexError("Posición fuera de rango")
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        return actual.valor  # Retorna el valor del nodo en la posición dada

    def limpiar(self):
        """Limpia la lista, eliminando todos los nodos."""
        self.cabeza = None
        self.tamano = 0
        print("Lista limpiada.")
