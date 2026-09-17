import random
import string 
import pytest
from arreglo_dinamico import ArregloDinamico
from posicion_cursor import PosicionCursor
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from busqueda_binaria import busqueda_binaria
from carga_archivos import CargaArchivos
def construir(valores):
    "simular doccumento"
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
    with pytest.raises(valueError):
        PosicionCursor(fila=-1)
def test_cursor_no_retrocede_inicio_linea():
    cursor=PosicionCursor(columna=0)
    cursor.mover_izquierda()
    assert cursor.columna==0
def test_cursor_no_sube_primera_linea():
    cursor=PosicionCursor(fila=0)
    cursor.mover_arriba()
    assert cursor._fila==0
def test_cursor_se_mueve_dentro_linea():
    linea="hola clase"
    cursor=PosicionCursor(fila=0,columna=0)
    for _ in range(len(linea)):
        cursor.mover_derecha()
        assert cursor._columna==len(linea)
def test_sort_documento_vacio():
    doc=construir([])
    insertion_sort(doc)
    assert a_lista(doc)==[]
def test_sort_ordena_alfabeticamente():
    doc=construir(["susana","mariana","agni","sofia"])
    insertion_sort(doc)
    assert a_lista(doc)==["agni","mariana","susana","sofia"]
def test_merge_docuemento_vacio():
    doc=construir([])
    merge_sort(doc)
    assert a_lista(doc) == []
def test_merge_ordena_alfabeticamente():
    doc=construir(["susana","mariana","agni","sofia"])
    merge_sort(doc)
    assert a_lista(doc)==["agni","mariana","susana","sofia"]
def test_busqueda_binaria_documento_vacio():
    doc=construir([])
    assert busqueda_binaria(doc,"hola")==-1
def test_busqueda_binaria_no_existe():
    doc=construir(["agni","mariana","susana","sofia"])
    assert busqueda_binaria(doc, "samuel")==-1
def test_bisqueda_binaria_primera_ultima_linea():
    doc=construir(["agni","mariana","susana","sofia"])
    assert busqueda_binaria(doc, "agni")==0
    assert busqueda_binaria(doc,"sofia")==3
def test_cargar_documentos_no_existe(tmp_path):
    ruta=tmp_path/"no _existe.txt"
    with pytest.raises(FileNotFoundError):
        CargaArchivos.cargar_documento(str(ruta))
def test_cargar_documentos_vacio_con_linea(tmp_path):
    ruta=tmp_path/"vacio.txt"
    ruta.write_text("",encoding="utf-8")
    doc=CargaArchivos.cargar_documentos(str(ruta))
    assert a_lista(doc)==[""]
def test_guardar_cargar_lineas(tmp_path):
    ruta=tmp_path/"documentos.txt"
    doc = construir(["primera linea","segunda linea"])
    CargaArchivos.guardar_documentos(str(ruta),doc)
    recargado=CargaArchivos.cargar_doccumento(str(ruta))
    assert a_lista(recargado)==a_lista(doc)
def _linea_aleatoria():
    largo=random.randint(1,20)
    return "".join(random.choices(string.ascoo_lowercase,k=largo))
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