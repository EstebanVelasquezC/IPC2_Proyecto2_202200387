from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from archivo_xml import ArchivoXML  # Asegúrate de importar la clase correcta
from simulacion import Simulador
from tda import ListaEnlazada
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Variables globales
maquinas = ListaEnlazada()  # Usamos ListaEnlazada en lugar de listas propias de Python
productos = ListaEnlazada()  # Usamos ListaEnlazada en lugar de listas propias de Python
simulador = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicializar')
def inicializar():
    """
    Ruta para inicializar los productos y cargar las máquinas desde el archivo XML.
    """
    global maquinas, productos
    maquinas = ArchivoXML.limpiar_datos()  # Limpiar las estructuras de datos
    try:
        maquinas = ArchivoXML.cargar_maquinas('ruta_al_archivo.xml')  # Cambia la ruta al archivo XML que quieras usar
        flash("Datos inicializados correctamente.")
    except FileNotFoundError:
        flash("Error: No se encontró el archivo XML.")
    return redirect(url_for('index'))

@app.route('/cargar')
def cargar():
    """
    Ruta para mostrar el formulario de carga de archivo.
    """
    return render_template('cargar.html')

@app.route('/cargar_archivo', methods=['POST'])
def cargar_archivo():
    """
    Ruta para manejar el archivo cargado y procesar la configuración.
    """
    global productos
    archivo = request.files['archivo']
    if archivo:
        # Aquí se maneja el archivo cargado, usando el método cargar_configuracion para leerlo
        productos = ArchivoXML.cargar_configuracion(archivo)  # Asegúrate de que cargar_configuracion acepte archivos
        if productos is not None:
            flash("Archivo cargado correctamente.")
        else:
            flash("Error al cargar el archivo. Inténtalo otra vez.")
    else:
        flash("No se seleccionó ningún archivo. Inténtalo otra vez.")
    return redirect(url_for('index'))

@app.route('/simular')
def simular():
    """
    Ruta para mostrar la página de simulación, con los productos disponibles.
    """
    return render_template('simulacion.html', productos=productos)

@app.route('/ejecutar_accion', methods=['POST'])
def ejecutar_accion():
    """
    Ruta para manejar la acción de simular máquinas o generar reportes.
    """
    global simulador
    accion = request.form.get('accion')

    try:
        if accion == 'generar_archivo_salida':
            # Lógica para ejecutar la simulación de la máquina
            if productos is not None and productos.get_tamaño() > 0:  # Verifica que hay productos
                simulador = Simulador(productos)  # Asegúrate de que el simulador acepta la lista de productos
                simulador.iniciar_simulacion()  # Iniciar la simulación

                # Generar archivo de salida XML
                ArchivoXML.guardar_simulacion('archivo_de_salida.xml', simulador.maquinas)
                flash("Archivo de salida generado correctamente.")
                
                # Generar el reporte HTML
                simulador.generar_reporte_html('reporte_simulacion.html')  # Asegúrate de implementar este método
                flash("Reporte HTML generado correctamente.")

                return render_template('simulacion.html', 
                                       report_data=True,  # Se usa True para mostrar los enlaces a los archivos
                                       archivo_xml='archivo_de_salida.xml', 
                                       reporte_html='reporte_simulacion.html')
            else:
                flash("No hay productos disponibles para simular.")
                return redirect(url_for('simular'))

        elif accion == 'descargar_reporte':
            # Lógica para generar el reporte HTML
            archivo_reporte = 'reporte_simulacion.html'
            if os.path.exists(archivo_reporte):
                return send_file(archivo_reporte, as_attachment=True)
            else:
                flash("Error: No se ha generado el reporte.")
                return redirect(url_for('simular'))

    except Exception as e:
        flash(f"Ocurrió un error durante la simulación: {str(e)}")
        return redirect(url_for('simular'))

    return redirect(url_for('index'))

@app.route('/reporte')
def reporte():
    """
    Ruta para mostrar el reporte de simulación una vez completada.
    """
    if simulador is not None:
        report_data = simulador.obtener_reporte()  # Asegúrate de implementar este método en el simulador
        return render_template('reporte.html', report_data=report_data)
    else:
        flash("No se ha realizado ninguna simulación.")
        return redirect(url_for('simular'))

@app.route('/ayuda')
def ayuda():
    """
    Ruta para mostrar una página de ayuda.
    """
    return render_template('ayuda.html', enlace='https://drive.google.com/drive/folders/15IxWDc_9gffhEuVLx13yzwTL4zDmdW7f?usp=sharing')

if __name__ == '__main__':
    app.run(debug=True)
