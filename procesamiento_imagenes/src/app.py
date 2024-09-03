
import time
from file_consumer import FileConsumer
from file_producer import FileProducer
from queue import Queue
from flask import Flask, render_template, jsonify, request
from models import db
from config import Config
from flasgger import Swagger
from utils.utilidades import extraer_resultados

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

swagger = Swagger(app)

#Rutas para renderizar contenido
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/results-page', methods=['GET'])
def results_page():
    return render_template('resultados.html')


#Endpoints - Apis
@app.route('/api/process_files', methods=['GET'])
def process_files():

    """
    Procesa archivos en un directorio utilizando múltiples hilos.
    ---
    parameters:
      - name: num_threads
        in: query
        type: integer
        required: true
        description: Número de hilos consumidores a utilizar.
    responses:
      200:
        description: Procesamiento de archivos completado exitosamente.
        schema:
          type: object
          properties:
            mensaje:
              type: string
              description: Mensaje de confirmación del procesamiento.
              example: Procesamiento completo
            tiempo_tomado:
              type: string
              description: Tiempo total tomado para el procesamiento en segundos.
              example: 12.34 segundos
      400:
        description: Error en los parámetros de entrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error en caso de parámetros inválidos.
              example: Error en el parámetro 'num_threads'
      500:
        description: Error interno del servidor.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error en caso de fallo en el procesamiento.
              example: Error durante el procesamiento de archivos
    """

    global result_data

    num_threads = int(request.args.get('num_threads'))
    queue = Queue()
    directory = Config.FILES_DIRECTORY

    start_time = time.time()

    # Crear y empezar el hilo productor
    producer = FileProducer(queue, directory)
    producer.start()
    
    consumers = []
    for i in range(num_threads):
        consumer = FileConsumer(queue, app)
        #consumer.setName(f"Consumer-{i}")
        consumers.append(consumer)
        consumer.start()

    # Esperar a que el productor termine
    producer.join()

    # Esperar a que todos los consumidores terminen
    for consumer in consumers:
        consumer.join()

    end_time = time.time()

    # Calcular y mostrar el tiempo transcurrido
    elapsed_time = end_time - start_time
    return jsonify({"mensaje": "Procesamiento completo", "tiempo_tomado": f"{elapsed_time:.2f} segundos"})


@app.route('/api/results', methods=['GET'])
def results():

    """
    Obtiene estadísticas de procesamiento de archivos.
    ---
    responses:
      200:
        description: Estadísticas de procesamiento de archivos
        schema:
          type: object
          properties:
            num_files_processed:
              type: integer
              description: Número total de archivos procesados
              example: 150
            ocr_total_time:
              type: number
              format: float
              description: Tiempo total de procesamiento OCR en segundos
              example: 1200.5
            ocr_average_time:
              type: number
              format: float
              description: Tiempo promedio de procesamiento OCR en segundos
              example: 8.0
            ai_total_time:
              type: number
              format: float
              description: Tiempo total de procesamiento IA en segundos
              example: 1500.0
            ai_average_time:
              type: number
              format: float
              description: Tiempo promedio de procesamiento IA en segundos
              example: 10.0
      500:
        description: Error al obtener los resultados
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error
              example: Error fetching results
    """

    return extraer_resultados()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

