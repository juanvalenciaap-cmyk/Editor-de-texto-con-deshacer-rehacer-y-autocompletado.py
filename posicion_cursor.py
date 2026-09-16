# por decision creativa, esat cosa solo va a tener la logica para mover el cursor, nada mas 
# despues con más tiempo y en otro archivo mas bonito dond eya va a ir la logica del editor
# se mete la logica para verificar, donde porongas estamos y si es valido hacer X movimiento
class PosicionCursor:
    def __init__(self, fila=0, columna=0):
        if fila < 0:
            raise ValueError("La fila no puede ser negativa")

        if columna < 0:
            raise ValueError("La columna no puede ser negativa")

        self._fila = fila
        self._columna = columna

    def mover_izquierda(self):
        if self._columna > 0:
            self._columna -= 1

    def mover_derecha(self):
        self._columna += 1

    def mover_arriba(self):
        if self._fila > 0:
            self._fila -= 1

    def mover_abajo(self):
        self._fila += 1