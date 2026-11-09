**Matrícula:** 125052770  
**Pregunta Asignada:** Obtener el total de ingresos por categoría de producto y por mes.

---

## 📊 Respuesta a la Pregunta Asignada

Resultados consolidados tras el procesamiento con el pipeline de MapReduce y cargados en PostgreSQL:

| Categoría | Mes | Ingreso Total ($) |
| :--- | :--- | :--- |
| **Abarrotes** | 2025-01 | $352,898,667.16 |
| **Abarrotes** | 2025-02 | $313,970,496.07 |
| **Abarrotes** | 2025-03 | $343,530,802.97 |
| **Abarrotes** | 2025-04 | $333,904,332.09 |
| **Abarrotes** | 2025-05 | $346,602,747.28 |
| **Abarrotes** | 2025-06 | $331,914,669.00 |
| **Abarrotes** | 2025-07 | $349,911,679.54 |
| **Abarrotes** | 2025-08 | $348,493,291.70 |
| **Abarrotes** | 2025-09 | $335,034,078.03 |
| **Abarrotes** | 2025-10 | $346,131,680.87 |
| **Abarrotes** | 2025-11 | $331,099,550.90 |
| **Abarrotes** | 2025-12 | $345,727,705.05 |
| **Bebidas** | 2025-01 | $340,245,970.85 |
| **Bebidas** | 2025-02 | $314,111,336.54 |
| **Papeleria** | 2025-06 | $328,755,060.71 |
| **Papeleria** | 2025-07 | $341,731,549.10 |
| **Papeleria** | 2025-08 | $344,137,783.84 |
| **Papeleria** | 2025-09 | $336,747,203.83 |
| **Papeleria** | 2025-10 | $345,435,963.46 |
| **Papeleria** | 2025-11 | $333,623,345.02 |
| **Papeleria** | 2025-12 | $345,031,093.90 |
| **Ropa** | 2025-01 | $346,976,373.61 |
| **Ropa** | 2025-02 | $308,640,738.75 |
| **Ropa** | 2025-03 | $343,575,557.06 |
| **Ropa** | 2025-04 | $339,052,362.23 |
| **Ropa** | 2025-05 | $346,203,828.63 |
| **Ropa** | 2025-06 | $335,971,041.44 |
| **Ropa** | 2025-07 | $343,676,270.40 |
| **Ropa** | 2025-08 | $344,789,794.05 |
| **Ropa** | 2025-09 | $335,106,095.54 |
| **Ropa** | 2025-10 | $347,331,930.39 |
| **Ropa** | 2025-11 | $338,294,008.70 |
| **Ropa** | 2025-12 | $344,082,626.19 |

---

## 🚀 Pasos para reproducir el proyecto

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd examen-p2-125052770

   ## Parte E: Teoría

### 1. Modos de Hadoop y HDFS
* **Standalone (Local):** Se ejecuta en un solo proceso JVM y utiliza el sistema de archivos local (no usa HDFS).
* **Pseudo-distribuido:** Se ejecuta en una sola máquina simulando todos los demonios de Hadoop en procesos separados; utiliza HDFS en modo local.
* **Totalmente distribuido:** Se ejecuta en un clúster de múltiples nodos físicos/virtuales separados (Master/Worker); utiliza HDFS de forma real.
* **¿En cuál se usa HDFS?:** Se utiliza en el modo **pseudo-distribuido** y **totalmente distribuido**.

---

### 2. Uso de volúmenes vs. COPY para el Dataset
1. **Eficiencia y rendimiento de construcción:** Copiar un archivo grande (como el dataset de 400 MB) dentro de la imagen incrementa drásticamente el tamaño final del contenedor y vuelve lenta la construcción de la imagen (*build*).
2. **Persistencia y desacoplamiento:** Los volúmenes permiten persistir y manipular datos externamente sin necesidad de reconstruir la imagen de Docker cada vez que el archivo cambie o se genere de nuevo.

---

### 3. Diferencia entre docker compose down y docker compose down -v
* **`docker compose down`:** Detiene y elimina los contenedores y las redes creadas, pero **mantiene intactos los volúmenes de datos**. Por lo tanto, la base de datos conservará su información.
* **`docker compose down -v`:** Detiene y elimina contenedores, redes y **destruye los volúmenes asociados**. La base de datos se eliminará por completo y se perderán todos los registros guardados.

---

### 4. Rendimiento de MapReduce vs. Script Secuencial (400 MB)
* **Por qué no siempre es más rápido:** En archivos pequeños o medianos (como 400 MB), la sobrecarga (*overhead*) de inicializar el framework MapReduce (coordinación de nodos, división de tareas, *shuffle & sort*, I/O de red) supera el tiempo que le toma a un script secuencial simple procesarlo en memoria RAM.
* **Condiciones convenientes:** Conviene a partir de volúmenes de datos masivos (terabytes o petabytes) que no quepan en la memoria de un solo equipo y requieran procesamiento distribuido entre múltiples nodos.

---

### 5. CMD vs ENTRYPOINT y COPY vs ADD
* **CMD vs ENTRYPOINT:**
  * `ENTRYPOINT` define el comando principal que **siempre** se ejecutará cuando el contenedor inicie (difícil de sobrescribir).
  * `CMD` define los argumentos o comandos por defecto que se le pasarán a `ENTRYPOINT`, y se pueden sobrescribir fácilmente al lanzar el contenedor.
* **COPY vs ADD:**
  * `COPY` únicamente copia archivos o carpetas locales desde el host hacia el contenedor.
  * `ADD` hace lo mismo que `COPY`, pero además puede desempaquetar archivos comprimidos (`.tar.gz`) automáticamente y descargar archivos desde URLs remotas.