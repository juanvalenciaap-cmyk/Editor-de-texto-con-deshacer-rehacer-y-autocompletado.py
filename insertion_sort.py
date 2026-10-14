from arreglo_dinamico import ArregloDinamico

def insertion_sort(arreglo):
    """
    Va recorriendo el arreglo tomando los elementos para posteriormente insertarlos en la seccion del arreglo que ya está ordenada
    Complejidad O(n²) en el peor de los casos
    """
    for i in range(1, len(arreglo)):

        elemento = arreglo.obtener(i)
        j = i - 1

        while j >= 0 and arreglo.obtener(j) > elemento:
            arreglo.establecer(j + 1, arreglo.obtener(j))
            j -= 1

        arreglo.establecer(j + 1, elemento)