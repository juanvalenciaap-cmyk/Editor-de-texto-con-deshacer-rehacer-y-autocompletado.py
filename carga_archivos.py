import os

class CargaArchivos:
    @staticmethod
    def cargar_documento(ruta_archivo):
        
        #lee un archivo del disco y carga cada línea en un ArregloDinamico nigga
        
        lineas = ArregloDinamico()

        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe.")

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                # quitamos el salto de línea al final para guardar la cadena limpia
                linea_limpia = linea.rstrip("\r\n")
                lineas.agregar(linea_limpia)

        # si el archivo está totalmente vacío, aseguramos al menos una línea
        if lineas.esta_vacio():
            lineas.agregar("")

        return lineas

    @staticmethod
    def guardar_documento(ruta_archivo, lineas_arreglo):
        
        
        #toma el ArregloDinamico de líneas y lo escribe en el disco.
        
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for i in range(len(lineas_arreglo)):
                linea = lineas_arreglo.obtener(i)
                archivo.write(linea + "\n")

#esto es un ejemplo/alfa, no entendi muy bien  las explicaciones del profe por lo tanto
# lo hice como yo lo entendi, obviamente el codigo esta sujeto a cambios y mejoras
#se le preguntara al profe las indicaciones wazaaaaaaaaaaaaaa👻👻👻👻👻👻👻👻👻
# ya lo que el me indique le metere un crafteo a la vaina, yarbis, abre la coca 🛩️🏢🏢
