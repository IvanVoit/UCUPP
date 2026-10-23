#!/usr/bin/env python3
"""
UCUPP - Ultimate Common User Passwords Profiler
Generador exhaustivo de diccionarios de contraseñas basado en datos
personales, para uso EXCLUSIVO en laboratorios propios de ciberseguridad
(máquinas virtuales de prueba, usuarios ficticios, auditorías autorizadas).

A diferencia de CUPP clásico, este script SÍ combina entre sí:
  - palabras base (nombre, apellido, nickname, mascota, hijo, pareja, etc.)
  - sus variantes en leetspeak
  - sus variantes con mayúscula inicial / todo mayúsculas / todo minúsculas
  - fragmentos de cada fecha (día, mes, año completo, año corto)
  - separadores entre palabra y número (nada, "_", "-", ".")
  - caracteres especiales opcionales al final

Uso:
    python3 ucupp.py
    (te irá preguntando los datos, igual que CUPP)

Repositorio: https://github.com/TU_USUARIO/ucupp
Licencia: MIT
"""

import itertools
import sys

LEET_MAP = {
    "a": ["a", "4", "@"],
    "e": ["e", "3"],
    "i": ["i", "1", "!"],
    "o": ["o", "0"],
    "s": ["s", "5", "$"],
    "t": ["t", "7"],
}

SEPARATORS = ["", "_", "-", "."]
SPECIAL_CHARS = ["", "!", "#", "@", "*"]


def leet_variants(word, max_variants=64):
    """Genera variantes leet de una palabra, limitando la cantidad
    para no explotar combinatoriamente (una palabra larga con muchas
    letras sustituibles podría generar miles de variantes ella sola)."""
    word = word.lower()
    options_per_char = []
    for ch in word:
        options_per_char.append(LEET_MAP.get(ch, [ch]))

    variants = set()
    # producto completo de sustituciones posibles
    for combo in itertools.product(*options_per_char):
        variants.add("".join(combo))
        if len(variants) >= max_variants:
            break
    variants.add(word)  # aseguramos que la original está incluida
    return variants


def case_variants(word):
    """minúscula, Mayúscula inicial, MAYÚSCULA completa."""
    return {word.lower(), word.capitalize(), word.upper()}


def date_fragments(date_str):
    """date_str en formato DDMMYYYY. Devuelve una lista de fragmentos
    útiles: dd, mm, yyyy, yy, ddmm, mmyyyy, yyyy, ddmmyyyy, etc."""
    if not date_str or len(date_str) != 8 or not date_str.isdigit():
        return []
    dd, mm, yyyy = date_str[0:2], date_str[2:4], date_str[4:8]
    yy = yyyy[2:4]
    frags = {dd, mm, yyyy, yy, dd + mm, mm + yyyy, mm + yy,
             dd + mm + yyyy, dd + mm + yy, yyyy + mm + dd}
    return [f for f in frags if f]


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def collect_words():
    """Recoge palabras base del usuario (como CUPP, pero puedes meter
    tantas como quieras)."""
    print("\n[+] Introduce los datos de la víctima (deja en blanco si no aplica)\n")
    fields = {
        "Nombre": ask("> Nombre: "),
        "Apellido": ask("> Apellido: "),
        "Nickname": ask("> Nickname: "),
        "Mascota": ask("> Nombre mascota: "),
        "Hijo/a": ask("> Nombre hijo/a: "),
        "Pareja": ask("> Nombre pareja: "),
        "Empresa": ask("> Empresa: "),
    }
    extra = ask("> Palabras clave extra, separadas por coma: ")
    extra_words = [w.strip() for w in extra.split(",") if w.strip()]

    words = [v for v in fields.values() if v] + extra_words
    return words


def collect_dates():
    print("\n[+] Fechas (formato DDMMYYYY, deja en blanco si no aplica)\n")
    dates = []
    for label in ["Nacimiento víctima", "Nacimiento pareja", "Nacimiento hijo/a"]:
        d = ask(f"> {label}: ")
        if d:
            dates.append(d)
    return dates


def generate(words, dates, use_leet, use_numbers, max_total=800_000):
    all_words = set()

    # 1. Variantes de cada palabra base: minúscula/mayúscula + leet opcional
    base_variants = set()
    for w in words:
        for cw in case_variants(w):
            base_variants.add(cw)
        if use_leet:
            for lv in leet_variants(w):
                base_variants.add(lv)
                base_variants.add(lv.capitalize())

    all_words |= base_variants

    # 2. Fragmentos de todas las fechas
    date_frags = set()
    for d in dates:
        date_frags |= set(date_fragments(d))

    # 3. Combinación palabra + separador + fragmento_fecha (+ al revés)
    combined = set()
    if use_numbers and date_frags:
        for w in base_variants:
            for sep in SEPARATORS:
                for frag in date_frags:
                    combined.add(f"{w}{sep}{frag}")
                    combined.add(f"{frag}{sep}{w}")
                    if len(combined) >= max_total:
                        break
                if len(combined) >= max_total:
                    break
            if len(combined) >= max_total:
                break

    all_words |= combined

    # 4. Añadir carácter especial final a una muestra (si no, el archivo
    # se dispara demasiado): lo aplicamos sobre las combinaciones ya hechas
    final_set = set(all_words)
    if len(final_set) < max_total:
        for w in list(all_words):
            for sc in SPECIAL_CHARS:
                if sc:
                    final_set.add(w + sc)
                if len(final_set) >= max_total:
                    break
            if len(final_set) >= max_total:
                break

    return final_set


def main():
    print("=" * 60)
    print(" UCUPP - Ultimate Common User Passwords Profiler")
    print(" SOLO para uso en tus propios laboratorios de pruebas")
    print("=" * 60)

    words = collect_words()
    if not words:
        print("[-] No has introducido ninguna palabra base. Saliendo.")
        sys.exit(1)

    dates = collect_dates()

    use_leet = ask("> ¿Activar leetspeak? (Y/n): ").lower() != "n"
    use_numbers = ask("> ¿Combinar con fechas? (Y/n): ").lower() != "n"
    max_total_str = ask("> Límite máximo de combinaciones [800000]: ")
    max_total = int(max_total_str) if max_total_str.isdigit() else 800_000

    print("\n[+] Generando combinaciones, esto puede tardar unos segundos...")
    result = generate(words, dates, use_leet, use_numbers, max_total)

    out_file = ask("> Nombre del archivo de salida [combogen.txt]: ") or "combogen.txt"
    with open(out_file, "w") as f:
        for w in sorted(result):
            f.write(w + "\n")

    print(f"\n[+] Hecho. Se generaron {len(result)} combinaciones.")
    print(f"[+] Guardado en: {out_file}")


if __name__ == "__main__":
    main()
