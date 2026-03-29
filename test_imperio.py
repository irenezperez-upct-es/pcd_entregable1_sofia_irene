import pytest
from imperio import *
from excepciones import StockInsuficienteError, RepuestoNoEncontradoError, WrongType

# -------------------------------------------------
# FIXTURES
# Los fixtures crean objetos reutilizables para los tests.
# Pytest los ejecuta automáticamente antes de cada prueba que los necesite.
# Esto evita duplicar código y garantiza un entorno controlado.
# -------------------------------------------------

@pytest.fixture
def repuesto_motor():
    """ Repuesto válido con stock suficiente para las pruebas """
    return Repuesto(nombre="Motor Aéreo", proveedor="Lion", cantidad=10, precio=5000.0)

@pytest.fixture
def repuesto_laser():
    """ Repuesto válido con stock suficiente para las pruebas """
    return Repuesto(nombre="Cañón Láser", proveedor="Laselir", cantidad=5, precio=2000.0)

@pytest.fixture
def almacen_central(repuesto_motor, repuesto_laser):
    """ Almacén con algunos repuestos para las pruebas del sistema """
    a = Almacen(nombre="Central", localizacion="Cúmulo Raimos")
    a.anadir_repuesto(repuesto_motor)
    a.anadir_repuesto(repuesto_laser)
    return a

@pytest.fixture
def imperio(almacen_central):
    """ MiImperio con un almacén para las pruebas del sistema """
    imp = MiImperio()
    imp.agregar_almacen(almacen_central)
    return imp

@pytest.fixture
def nave_estelar():
    """ Nave estelar válida para las pruebas de instanciación y sistema """
    return NaveEstelar(
        nombre="Halcón Imperial",
        catalogo=["Motor Aéreo", "Cañón Láser"],
        id_combate="A1",
        clave=101,
        tripulacion=35000,
        pasaje=5000,
        tipo_clase=EClaseNave.EJECUTOR
    )

@pytest.fixture
def estacion_espacial():
    """ Estación espacial válida para las pruebas de instanciación y sistema """
    return EstacionEspacial(
        nombre="Estrella de la Muerte",
        catalogo=["Motor Iónico"],
        id_combate="B45",
        clave=102,
        tripulacion=5000,
        pasaje=2000,
        localizacion=EUbicacion.ENDOR
    )

@pytest.fixture
def caza():
    """ Caza estelar válido para las pruebas de instanciación y sistema """
    return CazaEstelar(
        nombre="Rocket",
        catalogo=["Cañón Láser"],
        id_combate="C21",
        clave=103,
        dotacion=1
    )

@pytest.fixture
def almacen_vacio():
    """ Almacén vacío para pruebas de adición de repuestos """
    return Almacen("Central", "Endor")

@pytest.fixture
def repuesto_valido():
    """ Repuesto válido para pruebas de adición al almacén """
    return Repuesto("Motor Aéreo", "Lion", 10, 5000.0)


# -------------------------------------------------
# TESTS DE INSTANCIACIÓN
# -------------------------------------------------

def test_crear_repuesto(repuesto_motor):
    """Test de creación de un repuesto con datos válidos."""
    assert repuesto_motor.nombre == "Motor Aéreo"
    assert repuesto_motor.obtener_cantidad() == 10

def test_crear_almacen(almacen_central):
    """Test de creación de un almacén con datos válidos."""
    assert len(almacen_central.catalogo) == 2

def test_crear_nave_estelar(nave_estelar):
    """Test de creación de una nave estelar con datos válidos."""
    assert nave_estelar.tipo_clase == EClaseNave.EJECUTOR

def test_crear_estacion(estacion_espacial):
    """Test de creación de una estación espacial con datos válidos."""
    assert estacion_espacial.localizacion == EUbicacion.ENDOR

def test_crear_caza(caza):
    """Test de creación de un caza estelar con datos válidos."""
    assert caza.dotacion == 1


# -------------------------------------------------
# TESTS DE STOCK (REPUESTO)
# -------------------------------------------------

def test_reducir_stock_correcto(repuesto_motor):
    """Test de reducción de stock con cantidad válida."""
    repuesto_motor.reducir_stock(3)
    assert repuesto_motor.obtener_cantidad() == 7

def test_reducir_stock_insuficiente(repuesto_motor):
    """Test de reducción de stock con cantidad mayor al disponible,
        debe lanzar StockInsuficienteError."""
    with pytest.raises(StockInsuficienteError):
        repuesto_motor.reducir_stock(50)

def test_reducir_stock_incorrecto(repuesto_motor):
    """Test de reducción de stock con cantidad incorrecta, 
        debe lanzar ValueError."""
    with pytest.raises(ValueError):
        repuesto_motor.reducir_stock(-2)


# -------------------------------------------------
# TESTS DE ALMACÉN
# -------------------------------------------------

def test_anadir_repuesto_correcto(almacen_vacio, repuesto_valido):
    """Test de adición de un repuesto válido al almacén vacío."""
    almacen_vacio.anadir_repuesto(repuesto_valido)
    assert len(almacen_vacio.catalogo) == 1
    assert almacen_vacio.catalogo[0] == repuesto_valido

def test_anadir_repuesto_incorrecto(almacen_vacio):
    """Test de adición de un objeto no repuesto al almacén,
        debe lanzar TypeError."""
    with pytest.raises(TypeError):
        almacen_vacio.anadir_repuesto("no es un repuesto")

def test_anadir_repuesto_duplicado(almacen_central, repuesto_motor):
    """Test de adición de un repuesto que ya existe en el almacén,
        debe lanzar ValueError."""
    with pytest.raises(ValueError):
        almacen_central.anadir_repuesto(repuesto_motor)

def test_buscar_repuesto_existente(almacen_central):
    """Test de búsqueda de un repuesto que existe en el almacén."""
    r = almacen_central.buscar_repuesto("Motor Aéreo")
    assert r is not None

def test_buscar_repuesto_inexistente(almacen_central):
    """Test de búsqueda de un repuesto que no existe en el almacén."""
    r = almacen_central.buscar_repuesto("Motor Acelerador")
    assert r is None

def test_existencia_stock_existente(almacen_central):
    """Test de verificación de existencia de stock para un repuesto con cantidad suficiente."""
    assert almacen_central.existencia_stock("Motor Aéreo", 5)

def test_existencia_stock_insuficiente(almacen_central):
    """Test de verificación de existencia de stock para un repuesto con cantidad insuficiente."""
    assert not almacen_central.existencia_stock("Motor Aéreo", 999)


# -------------------------------------------------
# TESTS DEL SISTEMA MIIMPERIO
# -------------------------------------------------

def test_solicitar_repuesto_correcto(imperio):
    """Test de solicitud de un repuesto con cantidad válida, debe reducir 
        el stock correctamente."""
    rep = imperio.solicitar_repuesto("Motor Aéreo", 2)
    assert rep.obtener_cantidad() == 8

def test_solicitar_repuesto_inexistente(imperio):
    """Test de solicitud de un repuesto que no existe en el sistema, 
        debe lanzar RepuestoNoEncontradoError."""
    with pytest.raises(RepuestoNoEncontradoError):
        imperio.solicitar_repuesto("Hiperimpulsor", 1)

def test_solicitar_repuesto_cantidad_incorrecta(imperio):
    """Test de solicitud de un repuesto con cantidad negativa, 
        debe lanzar ValueError."""
    with pytest.raises(ValueError):
        imperio.solicitar_repuesto("Motor Aéreo", -5)


# -------------------------------------------------
# TESTS DE VALIDACIÓN DE ENUMS Y TIPOS
# -------------------------------------------------

def test_estacion_localizacion_incorrecta():
    """Test de creación de una estación espacial con localización no válida, 
        debe lanzar WrongType."""
    with pytest.raises(WrongType):
        EstacionEspacial("X", [], "ID", 1, 10, 10, "No enum")

def test_nave_estelar_clase_incorrecta():
    """Test de creación de una nave estelar con clase no válida, 
        debe lanzar WrongType."""
    with pytest.raises(WrongType):
        NaveEstelar("Nave", [], "ID", 1, 10, 10, "Clase inválida")
