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
