# UCUPP — Ultimate Common User Passwords Profiler

UCUPP es un generador de diccionarios de contraseñas basado en datos personales
(nombre, apellidos, fechas de nacimiento, mascotas, familiares, palabras clave...),
pensado para auditorías de seguridad, pentesting y laboratorios de aprendizaje
en ciberseguridad.

Está inspirado en el clásico [CUPP (Common User Passwords Profiler)](https://github.com/Mebus/cupp),
pero resuelve una de sus mayores limitaciones: **CUPP no combina entre sí todas
las transformaciones que aplica** (leetspeak, fechas, mayúsculas, caracteres
especiales), por lo que muchas contraseñas humanas realistas —como
`f3rn4nd0_1978`— nunca llegan a aparecer en el diccionario generado, aunque
los datos base estén presentes.

## Por qué nació este proyecto

Durante unas pruebas en una máquina virtual de laboratorio, generé una
contraseña a partir de mis propios datos de prueba (nombre + año de
nacimiento, con leetspeak y un separador) y comprobé que CUPP, pese a tener
toda la información necesaria, no era capaz de generarla porque sus listas de
sufijos/prefijos y su modo leet se calculan de forma independiente, sin
cruzarse entre sí. UCUPP nace para cubrir exactamente ese hueco: una
combinatoria real y configurable entre todas las variantes de los datos
introducidos.

## Ventajas frente a CUPP clásico

- **Combinación cruzada real**: cada palabra base (y su variante leet, en
  minúscula, con mayúscula inicial o en mayúsculas) se combina con cada
  fragmento de cada fecha introducida (día, mes, año, año corto, y
  combinaciones entre ellos), en ambos órdenes (`palabra+fecha` y
  `fecha+palabra`).
- **Separadores configurables**: prueba automáticamente sin separador, `_`,
  `-` y `.` entre palabra y número — el patrón `nombre_año` tan común en
  contraseñas reales.
- **Caracteres especiales al final**, igual que en CUPP, pero aplicados sobre
  las combinaciones ya cruzadas, no solo sobre las palabras sueltas.
- **Límite configurable** (`max_total`, 800.000 por defecto) para mantener el
  archivo en un tamaño manejable, evitando que la combinatoria se dispare sin
  control.
- **Cero dependencias externas**: solo usa la librería estándar de Python 3,
  así que no hace falta instalar nada con `pip`.
- **Compatible con las mismas herramientas** que usarías con un diccionario de
  CUPP: John the Ripper, Hashcat, Hydra, etc.

## Instalación

```bash
git clone https://github.com/TU_USUARIO/ucupp.git
cd ucupp
python3 ucupp.py
```

No requiere ninguna dependencia adicional (Python 3.6+ es suficiente).

## Uso

```bash
python3 ucupp.py
```

El script te preguntará, de forma interactiva:

- Nombre, apellido, nickname, mascota, hijo/a, pareja, empresa
- Palabras clave adicionales
- Fechas de nacimiento (formato `DDMMYYYY`) de la víctima, pareja e hijo/a
- Si quieres activar leetspeak
- Si quieres combinar las palabras con las fechas
- El límite máximo de combinaciones a generar
- El nombre del archivo de salida

Al terminar, obtendrás un archivo `.txt` con una contraseña candidata por
línea, listo para usar con cualquier herramienta de cracking:

```bash
john --wordlist=salida.txt hashes.txt
john --show hashes.txt

# o con Hashcat
hashcat -m 1800 -a 0 hashes.txt salida.txt

# o con Hydra, por ejemplo contra SSH
hydra -l usuario -P salida.txt ssh://IP_OBJETIVO
```

## Ejemplo

Puedes ver una ejecución de ejemplo completa en
[`examples/ejemplo_ejecucion.md`](examples/ejemplo_ejecucion.md).

## ⚠️ Uso responsable

Esta herramienta genera diccionarios de contraseñas a partir de datos
personales con el único fin de **auditar la robustez de contraseñas propias
o de sistemas para los que tengas autorización explícita** (máquinas
virtuales propias, laboratorios de formación, pentests contratados con
alcance definido por escrito).

- No uses UCUPP contra cuentas, sistemas o personas sin su consentimiento
  explícito y documentado.
- El uso no autorizado de herramientas de este tipo puede constituir un
  delito en la mayoría de jurisdicciones.
- Los autores no se hacen responsables del mal uso de esta herramienta.

## Licencia

Este proyecto se distribuye bajo licencia MIT. Consulta el archivo
[`LICENSE`](LICENSE) para más detalles.

## Créditos

Inspirado en [CUPP](https://github.com/Mebus/cupp), de Muris Kurgas y Mebus.
