from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from archivo_xml import ArchivoXML  # Asegúrate de importar la clase correcta
from simulacion import Simulador
from tda import ListaEnlazada
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Variables globales
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
    global productos
    productos = ArchivoXML.limpiar_datos()  # Limpiar las estructuras de datos
    try:
        productos = ArchivoXML.cargar_maquinas('ruta_al_archivo.xml')  # Cambia la ruta al archivo XML que quieras usar
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
            flash("Error al cargar el archivo.")
    else:
        flash("No se seleccionó ningún archivo.")
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

    if accion == 'simular':
        # Lógica para ejecutar la simulación de la máquina
        if productos is not None:
            simulador = Simulador(productos)  # Asumiendo que el simulador acepta la lista de productos
            simulador.iniciar_simulacion()  # Iniciar la simulación
            flash("Simulación de máquinas ejecutada.")
            return redirect(url_for('reporte'))  # Redirigir a la página del reporte
        else:
            flash("No hay productos disponibles para simular.")
            return redirect(url_for('simular'))

    elif accion == 'reporte':
        # Lógica para generar el reporte HTML
        archivo_reporte = 'reporte_simulacion.html'
        ArchivoXML.guardar_reporte_html(archivo_reporte, productos)  # Asegúrate de implementar este método
        flash("Reporte HTML generado correctamente.")
        return send_file(archivo_reporte, as_attachment=True)

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
    return render_template('ayuda.html')

if __name__ == '__main__':
    app.run(debug=True)
