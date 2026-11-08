from arreglo_dinamico import ArregloDinamico
from busqueda_binaria import busqueda_binaria
from carga_archivos import CargaArchivos
from cola_dinamica import ColaDinamica
from merge_sort import merge_sort
from pila_cola_estatica import (Historial,ColaEstatica,opeeracion,BORRAR,INSERTAR)
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
        self._cargar_palabras_por_defecto()
        self.pila_undo=PilaDinamica()
        self.pila_redo=PilaDinamica()
        self.cola_resultados_busqueda=ColaDinamica()
        self.arbol =ArbolBusqueda()
        self.gestor_archivos= GestorArchivosGrafo()
        self._total_acciones = 0
        self._ultima_accion = None

    def obtener_texto(self):
        lineas=[]
        for i in range (len(self.lineas)):
            lineas.append(self.lineas.obtener(i))
        return "\n".join(lineas)
    def cargar_texto(self,texto_completo):
        lista_lineas=texto_completo.split("\n")
        nuevo_arreglo=ArregloDinamico(max(1,len(lista_lineas)))
        for linea in lista_lineas:
            nuevo_arreglo.agregar(linea)
        self.lineas=nuevo_arreglo
    def total_lineas(self):
        return len(self.lineas)
    def total_caracteres(self):
        return len (self.obtener_texto())
    def nuevo_documento(self):
        self.lineas =ArregloDinamico()
        self.lineas.agregar("")
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
        self._total_acciones = 0
        self._ultima_accion = None


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
        self._total_acciones += 1
        self._ultima_accion = (tipo, posicion, texto)
    def total_acciones(self):
        return self._total_acciones
    def ultima_operacion(self):
        # numero, tipo y texto de la ultima edicion registrada
        if self._ultima_accion is None:
            return ""
        tipo, _, texto = self._ultima_accion
        resumen = texto if len(texto) <= 20 else texto[:17] + "..."
        return f'#{self._total_acciones} {tipo} "{resumen}"'
    def _detectar_cambio(self, previo, actual):
        # localiza que trozo se inserto y que trozo se elimino entre dos estados
        i = 0
        limite = min(len(previo), len(actual))
        while i < limite and previo[i] == actual[i]:
            i += 1
        j = 0
        while (j < len(previo) - i and j < len(actual) - i
               and previo[len(previo) - 1 - j] == actual[len(actual) - 1 - j]):
            j += 1
        fila = previo[:i].count("\n") + 1
        return previo[i:len(previo) - j], actual[i:len(actual) - j], fila
    def _registrar_cambio(self, texto_previo):
        texto_actual = self.obtener_texto()
        if texto_actual == texto_previo:
            return
        eliminado, insertado, fila = self._detectar_cambio(texto_previo, texto_actual)
        if eliminado:
            self.registrar_accion(BORRAR, fila, eliminado)
        if insertado:
            self.registrar_accion(INSERTAR, fila, insertado)
    def guardar_snapshot(self, texto_previo=None):
        # apila el estado ANTERIOR del documento, para que deshacer siempre
        # pueda retroceder hasta el punto previo a la edicion
        texto = self.obtener_texto() if texto_previo is None else texto_previo
        if not self.pila_undo.esta_vacia() and self.pila_undo.ver_tope()==texto:
            return
        self.pila_undo.apilar(texto)
        while not self.pila_redo.esta_vacia():
            self.pila_redo.desapilar()
        if texto_previo is not None:
            self._registrar_cambio(texto_previo)


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
        texto_siguiente=self.pila_redo.desapilar()
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
    def cargar_diccionario(self, ruta):
        # carga un diccionario de palabras sugeridas desde un .txt y lo deja
        # en lugar del por defecto. Formato: una palabra por linea (tambien
        # se aceptan varias separadas por espacios). Devuelve cuantas
        # palabras quedaron cargadas; un archivo sin palabras validas no
        # destruye el diccionario actual.
        lineas = CargaArchivos.cargar_documento(ruta)
        candidatas = ArregloDinamico()
        for i in range(len(lineas)):
            for palabra in lineas.obtener(i).split():
                candidatas.agregar(palabra.strip().lower())
        if len(candidatas) == 0:
            return 0
        merge_sort(candidatas)
        # al estar ordenadas, las repetidas quedan juntas: se descartan
        nuevo = ArregloDinamico(max(1, len(candidatas)))
        for i in range(len(candidatas)):
            palabra = candidatas.obtener(i)
            if i == 0 or palabra != candidatas.obtener(i - 1):
                nuevo.agregar(palabra)
        self.diccionario = nuevo
        return len(self.diccionario)
    def restaurar_diccionario_por_defecto(self):
        # vuelve a las palabras base del editor
        self.diccionario = ArregloDinamico()
        self._cargar_palabras_por_defecto()
        return len(self.diccionario)
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
        self.cursor = PosicionCursor(0,0)
        self.historial = Historial(capacidad=100)
        while not self.pila_undo.esta_vacia():
            self.pila_undo.desapilar()
        while not self.pila_redo.esta_vacia():
            self.pila_redo.desapilar()
        self._total_acciones = 0
        self._ultima_accion = None
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
    def _columnas_coincidencias(self,linea,termino):
        # columnas donde aparece 'termino' en 'linea', sin distinguir mayusculas
        linea_baja=linea.lower()
        termino_bajo=termino.lower()
        # si .lower() cambia la longitud no se pueden mapear las posiciones:
        # se busca distinguiendo mayusculas para no desalinear el resaltado
        if len(linea_baja)!=len(linea) or len(termino_bajo)!=len(termino):
            columnas=[]
            col=linea.find(termino)
            while col!=-1:
                columnas.append(col)
                col=linea.find(termino,col+len(termino))
            return columnas
        columnas=[]
        col=linea_baja.find(termino_bajo)
        while col!=-1:
            columnas.append(col)
            col=linea_baja.find(termino_bajo,col+len(termino_bajo))
        return columnas
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
                    for col in self._columnas_coincidencias(linea,palabra_buscar):
                        coincidencias.append((num_linea,col))
        else :
            for i in range (len(self.lineas)):
                linea = self.lineas.obtener(i)
                for col in self._columnas_coincidencias(linea,palabra_buscar):
                    coincidencias.append((i,col))
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
            self._reconstruir_arbol()
        return conteo 