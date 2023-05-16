import json
import datetime
import os

opc_disponible = "1"
opcion = 0
usuarios = []
productos = []
bodega = []
ventas = []
data = []



def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

#validar opciones para evitar falsos ingresos
def validacion(opc_disponible):
    """
    Funcion para validar que las opciones digitadas sean correctas
    """
    opcion_ingresada = input()
    while True:
        if opcion_ingresada in opc_disponible:
            return opcion_ingresada 
        else:
            print("Opcion Ingresada no valida")
            opcion_ingresada = input()

class BaseDatos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.tablas = {}
        self.cargar_db()

    def cargar_db(self):
        with open(self.nombre_archivo) as archivo_json:
            data = json.load(archivo_json)
            usuarios = [Usuario(u["id_usuario"], u["clave"], u["nombre"], u["tipo"], u["telefono"], u["edad"], u["correo"]) for u in data["Usuarios"]]
            return usuarios
        
class Usuario():

    """Clase abstracta para todos los usuarios de la plataforma. Posee elementos comunes heredables a clases como Cliente o vendedor."""

    def __init__(self, id_usuario, clave, nombre, tipo, telefono, edad, correo):
        self.id_usuario = id_usuario
        self.__clave = clave
        self.nombre = nombre
        self.tipo = tipo
        self.telefono = telefono
        self.edad = edad
        self.correo = correo

db_completa = BaseDatos("basedatos.json")
db_cargada = db_completa.cargar_db()
for x in db_cargada:
    print(x.nombre)