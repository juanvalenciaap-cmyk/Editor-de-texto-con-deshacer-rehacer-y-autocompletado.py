from lista_doble import lista_doble
class NodoArbol:
    def __init__(self,palabra,linea):
        self.palabra=palabra
        self.lineas=lista_doble()
        self.lineas.agregar_final(linea)
        self.izquierdo=None
        self.derecho=None
class ArbolBusqueda:
    def __init__(self):
        self.raiz=None
        self.tamaño=0
    def esta_vacio(self):
        return self.raiz is None
    def __len__(self):
        return self.tamaño
    def insertar(self,palabra,linea):
        palabra=palabra.lower()
        if self.raiz is None:
            self.raiz=NodoArbol(palabra,linea)
            self.tamaño +=1
            return
        actual=self.raiz
        while True:
            if palabra==actual.palabra:
                self.__anotar_linea(actual,linea)
                return
            if palabra < actual.palabra:
                if actual.izquierdo is None:
                    actual.izquierdo=NodoArbol(palabra,linea)
                    self.tamaño += 1
                    return
                actual= actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho=NodoArbol(palabra,linea)
                    self.tamaño +=1
                    return
                actual= actual.derecho
    def __anotar_linea(self,nodo,linea):
        if nodo.lineas[len(nodo.lineas)-1]!=linea:
            nodo.lineas.agregar_final(linea)
    def buscar(self,palabra):
        palabra=palabra.lower()
        actual = self.raiz
        while actual is not None:
            if palabra == actual.palabra:
                return actual.lineas
            if palabra < actual.palabra:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None
    def inorden(self):
        resultado=lista_doble()
        self.__inorden(self.raiz,resultado)
        return resultado
    def __inorden(self,nodo,resultado):
        if nodo is None:
            return
        self.__inorden(nodo.izquierdo,resultado)
        resultado.agregar_final((nodo.palabra,nodo.lineas.a_lista()))
        self.__inorden(nodo.derecho,resultado)
    def preorden(self):
        resultado=lista_doble()
        self.__preorden(self.raiz,resultado)
        return resultado
    def __preorden(self,nodo,resultado):
        if nodo is None:
            return
        resultado.agregar_final((nodo.palabra,nodo.lineas.a_lista()))
        self.__preorden(nodo.izquierdo,resultado)
        self.__preorden(nodo.derecho,resultado)
    def por_niveles(self):
        resultado=lista_doble()
        if self.raiz is None:
            return resultado
        cola=lista_doble()
        cola.agregar_final(self.raiz)
        while not cola.esta_vacio():
            nodo=cola.eliminar(0)
            resultado.agregar_final((nodo.palabra,nodo.lineas.a_lista()))
            if nodo.izquierdo is not None:
                cola.agregar_final(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.agregar_final(nodo.derecho)
        return resultado
    def buscar_prefijos(self,prefijo):
        resultado=lista_doble()
        self.__prefijo(self.raiz,prefijo.lower(),resultado)
        return resultado
    def __prefijo(self,nodo,prefijo,resultado):
        if nodo is None:
            return
        coincide=nodo.palabra.startswith(prefijo)
        if nodo.palabra >= prefijo:
            self.__prefijo(nodo.izquierdo,prefijo,resultado)
        if coincide:
            resultado.agregar_final((nodo.palabra,nodo.lineas.a_lista()))
        if coincide or nodo.palabra < prefijo:
            self.__prefijo(nodo.derecho,prefijo,resultado)
    def indexar_texto(self,lineas):
        for i in range(len(lineas)):
            for palabra in self.__separar_palabras(lineas[i]):
                self.insertar(palabra, i + 1)
    def __separar_palabras(self,texto):
        palabras=[]
        actual=""
        for caracter in texto:
            if caracter.isalnum():
                actual += caracter
            else:
                if actual !="":
                    palabras.append(actual)
                actual = ""
        if actual != "":
            palabras.append(actual)
        return palabras    