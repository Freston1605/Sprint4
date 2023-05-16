import json
import datetime
import os

opc_disponible = "1"
opcion = 0
usuarios = []
data = []

class BaseDatos():
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.tablas = {}
        self.cargar_db()

    def cargar_db(self):
        with open(self.nombre_archivo) as archivo_json:
            data = json.load(archivo_json)
            usuarios = [Usuario(u["id_usuario"], u["clave"], u["nombre"], u["tipo"], u["telefono"], u["edad"], u["correo"]) for u in data["Usuarios"]]
            return usuarios

    def guardar_db(self, usuarios, productos, bodegas, ventas):
        data = {"Usuarios": []}
        for u in usuarios:
            data["Usuarios"].append({"id_usuario": u.id_usuario, "clave": u.clave, "nombre": u.nombre, "tipo": u.tipo, "telefono": u.telefono, "edad": u.edad, "correo": u.correo})
        
        with open(self.nombre_archivo, "w") as archivo_json:
            json.dump(data, archivo_json)

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

    def __set_clave(self, nueva_clave):
        self.__clave = nueva_clave

    def __get_clave(self):
        return self.__clave


class Cliente(Usuario):

    """Clase para los clientes de la plataforma."""

    def __init__(self) -> None:
        super().__init__()

class Vendedor(Usuario):

    def __init__(self) -> None:
        super().__init__()


class Proveedor(Usuario):

    def __init__(self) -> None:
        super().__init__()


class Producto():
    pass


class CarroDeCompras():

    """Clase para los carros de compras."""

    valor_total = 0

    contenido = {}

    # El valor de la ID se asigna automáticamente al iniciar
    id = 0

    def __init__(self, Cliente):
        self.cliente = Cliente
        self.id = CarroDeCompras.id
        CarroDeCompras.id += 1
        self.contenido = CarroDeCompras.contenido
        self.valor_total = CarroDeCompras.valor_total

    def añadir_producto(self, Producto, unidades):
        self.contenido.update({Producto, unidades})

    def vaciar_carro():
        pass

    def calcular_total():
        pass


db_completa = BaseDatos("basedatos.json")
db_cargada = db_completa.cargar_db()
usuarios = db_cargada[0]
print(usuarios.nombre)