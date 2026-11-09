#!/usr/bin/env python3
import sys
from collections import defaultdict

def run_secuencial(filepath):
    ingresos = defaultdict(float)
    with open(filepath, "r", encoding="utf-8") as f:
        header = next(f, None)
        for line in f:
            fields = line.strip().split(",")
            if len(fields) != 8:
                continue
            try:
                mes = fields[1].split(" ")[0][:7]
                categoria = fields[3]
                ingreso = float(fields[5]) * float(fields[6])
                ingresos[(categoria, mes)] += ingreso
            except ValueError:
                continue

    for (cat, m), total in sorted(ingresos.items()):
        print(f"{cat}\t{m}\t{round(total, 2)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_secuencial(sys.argv[1])
