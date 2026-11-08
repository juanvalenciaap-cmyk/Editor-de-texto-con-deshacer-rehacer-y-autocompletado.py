# Editor de texto con deshacer, rehacer y autocompletado

Editor de texto de escritorio construido con **Tkinter** para la asignatura de
Estructuras de Datos. Todas las estructuras de datos y algoritmos están
implementados desde cero (sin usar las colecciones de la librería estándar).

## Características

- Escribir, borrar, **deshacer** y **rehacer** cada operación (Ctrl+Z / Ctrl+Y)
- Búsqueda y reemplazo, individual y total
- **Autocompletado** de palabras con árbol de búsqueda binario + diccionario ordenado
- Negrita, cursiva y subrayado
- Abrir / guardar archivos `.txt` con historial de navegación (grafo de archivos)
- Números de línea, contador de palabras, caracteres y líneas
- Barra de estado con estadísticas, contadores de deshacer/rehacer y bitácora de operaciones

## Requisitos

- Python 3.10 o superior con `tkinter` (incluido en la instalación estándar de Windows)
- `pytest` para correr las pruebas: `pip install pytest`

## Ejecutar

```bash
python interfaz_grafica.py
```

## Pruebas

```bash
pytest                     # colecciona test_editor.py automáticamente
pytest test_editor.py -q   # ejecutar solo las pruebas
```

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `interfaz_grafica.py` | Interfaz gráfica (Tkinter) |
| `logica.py` | Lógica del editor: texto, cursor, undo/redo, búsqueda, archivos |
| `arreglo_dinamico.py` | Arreglo dinámico (redimensionado ×2) |
| `lista_doble.py` | Lista doblemente enlazada |
| `pila_cola_estatica.py` | Pila y cola estáticas + `Historial` de operaciones |
| `pila_dinamica.py`, `cola_dinamica.py` | Pila y cola dinámicas |
| `arbol.py` | Árbol de búsqueda binario (índice de palabras y sugerencias) |
| `insertion_sort.py`, `merge_sort.py`, `busqueda_binaria.py` | Algoritmos de orden y búsqueda |
| `carga_archivos.py` | Lectura/escritura de archivos (iterativa) |
| `carga_archivos_recur.py` | Lectura de archivos de forma recursiva |
| `carga_de_archivos_ulti.py` | Grafo de archivos + historial de navegación |
| `posicion_cursor.py` | Posición del cursor (fila/columna) |
| `test_editor.py` | Pruebas (pytest) |
| `INFORME COMPLEJIDAD.pdf` | Informe de complejidad algorítmica |

## Atajos de teclado

| Atajo | Acción |
|---|---|
| Ctrl+Z / Ctrl+Y | Deshacer / Rehacer |
| Ctrl+N / Ctrl+O / Ctrl+S | Nuevo / Abrir / Guardar |
| Ctrl+F | Buscar y reemplazar |
| Ctrl+B / Ctrl+I / Ctrl+U | Negrita / Cursiva / Subrayado |
| Tab | Aplicar sugerencia del autocompletado |

## Diccionario de sugerencias

El autocompletado sugiere palabras de dos fuentes: las palabras del documento
abierto (árbol de búsqueda) y el **diccionario de palabras sugeridas**.

Por defecto el editor arranca con 10 palabras base, pero se puede reemplazar
por uno propio desde el **menú Archivo**:

| Opción (menú Archivo) | Acción |
|---|---|
| 📖 Cargar diccionario... | Reemplaza el diccionario actual por las palabras de un `.txt` |
| ↺ Diccionario por defecto | Restaura las 10 palabras originales |

**Formato del archivo**: texto plano `.txt`, una palabra por línea (también se
aceptan varias palabras separadas por espacios en la misma línea). Las
mayúsculas se normalizan a minúsculas y las palabras repetidas se ignoran.
Si el archivo no contiene palabras válidas se conserva el diccionario actual.

**Edición**: el diccionario no se modifica desde el editor; para cambiarlo se
edita el `.txt` directamente (en el Bloc de notas u otro editor) y se vuelve a
cargar con 📖 Cargar diccionario....

**Auto-carga**: si existe un archivo llamado `diccionario.txt` junto a
`interfaz_grafica.py`, se carga automáticamente al arrancar el editor, quedando
en lugar del diccionario por defecto.

Nota: al abrir un documento, sus palabras también se agregan al diccionario
(de forma automática y durante la sesión).

## Limitaciones

- **El formato no se persiste**: negrita/cursiva/subrayado (N/K/S) viven solo en el
  widget de Tkinter. El guardado en `.txt` es texto plano (no puede guardar formato)
  y el formato **no se conserva** al deshacer/rehacer, porque esos pasos restauran
  el texto completo.
- **Carga recursiva**: `carga_archivos_recur.py` falla con archivos de ~1 000 líneas
  o más, por el límite de recursión de Python (`RecursionError`). Para documentos
  grandes se usa la carga iterativa.
- **Memoria del deshacer**: cada paso guarda un snapshot completo del documento
  (O(n) por paso). Con documentos muy grandes y muchas ediciones, el consumo de
  memoria crece proporcionalmente.
- **Reemplazar todo distingue mayúsculas**: la búsqueda (Ctrl+F) no distingue
  mayúsculas, pero *Reemplazar todo* aplica el texto exacto escrito.
- **Bitácora**: es un registro visible de las operaciones (una por paso de
  deshacer), no es el mecanismo de deshacer; el deshacer real usa
  `pila_undo`/`pila_redo`.
