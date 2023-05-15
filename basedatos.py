import json
import datetime
import os

class BaseDatos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.tablas = {}
        self.cargar_db()

    def cargar_db(self):
        with open(self.nombre_archivo) as archivo_json:
            data = json.load(archivo_json)
            usuarios = [Usuario(u["id"], u["nick"], u["tipo"], u["clave"], u["telefono"], u["edad"]) for u in data["Usuarios"]]
            return usuarios

    def guardar_db(self, usuarios, productos, bodegas, ventas):
        data = {"Usuarios": [], "Productos": [], "Bodegas": [], "Ventas": []}
        for u in usuarios:
            data["Usuarios"].append({"id": u.id, "nick": u.nick, "tipo": u.tipo, "clave": u.clave, "telefono": u.telefono, "edad": u.edad})
        
        with open(self.nombre_archivo, "w") as archivo_json:
            json.dump(data, archivo_json)


import json
import datetime
import os
from basedatos import *

opc_disponible = "1"
opcion = 0
usuarios = []
productos = []
bodega = []
ventas = []
data = []





#iniciando las bases de archivo
db_completa = BaseDatos("main.json")
db_cargada = db_completa.cargar_db()
usuarios = db_cargada[0]

for x in usuarios:
    print(x.nick)