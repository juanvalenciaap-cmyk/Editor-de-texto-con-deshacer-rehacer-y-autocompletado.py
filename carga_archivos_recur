import os

class CargaArchivos:
    @staticmethod
    def cargar_documento_recursivo(ruta_archivo):
        lineas = ArregloDinamico()

        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe.")

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            
            # funcion axuliar recursiva 
            def leer_siguiente_linea():
                linea = archivo.readline()
                
                #caso base si la linea esta vacia (llegamos al final del archivo) ya para
                if not linea:
                    return
                
                # procesamos la linea actual y la agregamos al arreglo
                lineas.agregar(linea.rstrip("\r\n"))
                
                # aqui el caso recursivo La función se llama a sí misma para leer la siguiente línea
                leer_siguiente_linea()

            # iniciamos la recursividad leyendo la primera línea
            leer_siguiente_linea()

        # si el archivo está totalmente vacio aseguramos al menos una línea
        if lineas.esta_vacio():
            lineas.agregar("")

        return lineas

    @staticmethod
    def guardar_documento(ruta_archivo, lineas_arreglo):
        #ya el mnetodo que tenia originalmente de guardado no lo cambio jeje
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for i in range(len(lineas_arreglo)):
                linea = lineas_arreglo.obtener(i)
                archivo.write(linea + "\n")
#bueno ya ahora despues de implementar el algoritmo recursivo esto es mas que nada para
#entender como funciona, puesto que ya viendolo de manera general este algoritmo recursivo
#ya que solo funciona con archivos pequeños, por que si recordamos python tiene un limite
#de 1000 y si por ejemplo abres un archivo de 1500 lineas pues te soltara un "recursionerror"
#y yam, eso era to 👻👻
#ah si, decidi utilizarlo con este carga archivos puesto que me parecia lo mas optimo para practicar
#de buena manera la recursividad, si el profe me lo indica obviamente lo cambiare a una zona donde
#no pase lo del error de recursividad o no sea tan "pesado"
