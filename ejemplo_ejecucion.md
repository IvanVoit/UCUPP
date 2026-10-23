# Ejemplo de ejecución

Este es un ejemplo real de uso de UCUPP, con datos ficticios de un usuario de
laboratorio.

## Entrada

```
$ python3 ucupp.py

[+] Introduce los datos de la víctima (deja en blanco si no aplica)

> Nombre: Fernando
> Apellido: Puertas
> Nickname: fernando
> Nombre mascota: Kiwi
> Nombre hijo/a: Ivan
> Nombre pareja:
> Empresa: Eivexa
> Palabras clave extra, separadas por coma:

[+] Fechas (formato DDMMYYYY, deja en blanco si no aplica)

> Nacimiento víctima: 01041978
> Nacimiento pareja:
> Nacimiento hijo/a: 25072008
> ¿Activar leetspeak? (Y/n): Y
> ¿Combinar con fechas? (Y/n): Y
> Límite máximo de combinaciones [800000]:
> Nombre del archivo de salida [combogen.txt]: ejemplo_salida.txt
```

## Salida

```
[+] Generando combinaciones, esto puede tardar unos segundos...

[+] Hecho. Se generaron 148925 combinaciones.
[+] Guardado en: ejemplo_salida.txt
```

## Comprobación

Con estos datos, UCUPP sí genera combinaciones cruzadas como:

```
f3rn4nd0_1978
Fernando1978
fernando-01041978
F3rn4nd0.1978!
1978_fernando
```

A diferencia de CUPP clásico, que con los mismos datos de entrada **no**
llega a generar `f3rn4nd0_1978`, porque no combina su modo leet con los
fragmentos de fecha usando separadores.

## Uso posterior con John the Ripper

```bash
sudo unshadow /etc/passwd /etc/shadow > /tmp/hashes.txt
john --wordlist=ejemplo_salida.txt /tmp/hashes.txt
john --show /tmp/hashes.txt
```
