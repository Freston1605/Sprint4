import json
import datetime
import os

opc_disponible = "1"
opcion = 0
usuarios = []
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

    """Clase para los clientes de la plataforma. Añade el saldo del cliente.
    Todos los clientes parten con un saldo de 0 pesos"""
    saldo = 0

    def __init__(self, id_usuario, clave, nombre, tipo, telefono, edad, correo):
        super().__init__(id_usuario, clave, nombre, tipo, telefono, edad, correo)
        self.saldo = Cliente.saldo

    # Métodos para el saldo:

    def agregar_saldo(self, monto_agregado):
        """Agrega el monto ingresado en el parámetro a _saldo"""
        try:
            self.__saldo += monto_agregado
            print(
                f"Usted agrego {monto_agregado} pesos a su cartera digital. Su nuevo saldo es: {self.__saldo}")
        except TypeError:
            print(
                "Hay un problema con el tipo de dato para el saldo o el monto agregado.")

    def mostrar_saldo(self):
        print(f"Su saldo actual es: {self.__saldo}")

    def descontar_saldo(self, monto_deducido):
        """Descuenta el monto ingresado en el parámetro como argumento a la variable _saldo."""
        self.__saldo -= monto_deducido

    def get_saldo(self):
        return self.__saldo

    # Métodos para el carro de compras:

    def añadir_carro(self, **productos):
        """Agrega al carro de compras los productos ingresados como diccionario producto:unidades."""
        self.carro_compras.update(productos)

    def limpiar_carro(self):
        """Limpia el carrito de compras del usuario."""
        self.carro_compras.clear()
    """Clase para los clientes de la plataforma. Añade el saldo del cliente.
    Todos los clientes parten con un saldo de 0 pesos"""
    saldo = 0

    def __init__(self, id_usuario, clave, nombre, tipo, telefono, edad, correo):
        super().__init__(id_usuario, clave, nombre, tipo, telefono, edad, correo)
        self.saldo = Cliente.saldo

    # Métodos para el saldo:

    def agregar_saldo(self, monto_agregado):
        """Agrega el monto ingresado en el parámetro a _saldo"""
        try:
            self.__saldo += monto_agregado
            print(
                f"Usted agrego {monto_agregado} pesos a su cartera digital. Su nuevo saldo es: {self.__saldo}")
        except TypeError:
            print(
                "Hay un problema con el tipo de dato para el saldo o el monto agregado.")

    def mostrar_saldo(self):
        print(f"Su saldo actual es: {self.__saldo}")

    def descontar_saldo(self, monto_deducido):
        """Descuenta el monto ingresado en el parámetro como argumento a la variable _saldo."""
        self.__saldo -= monto_deducido

    def get_saldo(self):
        return self.__saldo

    # Métodos para el carro de compras:

    def añadir_carro(self, **productos):
        """Agrega al carro de compras los productos ingresados como diccionario producto:unidades."""
        self.carro_compras.update(productos)

    def limpiar_carro(self):
        """Limpia el carrito de compras del usuario."""
        self.carro_compras.clear()


class Vendedor(Usuario):
     
     """Clase para todos los vendedores. Añade comisión y sección del Vendedor."""

     comision = 0

     def __init__(self, id_usuario, clave, nombre, tipo, telefono, edad, correo, seccion):
        super().__init__(id_usuario, clave, nombre, tipo, telefono, edad, correo)
        self.seccion = seccion
        self.comision = Vendedor.comision


class Proveedor(Usuario):

    """Clase para todos los proveedores. Añade tipo de persona (jurídica o natural) y el rut."""

    inventario = {}

    def __init__(self, id_usuario, clave, nombre, tipo, telefono, correo, tipo_persona, rut):
        super().__init__(id_usuario, clave, nombre, tipo, telefono, correo)
        self.tipo_persona = tipo_persona
        self.rut = rut
        self.inventario = Proveedor.inventario

    def añadir_producto(self, Producto, unidades_nuevas):
        """Añade al inventario del Proveedor las unidades del producto señalado.
        Si es que ya hay unidades del producto en inventario, añade las nuevas unidades al total."""
        try:
            unidades_existentes = self.inventario[Producto]
            unidades_nuevas += unidades_existentes
        except KeyError:
            pass

        finally:
            self.inventario.update[Producto, unidades_nuevas]
    
    def descontar_productos(self, Producto, unidades_sustraidas):
        """Descuenta el número de unidades entregadas como argumento del inventario del Proveedor.
        Si es que ya hay unidades para el producto, descuenta las unidades a las existentes."""
        try:
            unidades_existentes = self.inventario[Producto]
            unidades_balance = unidades_existentes - unidades_sustraidas
        except KeyError:
            unidades_balance = unidades_sustraidas

        finally:
            self.inventario.update[Producto, unidades_balance]


class Producto():

    """Clase para todos los productos de la tienda. Otorga el SKU automáticamente.
    El descuento y el impuesto viene en el formato donde 1 = 100%, es decir, el valor neto sin cambios."""

    impuesto = 1.19
    descuento = 1
    sku = 1

    def __init__(self, nombre: str, categoria: str, stock: int, valor_neto: int,):
        self.nombre = nombre
        self.categoria = categoria
        self.proveedor = Proveedor
        self.stock = stock
        self.valor_neto = valor_neto
        self.descuento = Producto.descuento
        self.sku = Producto.sku
        Producto.sku += 1

    # Métodos para los descuentos

    def aplicar_descuento(self):
        """Devuelve el valor neto del producto con el descuento ingresado en la instancia."""
        precio_descuento = self.valor_neto * self.descuento
        return precio_descuento

    def actualizar_descuento(self, nuevo_descuento):
        """Actualiza el descuento que puede aplicar sobre el producto. El descuento es un factor que se multiplica por el valor neto.
        Por ejemplo, un 10% de descuento equivale a valor_neto * 0.9."""
        self.descuento = nuevo_descuento

    def valor_bruto(self):
        """Devuelve el valor bruto del objeto sin el IVA aplicado al valor neto."""
        valor_bruto = self.valor_neto / self.impuesto
        return valor_bruto

    def valor_impuesto(self):
        """Devuelve el detalle del impuesto."""
        try:
            valor_impuesto = self.valor_neto / self.impuesto
            return valor_impuesto
        except ZeroDivisionError:
            print(
                "Parece que hay un problema con el impuesto. Por favor revisar que no sea igual a cero.")


class CarroDeCompras():

    """Clase para los carros de compras. El valor de la ID se asigna automáticamente al iniciar"""
    """Clase para los carros de compras. El valor de la ID se asigna automáticamente al iniciar"""

    contenido = {}
    id = 0

    def __init__(self, Cliente):
        self.cliente = Cliente
        self.id = CarroDeCompras.id
        CarroDeCompras.id += 1
        self.contenido = CarroDeCompras.contenido

    def añadir_producto(self, Producto, unidades):
        """Añade al carro de compras el producto ingresado."""
        """Añade al carro de compras el producto ingresado."""
        self.contenido.update({Producto, unidades})

    def eliminar_producto(self, Producto):
        """ Elimina del carro el producto ingresado."""
        del self.contenido[Producto]

    def vaciar_carro(self):
        """Vacía todos los productos del carro."""
        self.contenido.clear()

    def calcular_total(self):
        """Calcula el total de la compra según los productos y las unidades dentro de éste."""
        valor_total = 0
        for item in self.contenido:
            unidades = self.contenido[item]
            if item.descuento != 0:
                valor_item = item.aplicar_descuento()
            else:
                valor_item = item.valor_neto
    def calcular_total(self):
        """Calcula el total de la compra según los productos y las unidades dentro de éste."""
        valor_total = 0
        for item in self.contenido:
            unidades = self.contenido[item]
            if item.descuento != 0:
                valor_item = item.aplicar_descuento()
            else:
                valor_item = item.valor_neto

            valor_total += valor_item * unidades
        return valor_total


db_completa = BaseDatos("basedatos.json")
db_cargada = db_completa.cargar_db()
usuarios = db_cargada[0]
print(usuarios.nombre)

while True:
    limpiar_pantalla()
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("**********************************                          Bienvenidos a la tienda Telecompro                   *************************************")
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("")
    usuario = input("Ingrese su nombre de usuario aquí: ")
    for x in usuarios:
        nombre = x.nick
        usuario_actual = Usuario(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
        if x.tipo == "Normal":
            usuario_actual = Cliente(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
            usuario_actual.menu2()
        elif x.tipo == "Vendedor":
            usuario_actual = Vendedor(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
            usuario_actual.menu3()