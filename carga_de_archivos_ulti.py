import os
from arreglo_dinamico import ArregloDinamico

class CargaArchivos:
    @staticmethod
    def cargar_documento(ruta_archivo):
        # lee un archivo del disco y carga cada línea en un ArregloDinamico
        lineas = ArregloDinamico()

        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe.")

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea_limpia = linea.rstrip("\r\n")
                lineas.agregar(linea_limpia)

        if lineas.esta_vacio():
            lineas.agregar("")

        return lineas

    @staticmethod
    def guardar_documento(ruta_archivo, lineas_arreglo):
        # Toma el ArregloDinamico de líneas y lo escribe en el disco.
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for i in range(len(lineas_arreglo)):
                linea = lineas_arreglo.obtener(i)
                archivo.write(linea + "\n")


class NodoArchivo:
   #Representa un archivo dentro del grafo del editor
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.nombre = os.path.basename(ruta_archivo)
        self.lineas = None # Aquí se guarda el ArregloDinamico
        self.vecinos = [] # Arcos que conectan con otros archivos (dependencias o historial)

    def cargar_contenido(self):
        if self.lineas is None:
            self.lineas = CargaArchivos.cargar_documento(self.ruta_archivo)


class GestorArchivosGrafo:
    #gestiona el grafo de archivos abiertos y el historial de navegación
    def __init__(self):
        self.nodos = {} # diccionario para acceso rápido por ruta: {ruta: NodoArchivo}
        self.historial = [] # lista o pila que funciona como historial de navegación lineal o de grafo
        self.indice_historial = -1 # Apunta a la posición actual en el historial (para deshacer/rehacer navegación)
        self.nodo_actual = None

    def abrir_o_enfocar_archivo(self, ruta_archivo):
        #abre un archivo, lo añade al grafo si no existe, y actualiza el historial
        ruta_absoluta = os.path.abspath(ruta_archivo)

        # si el nodo no está en el grafo, lo creamos
        if ruta_absoluta not in self.nodos:
            nuevo_nodo = NodoArchivo(ruta_absoluta)
            nuevo_nodo.cargar_contenido()
            self.nodos[ruta_absoluta] = nuevo_nodo
        
        nodo = self.nodos[ruta_absoluta]

        # conectamos con el archivo anterior en el grafo (crea una relación dirigida en el grafo)
        if self.nodo_actual and self.nodo_actual != nodo:
            if nodo not in self.nodo_actual.vecinos:
                self.nodo_actual.vecinos.append(nodo)

        # gestionar el historial de navegación (estilo navegador web: A -> B -> C)
        # si estábamos navegando hacia atrás y abrimos algo nuevo, cortamos el futuro
        if self.indice_historial < len(self.historial) - 1:
            self.historial = self.historial[:self.indice_historial + 1]

        self.historial.append(nodo)
        self.indice_historial = len(self.historial) - 1
        self.nodo_actual = nodo

        return nodo

    def navegar_atras(self):
        #permite retroceder en el historial de archivos visitados
        if self.indice_historial > 0:
            self.indice_historial -= 1
            self.nodo_actual = self.historial[self.indice_historial]
            return self.nodo_actual
        return None

    def navegar_adelante(self):
        #permite avanzar en el historial de archivos visitados
        if self.indice_historial < len(self.historial) - 1:
            self.indice_historial += 1
            self.nodo_actual = self.historial[self.indice_historial]
            return self.nodo_actual
        return None
#y aqui esta, mi magnus opus de la carga de archivos, el profesor me dijo que una recomendacion era 
#hacer un grafo para todo el codigo, pero como saben, decidi agregarlo a la carga de archivos con la 
#funcionalidad de historial, de esta manera deberia permitir mover entre los archivos que usaste anteriormente
