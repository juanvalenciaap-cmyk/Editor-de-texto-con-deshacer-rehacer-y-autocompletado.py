import random
import string 
import pytest
from arreglo_dinamico import ArregloDinamico
from posicion_cursor import PosicionCursor
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from busqueda_binaria import busqueda_binaria
from carga_archivos import CargaArchivos
from cola_dinamica import ColaDinamica
from lista_doble import lista_doble
from pila_dinamica import PilaDinamica
from pila_cola_estatica import (
    PilaEstatica, ColaEstatica, Historial, opeeracion,
    INSERTAR, BORRAR, EstructuraLlenaError, EstructuraVaciaError
)
from carga_archivos_recur import CargaArchivos as CargaArchivosRecur
from logica import Logica

def construir(valores):
    "simular documento"
    a=ArregloDinamico(capacidad_inicial=max(1,len(valores)))
    for v in valores:
        a.agregar(v)
    return a
def a_lista(arreglo):
    return[arreglo.obtener(i)for i in range(len(arreglo))]
def test_documento_no_puede_crearse_con_capacidad_invalidad():
    with pytest.raises(ValueError):
        ArregloDinamico(0)
def test_obtener_linea_fuera_de_rango():
    doc=construir(["primera linea", "segunda linea","tercera linea"])
    with pytest.raises(IndexError):
        doc.obtener(3)
def test_eliminar_unica_linea_documento_vacio():
    doc=construir(["unica linea"])
    doc.eliminar(0)
    assert doc.esta_vacio()
def test_insertar_linea_nueva():
    doc=ArregloDinamico(capacidad_inicial=2)
    doc.agregar("linea1")
    doc.agregar("linea2")
    doc.insertar(1,"lineanueva")
    assert a_lista(doc)==["linea1","lineanueva","linea2"]
def test_cursor_no_nace_fila_negativa():
    with pytest.raises(ValueError):
        PosicionCursor(fila=-1)
def test_cursor_no_retrocede_inicio_linea():
    cursor=PosicionCursor(columna=0)
    cursor.mover_izquierda()
    assert cursor._columna==0
def test_cursor_no_sube_primera_linea():
    cursor=PosicionCursor(fila=0)
    cursor.mover_arriba()
    assert cursor._fila==0
def test_cursor_se_mueve_dentro_linea():
    linea="hola clase"
    cursor=PosicionCursor(fila=0,columna=0)
    for i in range(len(linea)):
        cursor.mover_derecha()
        assert cursor._columna==i+1
def test_sort_documento_vacio():
    doc=construir([])
    insertion_sort(doc)
    assert a_lista(doc)==[]
def test_sort_ordena_alfabeticamente():
    doc=construir(["susana","mariana","agni","sofia"])
    insertion_sort(doc)
    assert a_lista(doc)==["agni","mariana","sofia","susana"]
def test_merge_docuemento_vacio():
    doc=construir([])
    merge_sort(doc)
    assert a_lista(doc) == []
def test_merge_ordena_alfabeticamente():
    doc=construir(["susana","mariana","agni","sofia"])
    merge_sort(doc)
    assert a_lista(doc)==["agni","mariana","sofia","susana"]
def test_busqueda_binaria_documento_vacio():
    doc=construir([])
    assert busqueda_binaria(doc,"hola")==-1
def test_busqueda_binaria_no_existe():
    doc=construir(["agni","mariana","susana","sofia"])
    assert busqueda_binaria(doc, "samuel")==-1
def test_bisqueda_binaria_primera_ultima_linea():
    # la busqueda binaria exige datos ordenados
    doc=construir(["agni","mariana","sofia","susana"])
    assert busqueda_binaria(doc, "agni")==0
    assert busqueda_binaria(doc,"susana")==3
def test_cargar_documentos_no_existe(tmp_path):
    ruta=tmp_path/"no _existe.txt"
    with pytest.raises(FileNotFoundError):
        CargaArchivos.cargar_documento(str(ruta))
def test_cargar_documentos_vacio_con_linea(tmp_path):
    ruta=tmp_path/"vacio.txt"
    ruta.write_text("",encoding="utf-8")
    doc=CargaArchivos.cargar_documento(str(ruta))
    assert a_lista(doc)==[""]
def test_guardar_cargar_lineas(tmp_path):
    ruta=tmp_path/"documentos.txt"
    doc = construir(["primera linea","segunda linea"])
    CargaArchivos.guardar_documento(str(ruta),doc)
    recargado=CargaArchivos.cargar_documento(str(ruta))
    assert a_lista(recargado)==a_lista(doc)
def _linea_aleatoria():
    largo=random.randint(1,20)
    return "".join(random.choices(string.ascii_lowercase,k=largo))
def test_docuemento_mil_lineas():
    random.seed(1)
    lineas=[_linea_aleatoria() for _ in range(1000)]
    doc = construir(lineas)
    insertion_sort(doc)
    assert a_lista(doc)==sorted(lineas)
def test_merge_mil_lineas():
    random.seed(2)
    lineas=[_linea_aleatoria() for _ in range(1000)]
    doc=construir(lineas)
    merge_sort(doc)
    assert a_lista(doc)==sorted(lineas)


 #pruebas entrega 2 :yose
# PRUEBAS DE HISTORIAL Y DESHACER / REHACER
def test_historial_flujo_deshacer_y_rehacer():
    h = Historial(capacidad=5)
    op = opeeracion(tipo=INSERTAR, posicion=0, texto="hola")
    h.registrar(op)
    
    assert h.puede_deshacer()
    assert not h.puede_rehacer()
    
    # Deshacer debe entregar la operación inversa (BORRAR)
    deshecha = h.deshacer()
    assert deshecha.tipo == BORRAR
    assert deshecha.texto == "hola"
    assert not h.puede_deshacer()
    assert h.puede_rehacer()
    
    # Rehacer debe entregar la operación original (INSERTAR)
    rehecha = h.rehacer()
    assert rehecha.tipo == INSERTAR
    assert rehecha.texto == "hola"
    assert h.puede_deshacer()
    assert not h.puede_rehacer()

def test_historial_deshacer_borrado():
    h = Historial(capacidad=5)
    op = opeeracion(tipo=BORRAR, posicion=2, texto="chau")
    h.registrar(op)
    deshecha = h.deshacer()
    assert deshecha.tipo == INSERTAR
    assert deshecha.texto == "chau"

def test_historial_nueva_operacion_limpia_rehacer():
    h = Historial(capacidad=5)
    h.registrar(opeeracion(INSERTAR, 0, "A"))
    h.deshacer()
    assert h.puede_rehacer()
    # Una nueva acción debe invalidar rehacer
    h.registrar(opeeracion(INSERTAR, 1, "B"))
    assert not h.puede_rehacer()

def test_historial_deshacer_vacio_lanza_error():
    h = Historial(capacidad=5)
    with pytest.raises(EstructuraVaciaError):
        h.deshacer()


# PRUEBAS DE PILA Y COLA ESTÁTICA
def test_pila_estatica_capacidad_y_errores():
    with pytest.raises(ValueError):
        PilaEstatica(capacidad=0)
    
    pila = PilaEstatica(capacidad=2)
    pila.push("A")
    pila.push("B")
    assert pila.esta_llena()
    with pytest.raises(EstructuraLlenaError):
        pila.push("C")
    
    assert pila.peek() == "B"
    assert pila.pop() == "B"
    assert pila.pop() == "A"
    assert pila.esta_vacia()
    with pytest.raises(EstructuraVaciaError):
        pila.pop()

def test_cola_estatica_fifo_y_rotacion():
    with pytest.raises(ValueError):
        ColaEstatica(capacidad=0)
        
    cola = ColaEstatica(capacidad=3)
    cola.enqueue("1")
    cola.enqueue("2")
    assert len(cola) == 2
    assert cola.dequeue() == "1"
    cola.enqueue("3")
    cola.enqueue("4")
    assert cola.esta_llena()
    with pytest.raises(EstructuraLlenaError):
        cola.enqueue("5")
    
    assert cola.peek() == "2"
    assert cola.dequeue() == "2"
    assert cola.dequeue() == "3"
    assert cola.dequeue() == "4"
    assert cola.esta_vacia()
    with pytest.raises(EstructuraVaciaError):
        cola.dequeue()

# PRUEBAS DE PILA Y COLA DINÁMICA
def test_pila_dinamica_lifo():
    pila = PilaDinamica()
    assert pila.esta_vacia()
    pila.apilar("x")
    pila.apilar("y")
    assert pila.tamano() == 2
    assert pila.ver_tope() == "y"
    assert pila.desapilar() == "y"
    assert pila.desapilar() == "x"
    with pytest.raises(IndexError):
        pila.desapilar()

def test_cola_dinamica_fifo():
    cola = ColaDinamica()
    assert cola.esta_vacia()
    cola.encolar("primero")
    cola.encolar("segundo")
    assert cola.tamano() == 2
    assert cola.ver_frente() == "primero"
    assert cola.desencolar() == "primero"
    assert cola.desencolar() == "segundo"
    with pytest.raises(IndexError):
        cola.desencolar()

# PRUEBAS DE LISTA DOBLE
def test_lista_doble_insercion_y_extraccion():
    ld = lista_doble()
    assert ld.esta_vacio()
    ld.agregar_final("B")
    ld.insertar(0, "A")       # inicio
    ld.insertar(2, "D")       # fin
    ld.insertar(2, "C")       # en medio
    assert ld.a_lista() == ["A", "B", "C", "D"]
    assert len(ld) == 4
    assert ld.obtener(1) == "B"
    assert ld[2] == "C"

def test_lista_doble_eliminacion_extremos_y_medio():
    ld = lista_doble()
    for item in ["A", "B", "C", "D"]:
        ld.agregar_final(item)
    
    # eliminar en medio
    assert ld.eliminar(1) == "B"
    assert ld.a_lista() == ["A", "C", "D"]
    # eliminar cabeza
    assert ld.eliminar(0) == "A"
    assert ld.a_lista() == ["C", "D"]
    # eliminar cola
    assert ld.eliminar(1) == "D"
    assert ld.a_lista() == ["C"]
    # eliminar último elemento restante
    assert ld.eliminar(0) == "C"
    assert ld.esta_vacio()

def test_lista_doble_indices_fuera_de_rango():
    ld = lista_doble()
    with pytest.raises(IndexError):
        ld.eliminar(0)
    with pytest.raises(IndexError):
        ld.obtener(0)
    with pytest.raises(IndexError):
        ld.insertar(5, "err")

# PRUEBAS DE CARGA DE ARCHIVOS RECURSIVA
def test_carga_archivos_recur_no_existe(tmp_path):
    ruta = tmp_path / "no_existe_recur.txt"
    with pytest.raises(FileNotFoundError):
        CargaArchivosRecur.cargar_documento_recursivo(str(ruta))

def test_carga_archivos_recur_lectura(tmp_path):
    ruta = tmp_path / "prueba_recur.txt"
    ruta.write_text("linea 1\nlinea 2\nlinea 3", encoding="utf-8")
    doc = CargaArchivosRecur.cargar_documento_recursivo(str(ruta))
    assert a_lista(doc) == ["linea 1", "linea 2", "linea 3"]


# PRUEBAS DE LA LOGICA DEL EDITOR (deshacer/rehacer/guardado)
def test_logica_se_puede_instanciar():
    # regresión: __init__ llamaba a un método inexistente y la app no arrancaba
    logica = Logica()
    assert logica.total_lineas() == 1
    assert logica.obtener_texto() == ""
    assert len(logica.diccionario) > 0


def test_deshacer_rehacer_por_operacion():
    logica = Logica()
    snap = ""
    # simula _on_tecla_liberada: aplica el cambio y registra el estado previo
    for texto in ["h", "ho", "hol", "hola"]:
        logica.cargar_texto(texto)
        logica.guardar_snapshot(snap)
        snap = texto

    assert logica.puede_deshacer()
    assert logica.deshacer() == "hol"
    assert logica.deshacer() == "ho"
    assert logica.rehacer() == "hol"
    assert logica.rehacer() == "hola"


def test_deshacer_llega_al_documento_original():
    logica = Logica()
    snap = ""
    for texto in ["uno", "uno ", "uno dos"]:
        logica.cargar_texto(texto)
        logica.guardar_snapshot(snap)
        snap = texto

    assert logica.deshacer() == "uno "
    assert logica.deshacer() == "uno"
    assert logica.deshacer() == ""      # vuelve al documento vacío original
    assert logica.deshacer() is None    # no hay más estados
    assert not logica.puede_deshacer()


def test_nueva_edicion_invalida_rehacer():
    logica = Logica()
    logica.cargar_texto("a")
    logica.guardar_snapshot("")
    logica.deshacer()
    assert logica.puede_rehacer()

    logica.cargar_texto("b")
    logica.guardar_snapshot("")
    assert not logica.puede_rehacer()


def test_guardar_snapshot_sin_argumento_usa_texto_actual():
    logica = Logica()
    logica.cargar_texto("original")
    logica.guardar_snapshot()
    logica.cargar_texto("modificado")
    assert logica.deshacer() == "original"


def test_reemplazar_todo_es_deshacible():
    logica = Logica()
    logica.cargar_texto("hola hola hola")
    assert logica.reemplazar_todo("hola", "adios") == 3
    assert logica.obtener_texto() == "adios adios adios"
    assert logica.deshacer() == "hola hola hola"


def test_historial_registrar_con_pila_llena_no_crash():
    # antes: EstructuraLlenaError a la 4ta operación con capacidad 3
    h = Historial(capacidad=3)
    for i in range(6):
        h.registrar(opeeracion(INSERTAR, i, "x"))
    assert h.puede_deshacer()


def test_guardar_archivo_registra_ruta_actual(tmp_path):
    # regresión: la GUI consultaba logica.ruta_archivo (inexistente)
    ruta = str(tmp_path / "salida.txt")
    logica = Logica()
    logica.cargar_texto("linea1\nlinea2")
    logica.guardar_archivo(ruta)
    assert logica.ruta_actual == ruta
    recargado = CargaArchivos.cargar_documento(ruta)
    assert a_lista(recargado) == ["linea1", "linea2"]


def test_sugerir_palabras_con_indice_de_texto():
    logica = Logica()
    logica.cargar_texto("python es un lenguaje")
    logica._reconstruir_arbol()
    assert "python" in logica.sugerir_palabras("py")


def test_busqueda_no_distingue_mayusculas():
    logica = Logica()
    logica.cargar_texto("Python es bueno\npython es malo\nPYTHON al reves")
    logica._reconstruir_arbol()

    encontradas = logica.buscar_texto("Python")
    # las tres lineas aparecen, en la columna real de la coincidencia
    assert encontradas == [(0, 0), (1, 0), (2, 0)]
    # escribirlo en minusculas devuelve exactamente lo mismo
    assert logica.buscar_texto("python") == encontradas
    assert logica.buscar_texto("PYTHON") == encontradas


def test_busqueda_con_caracteres_que_cambian_longitud():
    # 'İ'.lower() tiene 2 caracteres: no se pueden mapear posiciones,
    # asi que se cae a la busqueda sensible sin desalinear el resaltado
    logica = Logica()
    logica.cargar_texto("İstanbul es grande")
    logica._reconstruir_arbol()
    assert logica.buscar_texto("İstanbul") == [(0, 0)]


def test_guardar_snapshot_registra_en_bitacora():
    # la bitacora queda en cero al crear la instancia
    logica = Logica()
    assert logica.total_acciones() == 0
    assert logica.ultima_operacion() == ""

    # cada guardar_snapshot con texto_previo = un paso de deshacer = una entrada
    snap = ""
    for texto in ["h", "ho", "hol"]:
        logica.cargar_texto(texto)
        logica.guardar_snapshot(snap)
        snap = texto

    assert logica.total_acciones() == 3
    # numero, tipo y el trozo de texto registrado (no el texto completo)
    assert logica.ultima_operacion() == '#3 INSERTAR "l"'

    # un borrado se registra como BORRAR
    logica.cargar_texto("ho")
    logica.guardar_snapshot("hol")
    assert logica.ultima_operacion() == '#4 BORRAR "l"'


def test_bitacora_no_altera_el_deshacer():
    # el registro de la bitacora no cambia el comportamiento de pila_undo/pila_redo
    logica = Logica()
    snap = ""
    for texto in ["a", "ab", "abc"]:
        logica.cargar_texto(texto)
        logica.guardar_snapshot(snap)
        snap = texto

    assert logica.total_acciones() == 3
    assert logica.deshacer() == "ab"
    assert logica.deshacer() == "a"
    assert logica.rehacer() == "ab"
    assert logica.rehacer() == "abc"
    # deshacer/rehacer no son ediciones: no suman entradas nuevas
    assert logica.total_acciones() == 3

    # nuevo documento reinicia la bitacora
    logica.nuevo_documento()
    assert logica.total_acciones() == 0
    assert logica.ultima_operacion() == ""


def test_set_cursor_y_mover_cursor_desde_la_logica():
    # la interfaz sincroniza la posicion con set_cursor y delega el movimiento
    logica = Logica()
    logica.cargar_texto("hola\nmundo")

    logica.set_cursor(0, 4)              # final de la primera linea
    assert (logica.cursor._fila, logica.cursor._columna) == (0, 4)

    logica.mover_cursor("derecha")       # pasa al inicio de la linea siguiente
    assert (logica.cursor._fila, logica.cursor._columna) == (1, 0)

    logica.mover_cursor("abajo")         # ya esta en la ultima linea: no se mueve
    assert (logica.cursor._fila, logica.cursor._columna) == (1, 0)

    logica.mover_cursor("arriba")
    assert (logica.cursor._fila, logica.cursor._columna) == (0, 0)

    logica.mover_cursor("arriba")        # primera linea: no se mueve
    assert (logica.cursor._fila, logica.cursor._columna) == (0, 0)

    logica.mover_cursor("derecha")
    logica.mover_cursor("derecha")
    logica.mover_cursor("derecha")
    logica.mover_cursor("derecha")
    assert (logica.cursor._fila, logica.cursor._columna) == (0, 4)
    logica.mover_cursor("derecha")       # no pasa del largo de la linea
    assert (logica.cursor._fila, logica.cursor._columna) == (1, 0)


def test_set_cursor_no_acepta_valores_negativos():
    # indices invalidos (por ejemplo un widget sin texto) se recortan a 0
    logica = Logica()
    logica.set_cursor(-1, -5)
    assert (logica.cursor._fila, logica.cursor._columna) == (0, 0)


# PRUEBAS DEL DICCIONARIO DE PALABRAS SUGERIDAS
def test_cargar_diccionario_desde_archivo(tmp_path):
    ruta = tmp_path / "diccionario.txt"
    # mayusculas, repetidas, palabras en la misma linea y lineas vacias
    ruta.write_text("Algoritmos\narbol\nALGORITMOS\n\n  Datos  \nlista por nodo\n",
                    encoding="utf-8")
    logica = Logica()
    cantidad = logica.cargar_diccionario(str(ruta))

    # algoritmos, arbol, datos, lista, por, nodo
    assert cantidad == 6
    assert logica.sugerir_palabras("alg") == ["algoritmos"]
    assert logica.sugerir_palabras("ar") == ["arbol"]
    # el archivo viene desordenado: el diccionario resultante queda ordenado
    assert logica.sugerir_palabras("l") == ["lista"]
    assert logica.sugerir_palabras("no") == ["nodo"]


def test_cargar_diccionario_reemplaza_el_por_defecto(tmp_path):
    ruta = tmp_path / "diccionario.txt"
    ruta.write_text("ejemplo\nzzeta\n", encoding="utf-8")
    logica = Logica()
    assert logica.sugerir_palabras("py") == ["python"]   # por defecto

    logica.cargar_diccionario(str(ruta))
    assert logica.sugerir_palabras("py") == []           # ya no esta
    assert logica.sugerir_palabras("ej") == ["ejemplo"]


def test_cargar_diccionario_archivo_vacio_no_borra_el_actual(tmp_path):
    ruta = tmp_path / "vacio.txt"
    ruta.write_text("   \n\n\n", encoding="utf-8")
    logica = Logica()

    cantidad = logica.cargar_diccionario(str(ruta))
    assert cantidad == 0
    # el diccionario por defecto se conserva
    assert logica.sugerir_palabras("py") == ["python"]


def test_restaurar_diccionario_por_defecto(tmp_path):
    ruta = tmp_path / "personal.txt"
    ruta.write_text("zzeta\n", encoding="utf-8")
    logica = Logica()
    logica.cargar_diccionario(str(ruta))
    assert logica.sugerir_palabras("py") == []

    cantidad = logica.restaurar_diccionario_por_defecto()
    assert cantidad == 10
    assert logica.sugerir_palabras("py") == ["python"]
    assert logica.sugerir_palabras("zz") == []

   


