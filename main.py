import json
import datetime
import os

opc_disponible = "1"
opcion = 0
usuarios = []
productos = []
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

    def cargar_db(self):
        with open(self.nombre_archivo) as archivo_json:
            data = json.load(archivo_json)
            usuarios = [Usuario(u["id_usuario"], u["clave"], u["nombre"], u["tipo"], u["telefono"], u["edad"], u["correo"]) for u in data["Usuarios"]]
            productos = [Producto(p["sku"], p["nombre"], p["categoria"], p["descripcion"], p["valor_neto"], p["descuento"]) for p in data["Productos"]]
            return usuarios, productos

    def guardar_db(self, usuarios, productos):
        data = {"Usuarios": [], "Productos": []}
        for u in usuarios:
            data["Usuarios"].append({"id_usuario": u.id_usuario, "clave": u.clave, "nombre": u.nombre, "tipo": u.tipo, "telefono": u.telefono, "edad": u.edad, "correo": u.correo})
        for p in productos:
            data["Productos"].append({"sku": p.sku, "nombre": p.nombre, "descripcion": p.descripcion, "categoria": p.categoria, "valor_neto": p.valor_neto, "descuento": p.descuento})
        
        with open(self.nombre_archivo, "w") as archivo_json:
            json.dump(data, archivo_json)

class Producto():

    """Clase para todos los productos de la tienda. Otorga el SKU automáticamente.
    El descuento y el impuesto viene en el formato donde 1 = 100%, es decir, el valor neto sin cambios."""

    impuesto = 1.19
    descuento = 1
    sku = 1
    def __init__(self, sku: int, nombre: str, categoria: str, descripcion: str,  valor_neto: int, descuento):
        self.sku = sku
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.proveedor = Proveedor
        self.valor_neto = valor_neto
        self.descuento = descuento
        
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
    
    def listar_ofertas(self):
        print("Listando todas las ofertas")
        print("---------------------------------------------------------------------------")
        print("Codigo Nombre        Descripcion Valor                    Descuentos")
        for x in productos:
            if int(x.descuento) > 0:
                print(f"{x.sku} {x.nombre} {x.descripcion}    {int(x.valor_neto)+(int(x.valor_neto)*0.19)}     Tiene un descuento de:{x.descuento}%")
        print("---------------------------------------------------------------------------")

    def listar_productos(self):
        print("Listando todos los productos")
        print("---------------------------------------------------------------------------")
        print("Codigo Nombre        Descripcion Valor")
        for x in productos:
            print(x.sku, x.nombre, x.descripcion, int(x.valor_neto)+(int(x.valor_neto)*0.19))
        print("---------------------------------------------------------------------------")

class Usuario(Producto):

    """Clase abstracta para todos los usuarios de la plataforma. Posee elementos comunes heredables a clases como Cliente o vendedor."""

    def __init__(self, id_usuario, clave, nombre, tipo, telefono, edad, correo):
        self.id_usuario = id_usuario
        self.clave = clave
        self.nombre = nombre
        self.tipo = tipo
        self.telefono = telefono
        self.edad = edad
        self.correo = correo

    def __set_clave(self, nueva_clave):
        self.__clave = nueva_clave

    def __get_clave(self):
        return self.__clave
    
    def listar_usuarios(self, tipo):
        print("Listando todos los Usuarios")
        print("---------------------------------------------------------------------------")
        print("Codigo       Nombre                  Telefono")
        for x in usuarios:
            if x.tipo == tipo:
                print(x.id_usuario,"           ", x.nombre,"                ",         x.telefono)
        print("---------------------------------------------------------------------------")


    #crear un nuevo usuario

    @staticmethod
    def crear_usuario(usuarios):
        id = len(usuarios) + 1 if usuarios else 1
        nick = input("Indique Nombre: ")
        print("Tipo de Usuario 1)Administrador 2)Normal 3)Vendedor):")
        opcion = int(validacion("123"))
        if opcion == 1:
            tipo = "Administrador"
        elif opcion == 2:
            tipo = "Normal"
        elif opcion == 3:
            tipo = "Vendedor"
        clave = input("Ingrese clave: ")
        telefono = input("Telefono de contacto: ")
        edad = input("Edad (Solo Numeros): ")
        correo = input("Ingrese correo: ")
        nuevo_usuario = Usuario(id, clave, nick, tipo, telefono, edad, correo)
        print(f"Esta seguro que desea crear al {tipo} con Nombre: {nick} 1)Para Confirmar 2)Salir")
        opcion = int(validacion("12"))
        if opcion == 1:
            usuarios.append(nuevo_usuario)
            grabar_nuevo = BaseDatos("basedatos.json")
            grabar_nuevo.guardar_db(usuarios,productos)


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
    
    def menu1(self):
        while True:
            limpiar_pantalla()
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("*************************                         Seleccione las siguientes Opciones para navegar:                          **************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("1)Listar Ofertas 2)Listar todos los productos 3)Administrar su cuenta 4)Salir: ")
            print(f"Bienvenido {x.nombre}")
            print("")
            opcion = int(validacion("1234"))
            if opcion == 1:
                usuario_actual.listar_ofertas()
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 2:
                usuario_actual.listar_productos()
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 3:
                print("Opcion No desarrollada")
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 4:
                break 


class Vendedor(Usuario):
    comision = 0

    def __init__(self, id_usuario, clave, nombre, tipo, telefono, edad, correo):
        super().__init__(id_usuario, clave, nombre, tipo, telefono, edad, correo)
        self.comision = Vendedor.comision

    
    def menu2(self):
        limpiar_pantalla()
        while True:
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("*************************                          Seleccione las siguientes Opciones para Vender:                          **************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print(f"Bienvenido {x.nombre}")
            print("")
            print("1)Realizar Venta 2)Listar Ofertas 3)Listar Productos 4)Cancelar Venta **** 5)Salir ****")
            opcion = int(validacion("12345"))
            if opcion == 1:
                print("Opcion No desarrollada")
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 2:
                usuario_actual.listar_ofertas()
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 3:
                usuario_actual.listar_productos()
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 4:
                print("Opcion No desarrollada")
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 5:
                break

class Administrador(Vendedor,BaseDatos):
    def menu_admin(self):
        limpiar_pantalla()
        while True:
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("*************************                     Seleccione las siguientes Opciones para administrar:                          **************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print("******************************************************************************************************************************************************")
            print(f"Bienvenido {x.nombre}")
            print("")
            print("1)Listar Productos  2)Listar Ofertas 3)Listar Clientes 4) Listar Vendedores 5) Listar Administradores 6)Crear Usuario 7)Salir: ")
            opcion = int(validacion("1234567"))
            if opcion == 1:
                usuario_actual.listar_productos()
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 2:
                usuario_actual.listar_ofertas()
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 3:
                usuario_actual.listar_usuarios("Cliente")
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 4:
                usuario_actual.listar_usuarios("Vendedor")
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 5:
                usuario_actual.listar_usuarios("Administrador")
                opcion = input("Presione cualquier tecla para continuar...")
            elif opcion == 6:
                print("***************** Ingreso de Nuevos Usuarios ******************")
                Usuario.crear_usuario(usuarios)
            elif opcion == 7:
                break


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


class CarroDeCompras():
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

            valor_total += valor_item * unidades
        return valor_total


db_completa = BaseDatos("basedatos.json")
db_cargada = db_completa.cargar_db()
usuarios = db_cargada[0]
productos = db_cargada[1]

while True:
#    limpiar_pantalla()
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("**********************************                          Bienvenidos a la tienda TeloVendo                    *************************************")
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("******************************************************************************************************************************************************")
    print("")
    usuario = input("Ingrese su Usuario (telefono ej: 933444333): ")
    for x in usuarios :
        telefono = x.telefono
        usuario_actual = Usuario(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
        if usuario == telefono:  
            if x.tipo == "Cliente":
                usuario_actual = Cliente(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
                usuario_actual.menu1()
            elif x.tipo == "Vendedor":
                usuario_actual = Vendedor(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
                usuario_actual.menu2()
            elif x.tipo == "Administrador":
                usuario_actual = Administrador(x.id_usuario, x.clave, x.nombre, x.tipo, x.telefono, x.edad, x.correo)
                usuario_actual.menu_admin()