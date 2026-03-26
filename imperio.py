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
class Usuario(metaclass = ABCMeta):
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
        raise LookupError(f"Respuesto '{nombre}' no ha sido encontrado")
    
    def __str__(self):
        return f"MiImperio(Almacenes:{len(self.almacenes)}, Naves:{len(self.naves)})"

#demostración
def demo():
    #creación de usuarios
    comandante = Comandante("Sánchez")
    operario = Operario("Vader")

    #creación de respuestos
    r1 = Repuesto("Motor", "Proveedor1", 20, 700)
    r2 = Repuesto("Ala", "Proveedor2", 5, 300)
    r3 = Repuesto("Escudo", "Proveedor3", 10, 600)
    r4 = Repuesto("Turbina", "Proveedor4", 2, 2000)

    print(f"\nRepuestos creados:")
    for rep in [r1, r2, r3, r4]:
        print(f"{rep}")
    
    #creación de almacenes
    a1 = Almacen("Almacen1", "Cumulos_Raimos")
    operario.anadir_repuesto(a1, r1)
    operario.anadir_repuesto(a1, r2)
    operario.anadir_repuesto(a1, r3)

    print(f"\nEstado del almacén '{a1.nombre}' después de añadir repuestos:")
    for rep in a1.catalogo:
        print(f"{rep}")

    #creación de segundo almacén
    a2 = Almacen("Almacen2", "Nebulosa_Kaliida")
    operario.anadir_repuesto(a2, r4)  

    print(f"\nEstado del almacén '{a2.nombre}' después de añadir repuestos:")
    for rep in a2.catalogo:
        print(f"{rep}")

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
        print(f"{nave}")

    
    #comandante solicita repuestos correctamente
    print(f"\nComandante solicita 3 Motores y 2 Alas")
    try:
        rep1 = comandante.solicitar_repuesto(sistema, "Motor", 3)
        rep2 = comandante.solicitar_repuesto(sistema, "Ala", 2)
        print(f"Repuesto solicitado: {rep1}")
        print(f"Repuesto solicitado: {rep2}")
    except (StockInsuficienteError, LookupError, ValueError) as e: #para decir que este tipo de excepciones se manejan de la misma forma
        print(f"Error: {e}")

    
    #Comandante solicita un repuesto que solo está en el segundo almacén
    print(f"\nSolicitando un repuesto que solo está disponible en el 2º almacén:")
    try:
        rep_turbina = comandante.solicitar_repuesto(sistema, "Turbina", 1)
        print(f"Repuesto solicitado: {rep_turbina}")
    except (StockInsuficienteError, LookupError) as e:
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
    except LookupError as e:
        print(f"Error: {e}")

    #Mostrar estado final del almacén
    print(f"\nEstado final del almacén 1:")
    for repuesto in a1.catalogo:
        print(f"{repuesto}")

    print(f"\nEstado final del almacén 2:")
    for repuesto in a2.catalogo:
        print(f"{repuesto}")

    # Mostrar estado final de las naves
    print(f"\nEstado final de las naves:")
    for nave in sistema.naves:
        print(f"{nave}")


#programa principal
if __name__ == "__main__":
    demo()