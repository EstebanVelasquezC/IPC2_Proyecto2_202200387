from tda import ListaEnlazada  # Asegúrate de que tienes implementada esta clase en tda.py

class Componente:
    def __init__(self, id_componente, tiempo_ensamblaje):
        self.id_componente = id_componente
        self.tiempo_ensamblaje = tiempo_ensamblaje

    def __str__(self):
        return f"Componente(id: {self.id_componente}, tiempo: {self.tiempo_ensamblaje})"

class LineaEnsamblaje:
    def __init__(self, id_linea):
        self.id_linea = id_linea
        self.componentes = ListaEnlazada()  # Usar lista enlazada para almacenar componentes

    def agregar_componente(self, componente):
        self.componentes.insertar(componente)  # Insertar en la lista enlazada

    def obtener_componentes(self):
        return self.componentes  # Retorna la lista de componentes

class PasoSimulacion:
    def __init__(self, tiempo, linea, accion):
        self.tiempo = tiempo  # Tiempo del paso
        self.linea = linea  # Línea de ensamblaje
        self.accion = accion  # Acción realizada (Mover brazo, ensamblar, etc.)

    def __str__(self):
        return f"Segundo {self.tiempo}: Línea {self.linea} - {self.accion}"

class Producto:
    def __init__(self, nombre, secuencia):
        self.nombre = nombre
        self.secuencia = secuencia  # La secuencia será una lista enlazada de componentes a ensamblar
        self.pasos = ListaEnlazada()  # Agregar lista enlazada para almacenar los pasos de la simulación
        self.tiempo_total = 0  # Atributo para almacenar el tiempo total

    def agregar_paso(self, tiempo, linea, accion):
        paso = PasoSimulacion(tiempo, linea, accion)  # Crear un nuevo paso de simulación
        self.pasos.insertar(paso)  # Insertar el paso en la lista enlazada
        self.tiempo_total += tiempo  # Actualizar el tiempo total

    def obtener_pasos(self):
        return self.pasos  # Retornar los pasos de la simulación

    def __str__(self):
        return f"Producto(nombre: {self.nombre}, secuencia: {self.secuencia})"

class Maquina:
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.lineas = ListaEnlazada()  # Usar lista enlazada para almacenar líneas
        for i in range(1, cantidad_lineas + 1):
            self.lineas.insertar(LineaEnsamblaje(i))  # Insertar líneas en la lista enlazada
        self.productos = ListaEnlazada()  # Usar lista enlazada para almacenar productos

    def agregar_producto(self, producto):
        self.productos.insertar(producto)  # Insertar en la lista enlazada

    def obtener_lineas(self):
        return self.lineas  # Retornar la lista enlazada de líneas

    def obtener_productos(self):
        return self.productos  # Retornar la lista enlazada de productos

    def __str__(self):
        return f"Máquina(nombre: {self.nombre_maquina}, lineas: {self.lineas}, productos: {self.productos})"
