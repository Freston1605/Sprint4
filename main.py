import json, datetime, os

class BaseDeDatos():
    pass

class Usuario():

    """Clase abstracta para todos los usuarios de la plataforma. Posee elementos comunes heredables a clases como Cliente o vendedor."""

    def __innit__(self, id_usuario: str, contraseña: str, correo: str):
        self.id_usuario = id_usuario
        self.__contraseña = contraseña
        self.correo = correo

    def __set_contraseña(self, nueva_contraseña):
        self.__contraseña = nueva_contraseña

    def __get_contraseña(self):
        return self.__contraseña
    
class Cliente(Usuario):

    """Clase para los clientes de la plataforma."""

    def __innit__(self, id_usuario: str, contraseña: str, correo: str):
        return super().__innit__(id_usuario, contraseña, correo)
    
