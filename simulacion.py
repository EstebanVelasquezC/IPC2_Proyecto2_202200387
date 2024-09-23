# simulacion.py

from maquina import Maquina
from tda import ListaEnlazada

class Simulador:
    def __init__(self, maquina):
        self.maquina = maquina  # La máquina que vamos a simular

    def simular(self, producto):
        tiempo_total = 0
        pasos = ListaEnlazada()  # Usar lista enlazada para almacenar los pasos de la simulación
        componentes = producto.secuencia.split()  # Divide la secuencia

        # Inicializar acciones en cada línea de producción como listas enlazadas
        acciones_por_linea = [ListaEnlazada() for _ in range(self.maquina.cantidad_lineas)]

        # Registrar todas las acciones
        for componente in componentes:
            if len(componente) < 4:  # Verifica si el formato de paso es correcto
                continue

            # Extraer la línea y el componente del paso
            try:
                linea = int(componente[1])  # Línea de ensamblaje
                componente_num = int(componente[3:])  # Número del componente
            except ValueError:
                print(f"Error en el formato de la secuencia: {componente}")
                continue

            # Validar si la línea de ensamblaje es válida
            if linea < 1 or linea > self.maquina.cantidad_lineas:
                print(f"La línea {linea} no es válida en la máquina {self.maquina.nombre_maquina}")
                continue

            # Registrar el movimiento del brazo en todas las líneas antes de ensamblar
            tiempo_total += 2  # Suponiendo que cada acción de mover el brazo tarda 2 segundos

            for i in range(1, self.maquina.cantidad_lineas + 1):
                if i == linea:
                    acciones_por_linea[i - 1].insertar(f"Ensamblar Componente {componente_num}")
                    pasos.insertar(f"Segundo {tiempo_total}: Línea {i} - Ensamblar Componente {componente_num}")
                    producto.agregar_paso(tiempo_total, i, f"Ensamblar Componente {componente_num}")
                else:
                    acciones_por_linea[i - 1].insertar(f"Mover Brazo - Componente {componente_num}")
                    pasos.insertar(f"Segundo {tiempo_total}: Línea {i} - Mover Brazo - Componente {componente_num}")
                    producto.agregar_paso(tiempo_total, i, f"Mover Brazo - Componente {componente_num}")

            # Después de registrar todas las acciones, agregar "No hace nada" para líneas que no están activas
            for j in range(1, self.maquina.cantidad_lineas + 1):
                if j != linea:
                    pasos.insertar(f"Segundo {tiempo_total}: Línea {j} - No hace nada")
                    producto.agregar_paso(tiempo_total, j, "No hace nada")

        # Almacenar el tiempo total en el producto
        producto.tiempo_total = tiempo_total  # Agregar un atributo para almacenar el tiempo total

        # Retornar el tiempo total y los pasos
        return tiempo_total, pasos

    def mostrar_resultados(self, tiempo_total, pasos):
        print(f"Tiempo total para ensamblar el producto: {tiempo_total} segundos")
        print("Pasos realizados:")
        for paso in pasos.recorrer():
            print(paso)
