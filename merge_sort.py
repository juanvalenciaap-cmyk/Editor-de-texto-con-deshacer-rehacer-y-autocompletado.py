def merge_sort(arreglo):
    """
    El algoritmo divide recursivamente el arreglo en dos partes hasta
    obtener subarreglos de un solo elemento y posteriormente los mezcla
    en orden ascendente.
    Complejidad O(n log n)
    """
    if len(arreglo) <= 1:
        return

    _merge_sort(arreglo, 0, len(arreglo) - 1)


def _merge_sort(arreglo, izquierda, derecha):
    """
    Divide recursivamente una sección del arreglo dinámico en dos partes
    y ordena cada una mediante Merge Sort.
    """
    if izquierda >= derecha:
        return

    medio = (izquierda + derecha) // 2

    _merge_sort(arreglo, izquierda, medio)
    _merge_sort(arreglo, medio + 1, derecha)

    _mezclar(arreglo, izquierda, medio, derecha)


def _mezclar(arreglo, izquierda, medio, derecha):
    """
    Mezcla dos secciones previamente ordenadas del arreglo dinámico en
    una única sección ordenada.
    La primera sección comprende desde 'izquierda' hasta 'medio' y la
    segunda desde 'medio + 1' hasta 'derecha'.
     Complejidad O(n)
    """
    temporal = []

    i = izquierda
    j = medio + 1

    while i <= medio and j <= derecha:
        elemento_izquierda = arreglo.obtener(i)
        elemento_derecha = arreglo.obtener(j)

        if elemento_izquierda <= elemento_derecha:
            temporal.append(elemento_izquierda)
            i += 1
        else:
            temporal.append(elemento_derecha)
            j += 1

    while i <= medio:
        temporal.append(arreglo.obtener(i))
        i += 1

    while j <= derecha:
        temporal.append(arreglo.obtener(j))
        j += 1

    for k in range(len(temporal)):
        arreglo.establecer(izquierda + k, temporal[k])