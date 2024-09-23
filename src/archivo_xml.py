import xml.etree.ElementTree as ET
from maquina import Maquina, LineaProduccion

class ArchivoXML:
    """Clase para leer archivos XML y configurar una máquina."""
    
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_maquina(self):
        """Lee el archivo XML y retorna una instancia de la clase Maquina."""
        try:
            arbol = ET.parse(self.archivo)
            raiz = arbol.getroot()

            # Obtener el nombre de la máquina
            nombre_maquina = raiz.attrib['nombre']
            maquina = Maquina(nombre_maquina)

            # Recorrer las líneas de producción en el XML
            for linea_xml in raiz.findall('linea'):
                nombre_linea = linea_xml.attrib['nombre']
                linea = LineaProduccion(nombre_linea)

                # Recorrer los componentes dentro de la línea
                for componente_xml in linea_xml.findall('componente'):
                    componente_nombre = componente_xml.text
                    linea.componentes.agregar(componente_nombre)

                # Agregar la línea a la máquina
                maquina.agregar_linea(linea)
            
            return maquina

        except ET.ParseError as e:
            print(f"Error al leer el archivo XML: {e}")
            return None
