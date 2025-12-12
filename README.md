# Gestor Home Office - Contratos (MVP)

Aplicación web interna para gestionar presencialidad (P/H) por empleado y día, con:
- Toggle por celda (P <-> H)
- Totales por día
- Límite: máximo 8 presenciales por día (solo Contratos)
- Reset semana (todo blanco)
- Persistencia local en `data.json`

## Requisitos
- Python 3.x
- Flask (ver `requirements.txt`)

## Ejecutar local
```bash
pip install -r requirements.txt
python app.py
