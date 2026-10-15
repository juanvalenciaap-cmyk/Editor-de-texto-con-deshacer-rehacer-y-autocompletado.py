from dataclasses import dataclass
from arreglo_dinamico import ArregloDinamico
INSERTAR ="INSERTAR"
BORRAR = "BORRAR"
dataclass(frozen=True)
class opeeracion:
    """edicion
    tipo: INSERTAR O BORRAR
    posicion:
    texto
    """
    tipo: str
    posicion:int
    texto:str
    def inversa(self):
        """deshace"""
        nuevo_tipo=BORRAR if self.tipo==INSERTAR else INSERTAR
        return opeeracion(nuevo_tipo,self.posicion,self.texto)

class EstructuraLlenaError(Exception):
    pass

class EstructuraVaciaError(Exception):
    pass
def _crear_arreglo_fijo(capacidad):
    """ArregloDinamico de un tamaño"""
    arreglo=ArregloDinamico(capacidad)
    for _ in range(capacidad):
        arreglo.agregar(None)
    return arreglo

class PilaEstatica:
    def __init__(self,capacidad=100):
        if capacidad  <=0:
            raise ValueError("no puede ser negativa")
        self._datos=_crear_arreglo_fijo(capacidad)
        self._capacidad=capacidad
        self._tope=0
    def esta_vacia(self):
        return self._tope==0
    def esta_llena(self):
        return self._tope==self._capacidad
    def tamano(self):
        return self._tope
    def push(self,elemento):
        if self.esta_llena():
            raise EstructuraLlenaError("Pila llena")
        self._datos.establecer(self._tope,elemento)
        self._tope+=1
    def pop(self):
        if self.esta_vacia():
            raise EstructuraVaciaError("Pila vacia")
        self._tope-=1
        elemento=self._datos.obtener(self._tope)
        self._datos.establecer(self._tope,None)
        return elemento
    def peek(self):
        if self.esta_vacia():
            raise EstructuraVaciaError("Pila vacia")
        return self._datos.obtener(self._tope-1)
    def vaciar(self):
        while not self.esta_vacia():
            self.pop()
    def __len__(self):
        return self._tope
    def __repr__(self):
        return f"PilaEstatica({[self._datos.obteber(i)for i in range(self._tope)]})"

    class ColaEstatica:
        def __init__(self,capacidad=100):
            if capacidad<=0:
                raise ValueError("no puede ser negativa")
            self._datos== _crear_arreglo_fijo(capacidad)
            self._capacidad=capacidad
            self._frente=0
            self._tamano=0
        def esta_vacia(self):
            return self._tamano==0
        def esta_llena(self):
            return self._tamano==self._capacidad
        def tamano(self):
            return self._tamano
        def enqueue(self,elemento):
            if self.esta_llena():
                raise EstructuraLlenaError("Cola llena")
            final=(self._frente+self._tamano)%self._capacidad
            self.datos.establecer(final,elemento)
            self._tamano+=1
        def dequeue(self):
            if self.esta_vacia():
                raise EstructuraLlenaError("Cola vacia")
            elemento=self._datos.obtener(self._frente)
            self._datos.establecer(self._frente,None)
            self._frente=(self._frente+1)%self._capacidad
            self._tamano-=1
            return elemento
        def peel(self):
            if self.esta_vacia():
                raise  EstructuraVaciaError("cola vacia")
            return self._datos.obtener(self._frente)
        def vaciar(self):
            while not self.esta_vacia():
                self.dequeue()
        def __len__(self):
            items=[self._datos.obtener((self._frente + i) % self._capacidad)
                   for i in range(self._tamano)]
            return f"ColaEstatica({items})"

class Historial:
    """deshacer y rehacer"""
    def __init__(self, capacidad=100):
        self._deshacer=PilaEstatica(capacidad)
        self._rehacer=PilaEstatica(capacidad)
    def registrar(self, operacion):
        self._deshacer.push(operacion)
        self._rehacer.vaciar()
    def deshacer(self):
        """devuelve la inversa"""
        op=self._deshacer.pop()
        self._deshacer.push(op)
        return op.inversa()
    def rehacer(self):
        "devuelve la original"
        op=self._rehacer.pop()
        self._deshacer.push(op)
        return op
    def puede_deshacer(self):
        return not self._deshacer.esta_vacia()
    def puede_rehacer(self):
        return not self._rehacer.esta_vacia()        