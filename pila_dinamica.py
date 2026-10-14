from arreglo_dinamico import ArregloDinamico


class PilaDinamica:
    """Cola FIFO implementada con un arreglo dinámico."""

    def __init__(self):
        self.elementos = ArregloDinamico()

    def esta_vacia(self) -> bool:
        return self.elementos.esta_vacio()

    def apilar(self, elemento) -> None:
        self.elementos.agregar(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")

        indice_tope = len(self.elementos) - 1
        elemento = self.elementos.obtener(indice_tope)
        self.elementos.eliminar(indice_tope)
        return elemento

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")

        return self.elementos.obtener(len(self.elementos) - 1)

    def tamano(self) -> int:
        return len(self.elementos)
