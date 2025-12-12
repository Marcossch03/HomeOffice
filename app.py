from flask import Flask, render_template, request, redirect, url_for
import json
import os
from collections import Counter

app = Flask(__name__)

ARCHIVO_JSON = "data.json"

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
MAX_POR_DIA = 8


# ================================
#   PERSISTENCIA
# ================================

def datos_iniciales():
    """Se usa si no existe data.json."""
    return {
        "Esteban V.": [],
        "Celeste A.": [],
        "Sebastián A.": [],
        "Demerith G.": [],
        "Laura V.": [],
        "Pablo C.": [],
        "Agustin P.": [],
        "Marcos S.": [],
        "Marina D.": [],
        "Mariana M.": [],
        "María E.": [],
        "Mauro G.": [],
        "Agustin G.": [],
    }

def cargar_datos():
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    data = datos_iniciales()
    guardar_datos(data)
    return data

def guardar_datos(data):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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
#   RUTAS
# ================================

@app.route("/")
def contratos():
    conteo = contar_asistencia()
    return render_template(
        "Gerencia_Contratos.html",
        empleados=empleados,
        dias=dias,
        conteo=conteo,
        max_por_dia=MAX_POR_DIA
    )

@app.route("/toggle", methods=["POST"])
def toggle():
    empleado = request.form["empleado"]
    dia = request.form["dia"]

    # Validaciones básicas
    if empleado not in empleados:
        return redirect(url_for("contratos"))
    if dia not in dias:
        return redirect(url_for("contratos"))

    lista = empleados[empleado]

    # Si vamos a AGREGAR presencialidad, validar cupo
    if dia not in lista:
        if contar_asistencia().get(dia, 0) >= MAX_POR_DIA:
            return redirect(url_for("contratos"))
        lista.append(dia)
    else:
        # Si ya estaba, quitar (siempre permitido)
        lista.remove(dia)

    guardar_datos(empleados)
    return redirect(url_for("contratos"))

@app.route("/reset", methods=["POST"])
def reset():
    # Reset “todo blanco”
    for emp in empleados:
        empleados[emp] = []
    guardar_datos(empleados)
    return redirect(url_for("contratos"))


if __name__ == "__main__":
    # Para producción interna, ideal:
    app.run(host="0.0.0.0", debug=False)
