import re
import os
from datetime import datetime
from models import db, Archivo
from flask import jsonify


def extraer_periodico(nombre_archivo):
    # Mapeo de abreviaciones a nombres completos
    periodicos = {
        "EL_COLOMBIANO": "EL_COLOMBIANO",
        "EL_ESPECTADOR": "EL_ESPECTADOR",
        "EL_HERALDO": "EL_HERALDO",
        "EL_MUNDO": "EL_MUNDO",
        "EL_NUEVO_SIGLO": "EL_NUEVO_SIGLO",
        "EL_PA_S": "EL_PAIS",  # Mapeo para la abreviación
        "EL_TIEMPO": "EL_TIEMPO",
        "VANGUARDIA_LIBERAL": "VANGUARDIA_LIBERAL",
        "VOZ": "VOZ"
    }
    
    # Buscar el nombre del periódico en el nombre del archivo
    for abreviacion, nombre_completo in periodicos.items():
        if abreviacion in nombre_archivo:
            return nombre_completo


def extraer_fecha_publicacion(nombre_archivo):
    patron = r'\d{2}-\d{2}-\d{4}'
    coincidencia = re.search(patron, nombre_archivo)
    
    if coincidencia:
        fecha_str = coincidencia.group()
        # Convertir la fecha a formato YYYY-MM-DD
        fecha_obj = datetime.strptime(fecha_str, "%d-%m-%Y")
        return fecha_obj.strftime("%Y-%m-%d")
    else:
        return None


def extraer_nombre_archivo(ruta):
    # Obtener el nombre del archivo desde la ruta completa
    nombre_archivo = os.path.basename(ruta)
    return nombre_archivo


def extraer_resultados():
    try:
        # Obtener el número total de archivos
        num_files = Archivo.query.count()
        
        # Obtener los tiempos de procesamiento OCR e IA
        total_ocr_time = db.session.query(db.func.sum(Archivo.tiempo_procesamiento_ocr)).scalar() or 0
        total_ai_time = db.session.query(db.func.sum(Archivo.tiempo_procesamiento_ia)).scalar() or 0

        # Calcular el tiempo promedio
        average_ocr_time = total_ocr_time / num_files if num_files > 0 else 0
        average_ai_time = total_ai_time / num_files if num_files > 0 else 0

        return jsonify({
            "num_files_processed": num_files,
            "ocr_total_time": total_ocr_time,
            "ocr_average_time": average_ocr_time,
            "ai_total_time": total_ai_time,
            "ai_average_time": average_ai_time
        })
    except Exception as e:
        print(f"Error fetching results from database: {e}")
        return jsonify({"error": "Error fetching results"}), 500


def generar_prompt(text):
    return (
        f"Dado el siguiente texto, por favor, extrae la información relevante y devuélvela en formato JSON. El JSON debe contener dos secciones:\n\n"
        f"1. **Unidades Militares**: Incluye los nombres de las unidades militares mencionadas en el texto, tales como Batallones, Brigadas, Escuadrones, y Fuerzas de Tarea.\n\n"
        f"2. **Divisiones Políticas**: Incluye los nombres de las divisiones políticas mencionadas en el texto, tales como Departamentos, Ciudades, Municipios, Corregimientos y Veredas.\n\n"
        f"Aquí está el texto:\n{text}\n\n"
        f"Por favor, devuelve los datos en el siguiente formato JSON sin incluir comillas alrededor del código:\n"
        f"{{\n"
        f"  \"UnidadesMilitares\": [\n"
        f"    \"Nombre de unidad militar 1\",\n"
        f"    \"Nombre de unidad militar 2\",\n"
        f"    ...\n"
        f"  ],\n"
        f"  \"DivisionesPoliticas\": [\n"
        f"    \"Nombre de división política 1\",\n"
        f"    \"Nombre de división política 2\",\n"
        f"    ...\n"
        f"  ]\n"
        f"}}"
    )

