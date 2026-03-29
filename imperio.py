#impprtaciones necesarias
from abc import ABCMeta, abstractmethod
from enum import Enum
from excepciones import StockInsuficienteError, RepuestoNoEncontradoError, WrongType


class EUbicacion(Enum): #Enum para las ubicaciones de las naves
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class EClaseNave(Enum): #Enum para las clases de las naves estelares
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

#clase padre Nave 
class Nave:
    """
    Clase base que representa una nave genérica del sistema.
    Contiene atributos comunes a todas las naves, como el nombre y el catálogo de repuestos necesarios para su mantenimiento.
    """

    def __init__(self, nombre, catalogo):
        if not isinstance(nombre, str): # si el nombre no es una cadena de texto entonces lanza error
            raise WrongType("El nombre de la nave debe ser un string")
        
        if not isinstance(catalogo, list) or not all(isinstance(x, str) for x in catalogo): # si el catálogo no es una lista de objetos string entonces lanza error
            raise WrongType("El catálogo debe de ser una lista de nombres de repuestos (string)")
        
        self.nombre = nombre
        self.catalogo = catalogo

    # setters y getters para controlar el acceso a los atributos y validar los datos

    def set_nombre(self, nombre:str):
        """Establece el nombre de la nave, controlando que sea un string válido."""
        if not isinstance(nombre, str):
            raise WrongType("El nombre de la nave debe ser un string")
        self.nombre = nombre
    
    def set_catalogo(self, catalogo:list[str]):
        """Establece el catálogo de repuestos necesarios para el mantenimiento de la nave, controlando que sea una lista de strings válida."""
        if not isinstance(catalogo, list) or not all(isinstance(x, str) for x in catalogo): # si el catálogo no es una lista de objetos string entonces lanza error
            raise WrongType("El catálogo debe de ser una lista de nombres de repuestos (string)")
        self.catalogo = catalogo
    
    def get_nombre(self):
        """Devuelve el nombre de la nave."""
        return self.nombre
    
    def get_catalogo(self):
        """Devuelve el catálogo de repuestos de la nave."""
        return self.catalogo
    
    # métodos de la clase Nave

    def mostrar_catalogo(self):
        """Muestra el catálogo de repuestos necesarios para el mantenimiento de la nave."""
        for repuesto in self.catalogo:
            print(repuesto)

    def usar_repuesto(self, nombre: str):
        """Comprueba si un repuesto está disponible en el catálogo de la nave."""
        if not isinstance(nombre, str): # si el nombre no es una cadena de texto entonces lanza error
            raise WrongType("El nombre de la nave debe ser un string")
        return nombre in self.catalogo
    
    def __str__(self):
        return f"Nave: {self.nombre}, \nCatalogo: {self.catalogo}"
    

#clase Unidad de combate
class UnidadCombate:
    """
    Representa una unidad de combate con un ID de combate único y una clave de acceso.
    Se usa como clase base para diferentes tipos de naves de combate, como estaciones espaciales, naves estelares y cazas estelares.
    """

    def __init__(self, id_combate, clave):
        if not isinstance(id_combate, str): # si el id_combate no es una cadena de texto entonces lanza error
            raise WrongType("El id_combate de la nave debe ser un string")
        
        if not isinstance(clave, int): # si la clave no es un número entero entonces lanza error
            raise WrongType("La clave de la nave debe ser un número entero")
        
        self.id_combate = id_combate
        self.clave = clave
    
    # setters y getters para controlar el acceso a los atributos y validar los datos

    def set_id_combate(self, id_combate: str):
        """Establece el ID de combate de la nave, controlando que sea un string válido."""
        if not isinstance(id_combate, str): # si el id_combate no es una cadena de texto entonces lanza error
            raise WrongType("El id_combate de la nave debe ser un string")
        self.id_combate = id_combate
    
    def set_clave(self, clave:int):
        """Establece la clave de la nave, controlando que sea un número entero válido."""
        if not isinstance(clave, int):
            raise WrongType("La clave de la nave debe ser un número entero")
        self.clave = clave

    def get_id_combate(self):
        """Devuelve el ID de combate de la nave."""
        return self.id_combate
    
    def get_clave(self):
        """Devuelve la clave de la nave."""
        return self.clave

    def __str__(self):
        return f"ID Combate: {self.id_combate}"


#clases hijas según el tipo de nave
#clase Estacion espacial
class EstacionEspacial(Nave, UnidadCombate):
    """
    Representa uan estación espacial del imperio.
    Hereda de Nave y UnidadCombate, y añade atributos específicos como la tripulación, el pasaje y la localización de la estación espacial.
    Controla que los valores numéricos sean positivos y maneja errores en caso contrario.
    """

    def __init__(self, nombre, catalogo, id_combate, clave, tripulacion, pasaje, localizacion):
        Nave.__init__(self, nombre, catalogo) #Llamamos al constructor de Nave para inicializar los atributos comunes
        UnidadCombate.__init__(self, id_combate, clave) #Llamamos al constructor de UnidadCombate para inicializar los atributos de combate
        
        if not isinstance(tripulacion, int): 
            raise WrongType("La cantidad de tripulantes de la nave debe de ser un número entero")
        
        if not isinstance(pasaje, int): 
            raise WrongType("El pasaje de la nave debe ser un número entero")
        
        if not isinstance(localizacion, EUbicacion): 
            raise WrongType("La localización de la nave debe ser una de las ubicaiones posibles (EUbicacion)")
        
        if tripulacion < 0: 
            raise ValueError("Tripulación debe ser un número mayor que 0")
        
        if pasaje < 0:
            raise ValueError("El pasaje debe de ser un número mayor que 0")

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.localizacion = localizacion

    # setters y getters para controlar el acceso a los atributos y validar los datos

    def get_tripulacion(self):
        """Devuelve la cantidad de tripulantes de la estación espacial."""
        return self.tripulacion
    
    def get_pasaje(self):
        """Devuelve el pasaje de la estación espacial."""
        return self.pasaje
    
    def get_localizacion(self):
        """Devuelve la localización de la estación espacial."""
        return self.localizacion
    
    def set_tripulacion(self, tripulacion):
        """Establece la cantidad de tripulantes de la estación espacial, controlando que sea un número entero válido."""
        if not isinstance(tripulacion, int): 
            raise WrongType("La cantidad de tripulantes de la nave debe de ser un número entero")
        self.tripulacion = tripulacion

    def set_pasaje(self, pasaje):
        """Establece el pasaje de la estación espacial, controlando que sea un número entero válido."""
        if not isinstance(pasaje, int): 
            raise WrongType("El pasaje de la nave debe ser un número entero")
        self.pasaje = pasaje

    def set_localizacion(self, localizacion):
        """Establece la localización de la estación espacial, controlando que sea un valor válido del Enum EUbicacion."""
        if not isinstance(localizacion, EUbicacion): 
            raise WrongType("La localización de la nave debe ser una de las ubicaiones posibles (EUbicacion)")
        self.localizacion = localizacion

    def __str__(self):
        return f"EstacionEspacial({self.nombre}, Ubicación: {self.localizacion}, Tripulación:{self.tripulacion}, Pasaje:{self.pasaje})"


#clase Nave estelar
class NaveEstelar(Nave, UnidadCombate):
    """
    Representa una nave estelar con tipo de clase específico (Ejecutor, Eclipse o Soberano).
    Hereda de Nave y UnidadCombate, y añade atributos específicos como la tripulación, el pasaje y el tipo de clase de la nave estelar (Enum EClaseNave).
    Controla que los valores numéricos sean positivos y maneja errores en caso contrario.
    """

    def __init__(self, nombre, catalogo, id_combate, clave, tripulacion, pasaje, tipo_clase):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)

        if not isinstance(tripulacion, int): 
            raise WrongType("La cantidad de tripulantes de la nave debe de ser un número entero")
        
        if not isinstance(pasaje, int): 
            raise WrongType("El pasaje de la nave debe ser un número entero")
        
        if not isinstance(tipo_clase, EClaseNave): 
            raise WrongType("La clase de la nave debe ser una de las clases posibles (EClaseNave)")
        
        if tripulacion < 0: 
            raise ValueError("Tripulación debe ser un número mayor que 0")
        
        if pasaje < 0:
            raise ValueError("El pasaje debe de ser un número mayor que 0")

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.tipo_clase = tipo_clase
    
    # setters y getters para controlar el acceso a los atributos y validar los datos

    def get_tripulacion(self):
        """Devuelve la cantidad de tripulantes de la nave estelar."""
        return self.tripulacion
    
    def get_pasaje(self):
        """Devuelve el pasaje de la nave estelar."""
        return self.pasaje
    
    def get_tipo_clase(self):
        """Devuelve el tipo de clase de la nave estelar."""
        return self.tipo_clase
    
    def set_tripulacion(self, tripulacion):
        """Establece la cantidad de tripulantes de la nave estelar, controlando que sea un número entero válido."""
        if not isinstance(tripulacion, int): 
            raise WrongType("La cantidad de tripulantes de la nave debe de ser un número entero")
        if tripulacion < 0:
            raise TypeError("La tripulación debe ser un número mayor que 0")
        self.tripulacion = tripulacion

    def set_pasaje(self, pasaje):
        """Establece el pasaje de la nave estelar, controlando que sea un número entero válido."""
        if not isinstance(pasaje, int): 
            raise WrongType("El pasaje de la nave debe ser un número entero")
        if pasaje < 0:
            raise TypeError("El pasaje debe ser un número mayor que 0")
        self.pasaje = pasaje

    def set_tipo_clase(self, tipo_clase):
        """Establece el tipo de clase de la nave estelar, controlando que sea un valor válido del Enum EClaseNave."""
        if not isinstance(tipo_clase, EClaseNave): 
            raise WrongType("La clase de la nave debe ser una de las clases posibles (EClaseNave)")
        self.tipo_clase = tipo_clase

    def __str__(self):
        return f"NaveEstelar({self.nombre}, Clase:{self.tipo_clase}, Tripulación:{self.tripulacion})"


#clase Caza estelar
class CazaEstelar(Nave, UnidadCombate):
    """
    Representa una caza estelar con dotación específica.
    Hereda de Nave y UnidadCombate, y añade un atributo específico para la dotación de la caza estelar.
    Controla que la dotación sea un valor positivo y maneja errores en caso contrario.
    """

    def __init__(self, nombre, catalogo, id_combate, clave, dotacion):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)

        if not isinstance(dotacion, int):
            raise WrongType("La dotación de la nave debe ser in número entero")
        
        if dotacion < 0:
            raise ValueError("La dotación debe ser un número mayor que 0")

        self.dotacion = dotacion
    
    # setters y getters para controlar el acceso a los atributos y validar los datos

    def get_dotacion(self):
        """Devuelve la dotación de la caza estelar."""
        return self.dotacion
    
    def set_dotacion(self, dotacion):
        """Establece la dotación de la caza estelar, controlando que sea un número entero válido."""
        if not isinstance(dotacion, int):
            raise WrongType("La dotación debe ser un número entero")
        if dotacion < 0:
            raise TypeError("La dotación debe ser un número mayor que 0")
        self.dotacion = dotacion

    def __str__(self):
        return f"CazaEstelar({self.nombre}, Dotación:{self.dotacion})"


#clase Repuesto
class Repuesto:
    """
    Representa un repuesto disponible en el sistema, con atributos como el nombre del repuesto, el proveedor, la cantidad disponible y el precio.
    Permite consultar el stock y reducirlo al solicitar un repuesto con control de errores.
    """

    def __init__(self, nombre, proveedor, cantidad, precio):
        if not isinstance(nombre, str):
            raise WrongType("El nombre del repuesto debe ser un string")
        
        if not isinstance(proveedor, str):
            raise WrongType("El nombre del proveedor debe ser un string")
        
        if not isinstance(cantidad, int):
            raise WrongType("La cantidad de repuestos que hay debe ser un número entero")
        
        if not isinstance(precio, (int, float)):
            raise WrongType("El precio del repuesto debe ser un número")
        
        if cantidad < 0:
            raise TypeError("La cantidad de repuesto debe ser un número mayor que 0")
        
        if precio < 0:
            raise TypeError("El precio del repuesto debe ser un número mayor que 0")

        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad #atributo provado para proteger el stock del repuesto y controlar su acceso a través de métodos específicos
        self.precio = precio

    # setters y getters para controlar el acceso a los atributos y validar los datos

    def obtener_cantidad(self):
        """Devuelve la cantidad disponible del repuesto"""
        return self.__cantidad
    
    def get_nombre(self):
        """Devuelve el nombre del repuesto."""
        return self.nombre
    
    def get_proveedor(self):
        """Devuelve el nombre del proveedor."""
        return self.proveedor
    
    def get_precio(self):
        """Devuelve el precio del repuesto."""
        return self.precio
    
    def set_cantidad(self, cantidad):
        """Establece la cantidad disponible del repuesto, controlando que sea un número entero válido."""
        if not isinstance(cantidad, int):
            raise WrongType("La cantidad de repuestos que hay debe ser un número entero")
        if cantidad < 0:
            raise TypeError("La cantidad de repuesto debe ser un número mayor que 0")
        self.__cantidad = cantidad
    
    def set_nombre(self, nombre):
        """Establece el nombre del repuesto, controlando que sea un string válido."""
        if not isinstance(nombre, str):
            raise WrongType("El nombre del repuesto debe ser un string")
        self.nombre = nombre

    def set_proveedor(self, proveedor):
        """Establece el nombre del proveedor del repuesto, controlando que sea un string válido."""
        if not isinstance(proveedor, str):
            raise WrongType("El nombre del proveedor debe ser un string")
        self.proveedor = proveedor

    def set_precio(self, precio):
        """Establece el precio del repuesto, controlando que sea un número float válido."""
        if not isinstance(precio, float):
            raise WrongType("El precio del repuesto debe ser un float")
        if precio < 0:
            raise TypeError("El precio del repuesto debe ser un número mayor que 0")
        self.precio = precio
    
    # métodos de la clase Repuesto
    def reducir_stock(self, cantidad):
        """Reduce el stock del repuesto al solicitarlo, controlando que la cantidad solicitada no supere el stock disponible y manejando errores en caso contrario."""
        if cantidad <= 0:
            raise ValueError("Cantidad incorrecta")
        if cantidad > self.__cantidad:
            raise StockInsuficienteError("Stock insuficiente")
        self.__cantidad -= cantidad

    def __str__(self):
        return f"Repuesto({self.nombre}, Stock:{self.__cantidad}, Precio:{self.precio})"


#clase Almacen
class Almacen:
    """
    Representa un almacén del imperio que contiene un catálogo de repuestos disponibles.
    Permite añadir repuestos al almacén, buscar repuestos por nombre y verificar la existencia de stock para un repuesto específico.
    Controla errores en caso de objetos no válidos o repuestos duplicados.
    """

    def __init__(self, nombre, localizacion):
        if not isinstance(nombre, str):
            raise WrongType("El nombre del almacén debe ser un string")
        if not isinstance(localizacion, str):
            raise WrongType("La localización debe ser un string")
        
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = []
    
    # setters y getters para controlar el acceso a los atributos y validar los datos

    def set_nombre(self, nombre):
        """Establece el nombre del almacén, controlando que sea un string válido."""
        if not isinstance(nombre, str):
            raise WrongType("El nombre del almacén debe ser un string")
        self.nombre = nombre
    
    def set_localizacion(self, localizacion):
        """Establece la localización del almacén, controlando que sea un string válido."""
        if not isinstance(localizacion, str):
            raise WrongType("La localización debe ser un string")
        self.localizacion = localizacion

    def get_nombre(self):
        """Devuelve el nombre del almacén."""
        return self.nombre
    
    def get_localizacion(self):
        """Devuelve la localización del almacén."""
        return self.localizacion

    # métodos de la clase Almacen
    def anadir_repuesto(self, repuesto):
        """Añade un repuesto al ctálogo del almacén."""

        if not isinstance(repuesto, Repuesto): 
            raise TypeError("Objeto no válido")
        if self.buscar_repuesto(repuesto.nombre):
            raise ValueError(f"Repuesto '{repuesto.nombre}' ya existe en el almacén")
        self.catalogo.append(repuesto)

    def buscar_repuesto(self, nombre):
        """Buscar un repuesto por nombre en el catálogo del almacén y devolverlo si se encuentra, o None si no se encuentra."""

        for x in self.catalogo:
            if x.nombre == nombre:
                return x
        return None
    
    def existencia_stock(self, nombre, cantidad):
        """Devuelve True si el repuesto con el nombre especificado existe en el catálogo del almacén y tiene suficiente stock para la cantidad solicitada, o False en caso contrario."""

        r = self.buscar_repuesto(nombre)
        return r and r.obtener_cantidad() >= cantidad
    
    def __str__(self):
        return f"Almacen({self.nombre}, Ubicación: {self.localizacion})"


#clases tipos de usuarios (abstracta). No se puede instanciar directamente, solo a través de sus clases hijas (Comandante y Operario)
class Usuario(metaclass = ABCMeta):
    """
    Clase asbtracta que define el comportamiento común de los usuarios del sistema.
    Obliga a las clases hijas a implementar el método usar_sistema, que representa la acción principal que cada tipo de usuario realiza en el sistema.
    """

    def __init__(self, nombre):
        self.nombre = nombre
    
    @abstractmethod
    def usar_sistema(self):
        pass

class Comandante(Usuario):
    """
    Representa a un comandante del imperio que puede solicitar repuestos para las naves.
    Interactúa con MiImperio para solicitar repuestos, controlando errores en caso de cantidades incorrectas o repuestos no encontrados.
    """

    def usar_sistema(self):
        print("Solicitando repuesto...")
    
    def solicitar_repuesto(self, sistema, nombre, cantidad):
        """Solicita un repuesto al sistema."""

        return sistema.solicitar_repuesto(nombre, cantidad)
    
    def __str__(self):
        return f"Comandante {self.nombre}"

class Operario(Usuario):
    """Representa a un operario del imperio que puede gestionar los almacenes y añadir repuestos al sistema."""

    def usar_sistema(self):
        print("Gestionando almacén")

    def anadir_repuesto(self, almacen, repuesto):
        """Añade un repuesto a un almacén."""
        almacen.anadir_repuesto(repuesto)

    def __str__(self):
        return f"Operario {self.nombre}"

#Clase MiImperio (sistema principal):
class MiImperio:
    """
    Clase principal del sistema que representa el imperio y gestiona los almacenes y las naves.
    Permite agregar almacenes y naves al sistema, y manejar las solicitudes de repuestos por parte de los comandantes, controlando errores en caso de cantidades incorrectas o repuestos no encontrados.
    """

    def __init__(self):
        self.almacenes = []
        self.naves = []

    def agregar_almacen(self, almacen):
        """Agrega un almacén al sistema"""

        if not isinstance(almacen, Almacen):
            raise TypeError("Almacen no válido")
        self.almacenes.append(almacen)

    def agregar_nave(self, nave):
        """Agrega una nave al sistema"""

        if not isinstance(nave, Nave):
            raise TypeError("Nave no válida")
        self.naves.append(nave)

    def solicitar_repuesto(self, nombre, cantidad):
        """Permite a un comandante solicitar un repuesto al sistema."""

        if cantidad <= 0:
            raise ValueError("Cantidad incorrecta")
        
        for almacen in self.almacenes: #recorremos todos los almacenes para encontrar el repuesto solicitado
            repuesto = almacen.buscar_repuesto(nombre)
            if repuesto:
                repuesto.reducir_stock(cantidad)
                return repuesto
        raise RepuestoNoEncontradoError(f"Respuesto '{nombre}' no ha sido encontrado")
    
    def __str__(self):
        return f"MiImperio(Almacenes:{len(self.almacenes)}, Naves:{len(self.naves)})"

#Menú para interfaz de usuario
def pedir_entero(mensaje):
    """Función auxiliar para pedir un número entero al usuario, controlando errores de entrada."""
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")
def menu():
    """
    Implementa una interfaz de usuario por consola.
    Permite interactuar con el sistema a través de un menú que ofrece las siguientes opciones:
    1) Añadir repuesto al almacén (Operario)
    2) Solicitar repuesto (Comandante)
    3) Ver estado de los almacenes
    4) Crear nuevo almacén
    5) Salir
    """

    sistema = MiImperio()
    print(f"\nBienvenido al sistema de gestión de repuestos del Imperio Galáctico")
    nombre_usuario = input(f"Introduzca su nombre: ")
    comandante = Comandante(nombre_usuario)
    operario = Operario("Administrador")
    
    # Almacén inicial para la demostración, se puede eliminar o modificar según se desee
    a1 = Almacen("Almacen principal", "Endor")
    sistema.agregar_almacen(a1)

    while True: #bucle para mostrar el menú de forma continua hasta que el usuario decida salir
        print(f"\n")
        print(f"\n---Menú principal---")
        print()
        print(f"1) Añadir repuesto al almacén (Operario)")
        print(f"2) Solicitar repuesto (Comandante)")
        print(f"3) Ver estado de los almacenes")
        print(f"4) Crear nuevo almacén")
        print(f"5) Salir")
        
        opcion = input(f"Bienvenido {comandante.nombre}, elige una opción: ")

        if opcion == "1":
            try:
                print("\n Almacenes disponibles:")
                for i, almacen in enumerate(sistema.almacenes):
                    print(f"{i+1}) {almacen.get_nombre()} - Ubicación: {almacen.get_localizacion()}")

                idx = pedir_entero(f"Selecciona el número del almacén al que deseas añadir el repuesto: ") - 1
                almacen_seleccionado = sistema.almacenes[idx]

                nombre = input("Nombre del repuesto: ")
                proveedor = input(f"Proveedor: ")
                cantidad = pedir_entero(f"Cantidad: ")  
                precio = float(input(f"Precio: "))

                rep = Repuesto(nombre, proveedor, cantidad, precio)
                operario.anadir_repuesto(almacen_seleccionado, rep)

                print(f"Repuesto '{nombre}' añadido al almacén '{almacen_seleccionado.get_nombre()}' correctamente")
            
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "2":
            try:
                print(f"\nRepuestos disponibles:")
                for almacen in sistema.almacenes:
                    print(f"\nAlmacén: {almacen.get_nombre()}, Ubicación: {almacen.get_localizacion()}")
                    for rep in almacen.catalogo:
                        print(f"- {rep.get_nombre()}")

                nombre = input("Nombre del repuesto: ")
                cantidad = pedir_entero(f"Cantidad: ")

                rep = comandante.solicitar_repuesto(sistema, nombre, cantidad)
                print(f"Repuesto '{nombre}' solicitado correctamente. Stock restante: {rep.obtener_cantidad()}")
            
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "3":
            for almacen in sistema.almacenes:
                print(f"\nAlmacén: {almacen.nombre}, Ubicación: {almacen.localizacion}")
                for repuesto in almacen.catalogo:
                    print(f"- {repuesto}")
        
        elif opcion == "4":
            try:
                nombre = input("Nombre del almacén: ")
                localizacion = input(f"Ubicación: ")
                nuevo_almacen = Almacen(nombre, localizacion)

                sistema.agregar_almacen(nuevo_almacen)
                print(f"Almacén '{nombre}' creado correctamente")
            
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "5":
            print(f"Saliendo del sistema. Hasta pronto {comandante.nombre}!")
            break
        else:
            print(f"Opción no valida. Por favor, elige una opción del menú")

#demostración
def demo():
    """
    Función de demostración que muestra el funcionamiento del sistema a través de una serie de acciones predefinidas.
    Crea objetos de ejemplo y simula distintas operaciones, incluyendo casos correctos y manejo de errrores.
    """

    #creación de usuarios
    comandante = Comandante("Sánchez")
    operario = Operario("Vader")

    #creación de respuestos
    r1 = Repuesto("Motor", "Proveedor1", 20, 700.0)
    r2 = Repuesto("Ala", "Proveedor2", 5, 300.5)
    r3 = Repuesto("Escudo", "Proveedor3", 10, 600.0)
    r4 = Repuesto("Turbina", "Proveedor4", 2, 2000.3)

    print(f"\nRepuestos creados:")
    for rep in [r1, r2, r3, r4]:
        print(f"- {rep}")
    
    #creación de almacenes
    a1 = Almacen("Almacen1", "Cumulos_Raimos")
    operario.anadir_repuesto(a1, r1)
    operario.anadir_repuesto(a1, r2)
    operario.anadir_repuesto(a1, r3)

    print(f"\nEstado del almacén '{a1.nombre}' después de añadir repuestos:")
    for rep in a1.catalogo:
        print(f"- {rep}")

    #creación de segundo almacén
    a2 = Almacen("Almacen2", "Nebulosa_Kaliida")
    operario.anadir_repuesto(a2, r4)  

    print(f"\nEstado del almacén '{a2.nombre}' después de añadir repuestos:")
    for rep in a2.catalogo:
        print(f"- {rep}")

    #creación de naves
    nave1 = EstacionEspacial("Luna", ["Motor", "Ala"], "Id1", 1111, 50, 2, EUbicacion.ENDOR)
    nave2= NaveEstelar("Pleiades", ["Motor"], "Id2", 2222, 20, 5, EClaseNave.EJECUTOR)
    nave3 = CazaEstelar("Athena", ["Motor"], "Id3", 3333, 1)

    sistema = MiImperio()
    sistema.agregar_almacen(a1)
    sistema.agregar_almacen(a2)
    sistema.agregar_nave(nave1)
    sistema.agregar_nave(nave2)
    sistema.agregar_nave(nave3)

    print(f"\n----Estado inicial del sistema:----")
    print(sistema)
    for nave in sistema.naves:
        print(f"- {nave}")
    
    #comandante solicita repuestos correctamente
    print(f"\nComandante solicita 3 Motores y 2 Alas")
    try:
        rep1 = comandante.solicitar_repuesto(sistema, "Motor", 3)
        rep2 = comandante.solicitar_repuesto(sistema, "Ala", 2)
        print(f"Repuesto solicitado: {rep1}")
        print(f"Repuesto solicitado: {rep2}")
    except (StockInsuficienteError, RepuestoNoEncontradoError, ValueError) as e: #para decir que este tipo de excepciones se manejan de la misma forma
        print(f"Error: {e}")

    
    #Comandante solicita un repuesto que solo está en el segundo almacén
    print(f"\nSolicitando un repuesto que solo está disponible en el 2º almacén:")
    try:
        rep_turbina = comandante.solicitar_repuesto(sistema, "Turbina", 1)
        print(f"Repuesto solicitado: {rep_turbina}")
    except (StockInsuficienteError, RepuestoNoEncontradoError) as e:
        print(f"Error: {e}")

    #manejamos errores
    #Pedir mas repuestos de los que hay
    print(f"\nPidiendo más repuestos de los que hay")
    try:
        rep3 = comandante.solicitar_repuesto(sistema, "Ala", 10) 
        print(f"Repuesto solicitado: {rep3}")
    except StockInsuficienteError as e:
        print(f"Error: {e}")

    #Probar un repuesto que no existe
    print(f"\nProbando un repuesto que no existe")
    try:
        rep4 = comandante.solicitar_repuesto(sistema, "Láser", 1)
        print(f"Repuesto solicitado: {rep4}")
    except RepuestoNoEncontradoError as e:
        print(f"Error: {e}")

    #Mostrar estado de los almacenes
    for almacen in sistema.almacenes:
        print(f"\nAlmacén: {almacen.nombre}, Ubicación: {almacen.localizacion}")
        for repuesto in almacen.catalogo:
            print(f"- {repuesto}")

    # Mostrar estado final de las naves
    print(f"\nEstado final de las naves:")
    for nave in sistema.naves:
        print(f"- {nave}")


#programa principal
if __name__ == "__main__":
    demo()
    menu()