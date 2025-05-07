from flask import Flask, request, render_template
import math
import random
from flask_cors import CORS  
import os  

app = Flask(__name__, static_folder='static')
CORS(app)

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = sum(distancia(coord[ruta[i]], coord[ruta[i + 1]]) for i in range(len(ruta)-1))
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  
    return total

def hill_climbing_iterativo(coord, iteraciones=10):
    mejor_ruta_global = None
    mejor_distancia_global = float('inf')

    for _ in range(iteraciones):  
        ruta = list(coord.keys())
        random.shuffle(ruta)  

        mejor_ruta = ruta[:]
        max_iteraciones = 10

        while max_iteraciones > 0:
            mejora = False
            random.shuffle(ruta)  
            dist_actual = evalua_ruta(ruta, coord)

            for i in range(len(ruta)):  
                for j in range(len(ruta)):  
                    if i != j:
                        ruta_tmp = ruta[:]
                        ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                        dist = evalua_ruta(ruta_tmp, coord)
                        if dist < dist_actual:
                            mejora = True
                            ruta = ruta_tmp[:]
                            dist_actual = dist
            
            max_iteraciones -= 1
            
            if evalua_ruta(ruta, coord) < evalua_ruta(mejor_ruta, coord):
                mejor_ruta = ruta[:]

        distancia_mejor = evalua_ruta(mejor_ruta, coord)
        if distancia_mejor < mejor_distancia_global:
            mejor_distancia_global = distancia_mejor
            mejor_ruta_global = mejor_ruta

    return mejor_ruta_global, mejor_distancia_global

@app.route('/')
def home():
    mejor_ruta, distancia_total = hill_climbing_iterativo(coord)
    return render_template('index.html', ciudades=list(coord.keys()), ruta=mejor_ruta, distancia_total=distancia_total)

@app.route('/tsp', methods=['POST'])
def resolver_tsp():
    mejor_ruta, distancia_total = hill_climbing_iterativo(coord)
    return render_template('index.html', ciudades=list(coord.keys()), ruta=mejor_ruta, distancia_total=distancia_total)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
