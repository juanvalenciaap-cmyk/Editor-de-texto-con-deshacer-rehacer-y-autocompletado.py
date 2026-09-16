def busqueda_binaria(arreglo, objetivo):
    """
    Divide el arreglo en dos partes para comparar
    el elemento que se busca con el elemento de la mitad
    dependiendo del resultado toma una de las dos mitades
    y asi sucesivamente hasta dar con el elemeto que se busca
    Complejidad O(log n)
    """
    izquierda = 0
    derecha = len(arreglo) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        elemento = arreglo.obtener(medio)

        if elemento == objetivo:
            return medio

        if elemento < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1