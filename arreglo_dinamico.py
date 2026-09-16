
class ArregloDinamico:
    def __init__(self, capacidad_inicial=4):
        if capacidad_inicial <=0:
            raise ValueError("La capacidad inicial debe ser mayor a 0")
        self._datos = [None] * capacidad_inicial
        self._capacidad_total = capacidad_inicial
        self._tamaño = 0

    def agregar(self, elemento):
        if self._tamaño == self._capacidad_total:
            self._redimensionar()
        self._datos[self._tamaño] = elemento
        self._tamaño += 1 

    def _redimensionar(self):
        #O(n)
        self._capacidad_total *= 2
        nuevo_arreglo = [None] * self._capacidad_total
        for i in range(self._tamaño):
            nuevo_arreglo[i] = self._datos[i]
        self._datos = nuevo_arreglo

    def obtener(self, indice):
        #O(1)
        if indice < 0 or indice >= self._tamaño:
            raise IndexError("Índice fuera de rango")
        return self._datos[indice]    

    def establecer(self, indice, elemento):
        #O(1)
        if indice < 0 or indice >= self._tamaño:
            raise IndexError("Índice fuera de rango")
        self._datos[indice] = elemento    

    def eliminar(self, indice):    
        #O(n)
        if indice < 0 or indice >= self._tamaño:
            raise IndexError("Índice fuera de rango")
        for i in range(indice, self._tamaño - 1):
            self._datos[i] = self._datos[i + 1]
        self._datos[self._tamaño - 1] = None    
        self._tamaño -= 1  

    def insertar(self, indice, elemento):
        #O(n)
        if indice < 0 or indice > self._tamaño:
            raise IndexError("Índice fuera de rango")
        if self._tamaño == self._capacidad_total:
            self._redimensionar()
        for i in range(self._tamaño, indice, -1):
            self._datos[i] = self._datos[i - 1]    
        self._datos[indice] = elemento    
        self._tamaño += 1    

    def __len__(self):
        #O(1)
        return self._tamaño

    def esta_vacio(self):
        #O(1)
        return self._tamaño == 0