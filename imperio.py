

from abc import ABCMeta, abstractmethod
from enum import Enum

#creamos una clase excepcion 
class StockInsuficienteError(Exception):
    pass

#class RepuestoNoEncontradoError(Exception):
#    pass

class EUbicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class EClaseNave(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

#clase padre Nave 
class Nave:
    def __init__(self, nombre, catalogo):
        self.nombre = nombre
        self.catalogo = catalogo

    def usar_repuesto(self, nombre):
        return nombre in self.catalogo
    
    def __str__(self):
        return f"Nave: {self.nombre}, \nCatalogo: {self.catalogo}"
    

#clase Unidad de combate
class UnidadCombate:
    def __init__(self, id_combate, clave):
        self.id_combate = id_combate
        self.clave = clave

    def __str__(self):
        return f"ID Combate: {self.id_combate}"


#clases hijas según el tipo de nave
#clase Estacion espacial
class EstacionEspacial(Nave, UnidadCombate):
    def __init__(self, nombre, catalogo, id_combate, clave, tripulacion, pasaje, localizacion):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)

        if tripulacion < 0 or pasaje < 0: 
            raise ValueError("Valores incorrectos")

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.localizacion = localizacion

    def __str__(self):
        return f"EstacionEspacial({self.nombre}, Ubicación: {self.localizacion}, Tripulación:{self.tripulacion}, Pasaje:{self.pasaje})"


#clase Nave estelar
class NaveEstelar(Nave, UnidadCombate):
    def __init__(self, nombre, catalogo, id_combate, clave, tripulacion, pasaje, tipo_clase):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)

        if tripulacion < 0 or pasaje < 0:
            raise ValueError("Valores incorrectos")

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.tipo_clase = tipo_clase

    def __str__(self):
        return f"NaveEstelar({self.nombre}, Clase:{self.tipo_clase}, Tripulación:{self.tripulacion})"


#clase Caza estelar
class CazaEstelar(Nave, UnidadCombate):
    def __init__(self, nombre, catalogo, id_combate, clave, dotacion):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)

        if dotacion < 0:
            raise ValueError("Dotación icnorrecta")
        
        self.dotacion = dotacion

    def __str__(self):
        return f"CazaEstelar({self.nombre}, Dotación:{self.dotacion})"


#clase Repuesto
class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):
        if cantidad < 0 or precio < 0:
            raise ValueError("Valores incorrectos ")
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio

    def obtener_cantidad(self):
        return self.__cantidad
    
    def reducir_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad incorrecta")
        if cantidad > self.__cantidad:
            raise StockInsuficienteError("Stock insuficiente")
        self.__cantidad -= cantidad

    def __str__(self):
        return f"Repuesto({self.nombre}, Stock:{self.__cantidad}, Precio:{self.precio})"


#clase Almacen
class Almacen:
    def __init__(self, nombre, localizacion):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = []

    def anadir_repuesto(self, repuesto):
        if not isinstance(repuesto, Repuesto): 
            raise TypeError("Objeto no válido")
        self.catalogo.append(repuesto)

    def buscar_repuesto(self, nombre):
        for x in self.catalogo:
            if x.nombre == nombre:
                return x
        return None
    
    def existencia_stock(self, nombre, cantidad):
        r = self.buscar_repuesto(nombre)
        return r and r.obtener_cantidad() >= cantidad
    
    def __str__(self):
        return f"Almacen({self.nombre}, Ubicación: {self.localizacion})"


#clases tipos de usuarios (abstracta)
class Usuario(mataclass=ABCMeta):
    def __init__(self, nombre):
        self.nombre = nombre
    
    @abstractmethod
    def usar_sistema(self):
        pass

class Comandante(Usuario):
    def usar_sistema(self):
        print("Solicitando repuesto")
    
    def solicitar_repuesto(self, sistema, nombre, cantidad):
        return sistema.solicitar_repuesto(nombre, cantidad)
    
    def __str__(self):
        return f"Comandante {self.nombre}"

class Operario(Usuario):
    def usar_sistema(self):
        print("Geestionando almacén")

    def anadir_repuesto(self, almacen, repuesto):
        almacen.anadir_repuesto(repuesto)

    def __str__(self):
        return f"Operario {self.nombre}"

#Clase MiImperio (sistema principal):
class MiImperio:
    def __init__(self):
        self.almacenes = []
        self.naves = []

    def agregar_almacen(self, almacen):
        if not isinstance(almacen, Almacen):
            raise TypeError("Almacen no válido")
        self.almacenes.append(almacen)

    def agregar_nave(self, nave):
        if not isinstance(nave, Nave):
            raise TypeError("Nave no válida")
        self.naves.append(nave)

    def solicitar_repuesto(self, nombre, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad incorrecta")
        
        for almacen in self.almacenes:
            repuesto = almacen.buscar_repuesto(nombre)
            if repuesto:
                repuesto.reducir_stock(cantidad)
                return repuesto
        raise LookupError(f"Respuesto '{repuesto}' no ha sido encontrado") #BUSCAR LOOKUPERROR
    
    def __str__(self):
        return f"MiImperio(Almacenes:{len(self.almacenes)}, Naves:{len(self.naves)})"


