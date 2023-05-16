import json
import datetime
import os
from main import *

class BaseDatos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.tablas = {}
        self.cargar_db()

    def cargar_db(self):
        with open(self.nombre_archivo) as archivo_json:
            data = json.load(archivo_json)
            usuarios = [Usuario(u["id_usuario"], u["clave"], u["nombre"], u["tipo"],  u["telefono"], u["edad"]) for u in data["Usuarios"]]
            return usuarios

    def guardar_db(self, usuarios, productos, bodegas, ventas):
        data = {"Usuarios": []}
        for u in usuarios:
            data["Usuarios"].append({"id_usuario": u.id_usuario, "clave": u.clave, "nombre": u.nombre, "tipo": u.tipo, "telefono": u.telefono, "edad": u.edad})
        
        with open(self.nombre_archivo, "w") as archivo_json:
            json.dump(data, archivo_json)
