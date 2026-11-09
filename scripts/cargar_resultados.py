import os
import sys
import psycopg2

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "datamart")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres_password")

def main():
    part_file = sys.argv[1] if len(sys.argv) > 1 else "/data/output/resultado/part-00000"

    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingresos_categoria_mes (
            id SERIAL PRIMARY KEY,
            categoria VARCHAR(100),
            mes VARCHAR(10),
            ingreso_total NUMERIC(15, 2)
        );
    """)

    with open(part_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                cat, mes, ingreso = parts[0], parts[1], float(parts[2])
                cur.execute(
                    "INSERT INTO ingresos_categoria_mes (categoria, mes, ingreso_total) VALUES (%s, %s, %s)",
                    (cat, mes, ingreso)
                )

    conn.commit()
    cur.close()
    conn.close()
    print("Resultados cargados exitosamente a PostgreSQL.")

if __name__ == "__main__":
    main()
