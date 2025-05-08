from PIA_Modulo2 import obtener_datos_ciudades, mostrar_resultados, graficar_temperaturas, exportar_datos_a_excel

ciudades = []
cantidad = int(input("\nIngrese la cantidad de ciudades que desea consultar: "))
for ciudad in range(0, cantidad):
    lugar = input(f"\nIngrese la ciudad {ciudad + 1} que desea consultar: ")
    ciudades.append(lugar)

datos = obtener_datos_ciudades(ciudades)
mostrar_resultados(datos)
graficar_temperaturas(datos)
exportar_datos_a_excel(datos)