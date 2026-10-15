# Chicos lo siento pero hoy no voy a poder poner la explicacion de todo este mamotrero en comentarios,
# Igual es simple, lo que vimos en clase de nodos y listas, las operaciones basicas.
# aqui no hay nada extraño
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None


class lista_doble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamaño = 0

    def esta_vacio(self):
        return self.tamaño == 0
    
    def __len__(self):
        return self.tamaño

    def __obtener_nodo(self, indice):
        if indice < 0 or indice >= self.tamaño:
            raise IndexError("Índice fuera de rango")

        #O(n/2)
        if indice < self.tamaño // 2:
            nodo = self.cabeza
            for i in range(indice):
                nodo = nodo.siguiente

        else:
            nodo = self.cola
            for i in range(self.tamaño - indice - 1):
                nodo = nodo.anterior
        return nodo    

    def agregar_final(self, valor):
        #O(1)
        nuevo_nodo = Nodo(valor)
        if self.esta_vacio():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamaño += 1
    
    def insertar(self, indice, valor):
        
        if indice < 0 or indice > self.tamaño:
            raise IndexError("Índice fuera de rango")
        if indice==self.tamaño:
            self.agregar_final(valor)
            return
        nuevo_nodo = Nodo(valor)
        if indice==0:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        else:
            # solo voy a medio explicar esto que me parece medio enredado.
            # el nodo que vamos a insertar va pasar a ser anterior al nodo que vamos a obtener con el indice
            # y va ser el siguiente del anterior del nodo que vamos a obtener con el indice.
            # basicamente es: el nodo nuevo es❤️, el que vamos a obtener con el indice es 👍, y el anterior a ese es😎
            # entonces: ❤️-> 😎-❤️-👍
            # no se si se entiende, espero que si
            nodo = self.__obtener_nodo(indice)
            anterior_nodo = nodo.anterior
            anterior_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = anterior_nodo
            nuevo_nodo.siguiente = nodo
            nodo.anterior = nuevo_nodo
            
        self.tamaño += 1
            
        
    def eliminar(self, indice):
        if self.esta_vacio():
            raise IndexError("La lista está vacía")
        nodo_a_eliminar=self.__obtener_nodo(indice)
        valor= nodo_a_eliminar.valor
        if self.tamaño == 1:
            self.cabeza = None
            self.cola = None
        elif nodo_a_eliminar == self.cabeza:
            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = None
        elif nodo_a_eliminar == self.cola:
            self.cola = self.cola.anterior
            self.cola.siguiente = None
        else:
            nodo_a_eliminar.anterior.siguiente = nodo_a_eliminar.siguiente
            nodo_a_eliminar.siguiente.anterior = nodo_a_eliminar.anterior
        self.tamaño -= 1
        return valor

    def modificar(self, indice, valor):
        nodo = self.__obtener_nodo(indice)
        nodo.valor = valor
    # y lo pasamos a listas, para manejarlo con los archivos TXT 
    def a_lista(self):
        resultado = []
        nodo = self.cabeza
        while nodo is not None:
            resultado.append(nodo.valor)
            nodo = nodo.siguiente
        return resultado 


    def __getitem__(self, indice):
        nodo = self.__obtener_nodo(indice)
        return nodo.valor


    def __setitem__(self, indice, valor):
        self.modificar(indice, valor)

# Like y suscripsion