from arreglo_dinamico import ArregloDinamico
from busqueda_binaria import busqueda_binaria
from carga_archivos import CargaArchivos
from cola_dinamica import ColaDinamica
from lista_doble import (lista_doble,Nodo)
from merge_sort import merge_sort
from pila_cola_estatica import (Historial,ColaEstatica,PilaEstatica,opeeracion,EstructuraVaciaError,BORRAR,INSERTAR)
from pila_dinamica import PilaDinamica
from posicion_cursor import PosicionCursor
from insertion_sort import insertion_sort
from carga_de_archivos_ulti import GestorArchivosGrafo
from carga_archivos_recur import CargaArchivos as CargaArchivosRecur 
from arbol import ArbolBusqueda

class Logica:
    def __init__(self,capacidad_historial=200):
        self.historial = Historial(capacidad = capacidad_historial)
        self.cursor = PosicionCursor(fila=0,columna=0)
        self.lineas = ArregloDinamico()
        self.lineas.agregar("")
        self.cola_estatica = ColaEstatica(capacidad=100)
        self.ruta_actual = None
        self.diccionario = ArregloDinamico()
        self._inicializar_diccionario_base()
        self.lineas_lista_doble = lista_doble()
        self.lineas_lista_doble.agregar_final("")
        self.pila_undo=PilaDinamica()
        self.pila_redo=PilaDinamica()
        self.pila_dinamica=PilaDinamica()
        self.cola_resultados_busqueda=ColaDinamica()
        self.arbol =ArbolBusqueda()
        self.gestor_archivos= GestorArchivosGrafo()

    def obtener_texto(self):
        lineas=[]
        for i in range (len(self.lineas)):
            lineas.append(self.lineas.obtener(i))
        return "\n".join(lineas)
    def cargar_texto(self,texto_completo):
        lista_lineas=texto_completo.split("\n")
        nuevo_arreglo=ArregloDinamico(max(1,len(lista_lineas)))
        nueva_lista_doble=lista_doble()
        for linea in lista_lineas:
            nuevo_arreglo.agregar(linea)
            nueva_lista_doble.agregar_final(linea)
        self.lineas=nuevo_arreglo
        self.lineas_lista_doble=nueva_lista_doble
    def total_lineas(self):
        return len(self.lineas)
    def total_caracteres(self):
        return len (self.obtener_texto())
    def nuevo_documento(self):
        self.lineas =ArregloDinamico()
        self.lineas.agregar("")
        self.lineas_lista_doble=lista_doble()
        self.lineas_lista_doble.agregar_final("")
        self.cursor=PosicionCursor(0,0)
        self.historial=Historial(capacidad=100)
        self.arbol=ArbolBusqueda()
        self.ruta_actual = None
        while not self.pila_undo.esta_vacia():
            self.pila_undo.desapilar()
        while not self.pila_redo.esta_vacia():
            self.pila_redo.desapilar()
        while not self.cola_resultados_busqueda.esta_vacia():
            self.cola_resultados_busqueda.desencolar()


    def mover_cursor(self,direccion):
        if direccion == "izquierda":
            if self.cursor._columna>0:
                self.cursor.mover_izquierda()
            elif self.cursor._fila>0:
                self.cursor.mover_arriba()
                self.cursor._columna= len(self.lineas.obtener(self.cursor._fila))
        elif direccion == "derecha":
            longitud_linea=len(self.lineas.obtener(self.cursor._fila))
            if self.cursor._columna<longitud_linea:
                self.cursor.mover_derecha()
            elif self.cursor._fila<len(self.lineas)-1:
                self.cursor.mover_abajo()
                self.cursor._columna=0

        elif direccion == "arriba":
            if self.cursor._fila>0:
                self.cursor.mover_arriba()
                max_col=len(self.lineas.obtener(self.cursor._fila))
                if self.cursor._columna>max_col:
                    self.cursor._columna=max_col
        elif direccion == "abajo":
            if self.cursor._fila<len(self.lineas)-1:
                self.cursor.mover_abajo()
                max_col=len(self.lineas.obtener(self.cursor._fila))
                if self.cursor._columna>max_col:
                    self.cursor._columna=max_col
    def set_cursor(self,fila,columna):
        self.cursor=PosicionCursor(max(0,fila),max(0,columna))
    def registrar_accion(self,tipo,posicion,texto):
        op=opeeracion(tipo=tipo,posicion=posicion,texto=texto)
        self.historial.registrar(op)
        if not self.cola_estatica.esta_llena():
            self.cola_estatica.enqueue(f"{tipo}:{texto[:20]}")
    def guardar_snapshot(self):
        texto = self.obtener_texto()
        if not self.pila_undo.esta_vacia() and self.pila_undo.ver_tope()==texto:
            return
        self.pila_undo.apilar(texto)
        while not self.pila_redo.esta_vacia():
            self.pila_redo.desapilar()


    def deshacer(self):
        if self.pila_undo.esta_vacia():
            return None
        texto_actual=self.obtener_texto()
        self.pila_redo.apilar(texto_actual)
        texto_anterior=self.pila_undo.desapilar()
        self.cargar_texto(texto_anterior)
        return texto_anterior
    def rehacer(self):
        if self.pila_redo.esta_vacia():
            return None
        texto_actual = self.obtener_texto()
        self.pila_undo.apilar(texto_actual)
        texto_siguiente=self.pila_redo.desapilar
        self.cargar_texto(texto_siguiente)
        return texto_siguiente
    def puede_deshacer (self):
        return not self.pila_undo.esta_vacia()
    def puede_rehacer(self):
        return not self.pila_redo.esta_vacia()
    
    def _cargar_palabras_por_defecto(self):
        palabras = ["realizar","arbol","python","lenguaje","interfaz","hola","libreria","estructura","datos","listas"]
        for p in palabras:
            self.diccionario.agregar(p)
        merge_sort(self.diccionario)
    def agregar_palabra_al_diccionario(self,palabra):
        palabra=palabra.strip().lower()
        if len(palabra)<3:
            return
        indice = busqueda_binaria(self.diccionario,palabra)
        if indice == -1:
            self.diccionario.agregar(palabra)
            if len(self.diccionario)<40:
                insertion_sort(self.diccionario)
            else: 
                merge_sort(self.diccionario)
    def sugerir_palabras(self,prefijo,limite=5):
        prefijo=prefijo.strip().lower()
        if not prefijo :
            return[]
        sugerencias = []
        resultado_arbol=self.arbol.buscar_prefijos(prefijo)
        for i in range (len(resultado_arbol)):
            palabra, _ = resultado_arbol.obtener(i)
            if palabra not in sugerencias : 
                sugerencias.append(palabra)
                if len(sugerencias)>=limite:
                    return sugerencias
                
        for i in range (len(self.diccionario)):
            palabra = self.diccionario.obtener(i)
            if palabra.startswith(prefijo) and palabra not in sugerencias:
                sugerencias.append(palabra)
                if len (sugerencias)>=limite:
                    break
        return sugerencias
    def _reconstruir_arbol(self):
        self.arbol=ArbolBusqueda()
        lineas_lista=[]
        for i in range (len(self.lineas)):
            lineas_lista.append(self.lineas.obtener(i))
        self.arbol.indexar_texto(lineas_lista)
    def abrir_archivo(self,ruta,usar_recursivo=False):
        nodo = self.gestor_archivos.abrir_o_enfocar_archivo(ruta)
        self.lineas = nodo.lineas
        self.ruta_actual = ruta
        if usar_recursivo:
            self.lineas=CargaArchivosRecur.cargar_documento_recursivo(ruta)
            nodo.lineas = self.lineas 
        self.lineas_lista_doble = lista_doble ()   
        for i in range (len(self.lineas)):
            self.lineas_lista_doble.agregar_final(self.lineas.obtener(i))
        self.cursor = PosicionCursor(0,0)
        self.historial = Historial(capacidad=100)
        while not self.pila_undo.esta_vacia():
            self.pila_undo.desapilar()
        while not self.pila_redo.esta_vacia():
            self.pila_redo.desapilar()
        self._reconstruir_arbol()
        texto = self.obtener_texto()
        for palabra in texto.split():
            self.agregar_palabra_al_diccionario(palabra)
        return nodo
    def guardar_archivo(self,ruta=None):
        destino = ruta or self.ruta_actual
        if not destino : 
            raise ValueError("no hay una ruta definida para guardar")
        CargaArchivos.guardar_documento(destino,self.lineas)
        self.ruta_actual = destino
    def archivo_anterior (self):
        nodo = self.gestor_archivos.navegar_atras()
        if nodo :
            self.lineas = nodo.lineas
            self.ruta_actual = nodo.ruta_actual
            self._reconstruir_arbol()
        return nodo 
    def archivo_siguiente (self):
        nodo = self.gestor_archivos.navegar_adelante()
        if nodo :
            self.lineas = nodo.lineas
            self.ruta_actual = nodo.ruta_actual
            self._reconstruir_arbol()
        return nodo 
    def buscar_texto (self,palabra_buscar):
        if not palabra_buscar:
        
            return[]
        coincidencias = []
        lineas_candidatas = self.arbol.buscar(palabra_buscar.lower())
        if lineas_candidatas is not None :
            for i in range (len(lineas_candidatas)):
                num_linea = lineas_candidatas.obtener(i) -1
                if 0<=num_linea <len (self.lineas):
                    linea=self.lineas.obtener(num_linea)
                    col=linea.find(palabra_buscar)
                    while col != -1 :
                        coincidencias.append((num_linea,col))
                        col = linea.find (palabra_buscar,col+len(palabra_buscar))
        else :
            for i in range (len(self.lineas)):
                linea = self.lineas.obtener(i)
                col = linea.find(palabra_buscar)
                while col != -1 :
                    coincidencias.append((i,col))
                    col = linea.find(palabra_buscar,col+len(palabra_buscar))
        while not self.cola_resultados_busqueda.esta_vacia():
            self.cola_resultados_busqueda.desencolar()
        for c in coincidencias:
            self.cola_resultados_busqueda.encolar(c)
        return coincidencias
    def siguiente_coincidencia(self):
        if self.cola_resultados_busqueda.esta_vacia():
            return None
        coincidencia = self.cola_resultados_busqueda.desencolar()
        self.cola_resultados_busqueda.encolar(coincidencia)
        return coincidencia
    def reemplazar_todo (self,buscar,reemplazar):
        if not buscar :
            return 0
        texto_original = self.obtener_texto()
        conteo= texto_original.count(buscar)
        if conteo>0 : 
            self.guardar_snapshot()
            self.registrar_accion(BORRAR,0,texto_original)
            nuevo_texto = texto_original.replace(buscar,reemplazar)
            self.cargar_texto(nuevo_texto)
            self.registrar_accion(INSERTAR,0,nuevo_texto)
            self._reconstruir_arbol
        return conteo 