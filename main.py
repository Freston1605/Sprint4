import json
import datetime
import os
from basedatos import *


opc_disponible = "1"
opcion = 0
usuarios = []
data = []


class Usuario():

    """Clase abstracta para todos los usuarios de la plataforma. Posee elementos comunes heredables a clases como Cliente o vendedor."""

    def __innit__(self, id_usuario: str, clave: str, nombre, tipo, telefono, edad, correo):
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
