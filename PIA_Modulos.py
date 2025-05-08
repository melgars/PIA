import requests
import matplotlib.pyplot as plt
import pandas as pd
import re
import statistics

api_key = "insertar api key"

def validar_ciudad(ciudad):
    patron = r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s\-]+$"
    return re.match(patron, ciudad)

def obtener_datos_ciudades(ciudades):
    datos_ciudades = []

    for ciudad in ciudades:
        if not validar_ciudad(ciudad):
            continue

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units=metric&lang=es"
        respuesta = requests.get(url)
        datos = respuesta.json()

        temperaturas = []
        humedades = []
        vientos = []

        for pronostico in datos["list"]:
            hora = pronostico["dt_txt"].split(" ")[1]
            if hora == "12:00:00":
                temperaturas.append(pronostico["main"]["temp"])
                humedades.append(pronostico["main"]["humidity"])
                vientos.append(pronostico["wind"]["speed"])
                if len(temperaturas) == 5:
                    break

        datos_ciudades.append({
            "ciudad": ciudad,
            "temperaturas": temperaturas,
            "humedades": humedades,
            "vientos": vientos
        })

    return datos_ciudades

def calcular_estadisticas(valores):
    return {
        'promedio': sum(valores) / len(valores),
        'media': statistics.mean(valores),
        'mediana': statistics.median(valores),
        'moda': statistics.mode(valores),
        'varianza': statistics.variance(valores),
        'desviación estándar': statistics.stdev(valores)
    }

def imprimir_estadisticas(nombre, estadisticas):
    print(f"\nEstadísticas para {nombre.capitalize()}:")
    for clave, valor in estadisticas.items():
        print(f"{clave:<20} {valor:>10.4f}")

def mostrar_resultados(datos_ciudades):
    for ciudad in datos_ciudades:
        print(f"\nCiudad: {ciudad['ciudad']}")
        print(f"Temperaturas: {ciudad['temperaturas']}")
        print(f"Humedades: {ciudad['humedades']}")
        print(f"Vientos: {ciudad['vientos']}")

        for clave in ['temperaturas', 'humedades', 'vientos']:
            resultado = calcular_estadisticas(ciudad[clave])
            imprimir_estadisticas(clave, resultado)

def exportar_datos_a_excel(datos_ciudades, nombre_archivo="reporte_clima.xlsx"):
    filas = []
    for ciudad in datos_ciudades:
        for i in range(len(ciudad['temperaturas'])):
            filas.append({
                "Ciudad": ciudad["ciudad"],
                "Día": i + 1,
                "Temperatura (°C)": ciudad["temperaturas"][i],
                "Humedad (%)": ciudad["humedades"][i],
                "Viento (m/s)": ciudad["vientos"][i]
            })

    df = pd.DataFrame(filas)
    df.to_excel(nombre_archivo, index=False)
    print(f"\nArchivo '{nombre_archivo}' creado con éxito.")

def graficar_temperaturas(datos_ciudades):
    dias = list(range(1, 6))
    for datos in datos_ciudades:
        plt.plot(dias, datos["temperaturas"], 'o-', label=datos["ciudad"], linewidth=2, markersize=8)

    plt.xlabel("Días (pronóstico)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Comparación de temperaturas a las 12:00 PM")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(dias)
    plt.show()