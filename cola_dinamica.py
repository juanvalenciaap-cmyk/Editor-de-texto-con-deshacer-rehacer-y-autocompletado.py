from arreglo_dinamico import ArregloDinamico


class ColaDinamica:
    """Cola FIFO implementada con un arreglo dinámico."""

    def __init__(self):
        self.elementos = ArregloDinamico()

    def esta_vacia(self) -> bool:
        return self.elementos.esta_vacio()

    def encolar(self, elemento) -> None:
        self.elementos.agregar(elemento)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")

        elemento = self.elementos.obtener(0)
        self.elementos.eliminar(0)
        return elemento

    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")

        return self.elementos.obtener(0)

    def tamano(self) -> int:
        return len(self.elementos)
