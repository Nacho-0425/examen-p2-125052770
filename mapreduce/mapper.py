#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id"):
        continue

    fields = line.split(",")
    if len(fields) != 8:
        continue

    try:
        fecha_hora = fields[1]
        categoria = fields[3]
        cantidad = float(fields[5])
        precio_unitario = float(fields[6])

        mes = fecha_hora.split(" ")[0][:7]
        ingreso_total = cantidad * precio_unitario

        print(f"{categoria}\t{mes}\t{ingreso_total}")
    except ValueError:
        continue
