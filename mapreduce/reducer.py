#!/usr/bin/env python3
import sys

current_key = None
total_revenue = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        categoria, mes, ingreso = line.split("\t")
        ingreso = float(ingreso)
    except ValueError:
        continue

    key = f"{categoria}\t{mes}"

    if current_key == key:
        total_revenue += ingreso
    else:
        if current_key:
            cat, m = current_key.split("\t")
            print(f"{cat}\t{m}\t{round(total_revenue, 2)}")
        current_key = key
        total_revenue = ingreso

if current_key:
    cat, m = current_key.split("\t")
    print(f"{cat}\t{m}\t{round(total_revenue, 2)}")
