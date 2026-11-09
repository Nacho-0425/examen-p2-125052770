import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "datamart"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres_password"),
        port=os.getenv("DB_PORT", "5432")
    )

class Record(BaseModel):
    categoria: str
    mes: str
    ingreso_total: float

@app.get("/resultados")
def get_todos():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM ingresos_categoria_mes ORDER BY categoria, mes;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/resultados/{categoria}")
def get_por_clave(categoria: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM ingresos_categoria_mes WHERE LOWER(categoria) = LOWER(%s);", (categoria,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return rows

@app.post("/resultados")
def create_registro(record: Record):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ingresos_categoria_mes (categoria, mes, ingreso_total) VALUES (%s, %s, %s) RETURNING id;",
        (record.categoria, record.mes, record.ingreso_total)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Registro creado exitosamente", "id": new_id}
