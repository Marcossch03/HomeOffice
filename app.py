from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from collections import Counter

app = Flask(__name__)

# 1. HABILITAR CORS (Crucial para Google Sites)
CORS(app)

ARCHIVO_JSON = "data.json"
# Usamos rutas absolutas para evitar errores en la nube
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_COMPLETA_JSON = os.path.join(BASE_DIR, ARCHIVO_JSON)

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
MAX_POR_DIA = 8

# ================================
#   PERSISTENCIA
# ================================

def datos_iniciales():
    return {
        "Esteban V.": [],
        "Celeste A.": [],
        "Sebastián A.": [],
        "Demerith G.": [],
        "Laura V.": [],
        "Pablo C.": [],
        "Agustin P.": [],
        "Marcos S.": [],
        "Jonathan A.": [],
        "Samanta S.": [],
        "Veronica T.": [],
        "Marina D.": [],
        "Mariana M.": [],
        "María E.": [],
        "Mauro G.": [],
        "Agustin G.": [],
    }

def cargar_datos():
    if os.path.exists(RUTA_COMPLETA_JSON):
        with open(RUTA_COMPLETA_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return datos_iniciales()
    data = datos_iniciales()
    guardar_datos(data)
    return data

def guardar_datos(data):
    with open(RUTA_COMPLETA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Cargar en memoria al iniciar
empleados = cargar_datos()

# ================================
#   CÁLCULOS
# ================================

def contar_asistencia():
    c = Counter()
    for lista_dias in empleados.values():
        for d in lista_dias:
            c[d] += 1
    return c

# ================================
#   RUTAS (API JSON)
# ================================

@app.route("/api/datos", methods=["GET"])
def obtener_datos():
    """Esta ruta le entrega al Google Site el estado actual de la tabla"""
    conteo = contar_asistencia()
    return jsonify({
        "empleados": empleados,
        "conteo": conteo,
        "dias": dias,
        "max_por_dia": MAX_POR_DIA
    })

@app.route("/toggle", methods=["POST"])
def toggle():
    # Recibimos JSON en lugar de Form Data
    data = request.json
    empleado = data.get("empleado")
    dia = data.get("dia")

    if empleado not in empleados or dia not in dias:
        return jsonify({"status": "error", "message": "Datos inválidos"}), 400

    lista = empleados[empleado]
    conteo_actual = contar_asistencia()

    # Lógica de toggle
    if dia in lista:
        lista.remove(dia) # Quitar asistencia
        accion = "removido"
    else:
        # Validar cupo antes de agregar
        if conteo_actual.get(dia, 0) >= MAX_POR_DIA:
             return jsonify({"status": "error", "message": f"Cupo lleno para el {dia}"}), 400
        lista.append(dia)
        accion = "agregado"

    guardar_datos(empleados)

    # Devolvemos el nuevo estado para que el frontend se actualice solo
    return jsonify({
        "status": "success",
        "accion": accion,
        "nuevo_conteo": contar_asistencia(),
        "empleados": empleados
    })

@app.route("/reset", methods=["POST"])
def reset():
    for emp in empleados:
        empleados[emp] = []
    guardar_datos(empleados)
    return jsonify({"status": "success", "message": "Tabla reseteada"})

if __name__ == "__main__":
    app.run(debug=True)