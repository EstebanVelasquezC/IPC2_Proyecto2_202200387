import xml.etree.ElementTree as ET
from xml.dom import minidom  # Para dar formato al XML
from maquina import Maquina, Producto, Componente
from tda import ListaEnlazada

class ArchivoXML:

    @staticmethod
    def cargar_maquinas(archivo):
        try:
            tree = ET.parse(archivo)
            root = tree.getroot()
            maquinas = ListaEnlazada()  # Usar lista enlazada para almacenar máquinas

            for maquina_elem in root.findall('Maquina'):
                nombre_maquina = maquina_elem.find('NombreMaquina').text
                cantidad_lineas = int(maquina_elem.find('CantidadLineasProduccion').text)
                cantidad_componentes = int(maquina_elem.find('CantidadComponentes').text)
                tiempo_ensamblaje = int(maquina_elem.find('TiempoEnsamblaje').text)

                nueva_maquina = Maquina(nombre_maquina, cantidad_lineas, cantidad_componentes)

                # Cargar los componentes para cada línea de ensamblaje
                for linea in nueva_maquina.obtener_lineas().recorrer():
                    for i in range(1, cantidad_componentes + 1):
                        componente = Componente(i, tiempo_ensamblaje)
                        linea.agregar_componente(componente)

                # Cargar productos
                productos_elem = maquina_elem.find('ListadoProductos')
                if productos_elem is not None:  # Verificar si existen productos
                    for producto_elem in productos_elem:
                        nombre_producto = producto_elem.find('nombre').text
                        elaboracion = producto_elem.find('elaboracion').text.strip()
                        nuevo_producto = Producto(nombre_producto, elaboracion)
                        nueva_maquina.agregar_producto(nuevo_producto)

                maquinas.insertar(nueva_maquina)  # Insertar máquina en la lista enlazada

            return maquinas  # Retorna la lista de máquinas cargadas
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return None

    @staticmethod
    def cargar_configuracion(archivo):
        """
        Cargar la configuración desde un archivo XML.
        En este caso, se cargan los productos de ensamblaje y sus detalles.
        """
        try:
            tree = ET.parse(archivo)
            root = tree.getroot()
            productos = ListaEnlazada()  # Usar lista enlazada para almacenar productos

            # Asumiendo que el archivo tiene una estructura como:
            # <Configuracion>
            #   <Producto>
            #       <Nombre>Producto1</Nombre>
            #       <Elaboracion>...</Elaboracion>
            #   </Producto>
            # </Configuracion>
            for producto_elem in root.findall('Producto'):
                nombre_producto = producto_elem.find('Nombre').text
                elaboracion = producto_elem.find('Elaboracion').text.strip()
                nuevo_producto = Producto(nombre_producto, elaboracion)
                productos.insertar(nuevo_producto)  # Insertar el producto en la lista enlazada

            return productos  # Retornar la lista enlazada de productos
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML de configuración: {e}")
            return None

    @staticmethod
    def guardar_simulacion(archivo, maquinas):
        root = ET.Element('SalidaSimulacion')  # Crear el nodo raíz

        for maquina in maquinas.recorrer():
            maquina_elem = ET.SubElement(root, 'Maquina')
            ET.SubElement(maquina_elem, 'Nombre').text = maquina.nombre_maquina
            
            listado_productos = ET.SubElement(maquina_elem, 'ListadoProductos')

            for producto in maquina.obtener_productos().recorrer():
                producto_elem = ET.SubElement(listado_productos, 'Producto')
                ET.SubElement(producto_elem, 'Nombre').text = producto.nombre
                
                # Guardar el tiempo total del producto
                tiempo_total_elem = ET.SubElement(producto_elem, 'TiempoTotal')
                tiempo_total_elem.text = str(producto.tiempo_total)

                # Estructura para los pasos de elaboración
                elaboracion_optima_elem = ET.SubElement(producto_elem, 'ElaboracionOptima')

                for paso in producto.obtener_pasos().recorrer():
                    tiempo_elem = ET.SubElement(elaboracion_optima_elem, 'Paso')
                    ET.SubElement(tiempo_elem, 'Tiempo').text = str(paso.tiempo)
                    ET.SubElement(tiempo_elem, 'Linea').text = str(paso.linea)
                    ET.SubElement(tiempo_elem, 'Accion').text = paso.accion

        # Convertir el árbol XML a una cadena
        rough_string = ET.tostring(root, 'utf-8')

        # Usar minidom para hacer "prettify" y dar formato con indentación
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ")  # 4 espacios de indentación

        # Escribir el archivo formateado
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        print(f"Archivo de simulación guardado en {archivo}")

    @staticmethod
    def guardar_reporte_html(archivo, maquinas):
        with open(archivo, 'w', encoding='utf-8') as f:
            # Escribir la cabecera HTML
            f.write("<html>\n<head>\n<title>Reporte de Simulación</title>\n")
            f.write("<style>body { font-family: Arial, sans-serif; } .maquina { margin-bottom: 20px; } ")
            f.write("h1, h2, h3, h4 { color: #333; } </style>\n</head>\n<body>\n")
            f.write("<h1>Reporte de Simulación</h1>\n")

            # Iterar sobre las máquinas y productos
            for maquina in maquinas.recorrer():
                f.write(f"<div class='maquina'>\n<h2>Máquina: {maquina.nombre_maquina}</h2>\n")
                
                # Encabezado del reporte
                for producto in maquina.obtener_productos().recorrer():
                    f.write(f"<h3>Producto: {producto.nombre}</h3>\n")
                    f.write(f"<p><strong>Tiempo Total de Ensamblaje:</strong> {producto.tiempo_total} segundos</p>\n")
                    
                    f.write("<table border='1'>\n<tr><th>Tiempo</th>")
                    for i in range(1, maquina.cantidad_lineas + 1):
                        f.write(f"<th>Línea {i}</th>")
                    f.write("</tr>\n")

                    # Inicialización de variables para la construcción de la tabla
                    filas = ""

                    # Recolectar pasos de cada producto
                    for segundo in range(1, producto.tiempo_total + 1):
                        fila_actual = f"<tr><td>{segundo}s</td>"

                        # Muestra todos los movimientos del brazo y componentes
                        for i in range(1, maquina.cantidad_lineas + 1):
                            accion = "No hace nada"  # Acción por defecto
                            for paso in producto.obtener_pasos().recorrer():
                                if paso.tiempo == segundo and paso.linea == i:
                                    accion = paso.accion
                                    break
                            fila_actual += f"<td>{accion}</td>"

                        fila_actual += "</tr>\n"  # Cierre de la fila
                        filas += fila_actual

                    # Escribir filas de la tabla
                    f.write(filas)

                    f.write("</table></div>\n")
            f.write("</body>\n</html>")
            print(f"Reporte guardado en {archivo}")

    @staticmethod
    def limpiar_datos():
        """
        Método que restablece las estructuras de datos a su estado inicial.
        """
        return ListaEnlazada()  # Retorna una nueva lista enlazada vacía para reiniciar las máquinas
