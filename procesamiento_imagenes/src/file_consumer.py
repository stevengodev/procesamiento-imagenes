import threading
from utils.utilidades import extraer_periodico, extraer_fecha_publicacion, extraer_nombre_archivo
from datetime import datetime
from queue import Empty
import time
import mimetypes
from models import db, Archivo, DivisionPolitica, UnidadMilitar
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import google.generativeai as genai
from utils.utilidades import generar_prompt
from config import Config
import json


class FileConsumer(threading.Thread):
    def __init__(self, queue, app):
        super().__init__()
        self.queue = queue
        self.app = app



    def run(self):
        with self.app.app_context():
            while True:
                try:
                    file_path = self.queue.get(timeout=1)
                    print(f"Processing file: {file_path} by {threading.current_thread().name}")

                    file_name = extraer_nombre_archivo(file_path)
                    newspaper_name = extraer_periodico(file_name)
                    publication_date = extraer_fecha_publicacion(file_name)
                    
                    datetime_ocr = datetime.now()
                    start_time_ocr = time.time()
                    content = self.get_text_from_pdf_ocr(file_path)
                    end_time_ocr = time.time()
                    total_time_ocr = end_time_ocr - start_time_ocr

                    datetime_ia = datetime.now()
                    start_time_ia = time.time()
                    txt_ia = self.process_text_with_ia(content)
                    end_time_ia = time.time()
                    total_time_ia = end_time_ia - start_time_ia

                    if txt_ia:
                        unidades_militares = txt_ia.get('UnidadesMilitares', [])
                        divisiones_politicas = txt_ia.get('DivisionesPoliticas', [])
                    else:
                        unidades_militares = []
                        divisiones_politicas = []

                    print(unidades_militares)
                    print(divisiones_politicas)

                    self.save_to_database(file_name, newspaper_name, file_path, publication_date,
                                          datetime_ocr, datetime_ia, total_time_ocr, total_time_ia,
                                          unidades_militares, divisiones_politicas)

                    self.queue.task_done()
                except Empty:
                    break



    def get_text_from_pdf_ocr(self, file_path):
        try:
            mime_type, _ = mimetypes.guess_type(file_path)

            client = documentai.DocumentProcessorServiceClient(
                client_options=ClientOptions(api_endpoint=f"{Config.DOCUMENT_AI_LOCATION}-{Config.DOCUMENT_AI_ENDPOINT}"))
            name = client.processor_path(Config.DOCUMENT_AI_PROJECT_ID, Config.DOCUMENT_AI_LOCATION, Config.DOCUMENT_AI_PROCESSOR_ID)
            with open(file_path, "rb") as image:
                image_content = image.read()
            
            raw_document = documentai.RawDocument(
                content=image_content, mime_type=mime_type)
            
            request = documentai.ProcessRequest(name=name, raw_document=raw_document)
            response = client.process_document(request=request)
            document = response.document
            return document.text

        except Exception as e:
            print(f"Error in OCR: {e}")
            return None



    def process_text_with_ia(self, text):
        
        genai.configure(api_key=Config.GENERATIVE_AI_API_KEY)
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(generar_prompt(text))

        try:
            json_data = json.loads(response.text)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in IA processing: {e}")
            return None



    def save_to_database(self, file_name, newspaper_name, file_path, publication_date,
                        datetime_ocr, datetime_ia, total_time_ocr, total_time_ia,
                        unidades_militares, divisiones_politicas):
        try:
            with self.app.app_context():
                nuevo_archivo = Archivo(
                    fecha_publicacion=publication_date,
                    nombre=file_name,
                    nombre_periodico=newspaper_name,
                    ruta=file_path,
                    tiempo_procesamiento_ia=total_time_ia,
                    fecha_procesamiento_ia=datetime_ia,
                    tiempo_procesamiento_ocr=total_time_ocr,
                    fecha_procesamiento_ocr=datetime_ocr
                )

                db.session.add(nuevo_archivo)

                db.session.commit()  # Confirmar la transacción para que se genere el ID
            
                # Recuperar el id
                archivo_id = nuevo_archivo.id

                # Guardar divisiones políticas
                if isinstance(divisiones_politicas, list):
                    for division in divisiones_politicas:
                        if isinstance(division, str):  
                            nueva_division = DivisionPolitica(
                                archivo_id=archivo_id,
                                nombre=division
                            )
                            db.session.add(nueva_division)

                # Guardar unidades militares
                if isinstance(unidades_militares, list):
                    for unidad in unidades_militares:
                        if isinstance(unidad, str):  
                            nueva_unidad = UnidadMilitar(
                                archivo_id=archivo_id,
                                nombre=unidad
                            )
                            db.session.add(nueva_unidad)

                db.session.commit()  

        except Exception as e:
            print(f"Error saving to database: {e}")

