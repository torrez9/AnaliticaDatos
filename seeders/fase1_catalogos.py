import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faker import Faker
from config.db import get_connection
import time, random

fake = Faker(['es_MX', 'es'])

# ── Helper base ────────────────────────────────────────────────────────────
def _exec(sql: str, data: list, label: str) -> None:
    """Ejecuta un INSERT múltiple con manejo de errores centralizado."""
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, data)
        conn.commit()
        print(f"    {label:<40} {len(data):>5} registros")
    except Exception as e:
        conn.rollback()
        print(f"    ERROR  {label}: {e}")
    finally:
        cursor.close()
        conn.close()

def _exec_timed(sql: str, data: list, label: str, start: float) -> None:
    """Igual que _exec pero muestra el tiempo transcurrido."""
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, data)
        conn.commit()
        elapsed = time.time() - start
        print(f"    {label:<40} {len(data):>5} registros  {elapsed:.2f}s")
    except Exception as e:
        conn.rollback()
        print(f"    ERROR  {label}: {e}")
    finally:
        cursor.close()
        conn.close()

# ── Seeders ────────────────────────────────────────────────────────────────
def seed_rols() -> None:
    roles = [
        ("Administrador", "Control total del sistema"),
        ("Vendedor",       "Gestion de ventas y facturas"),
        ("Bodeguero",      "Control de inventario y bodegas"),
        ("Cajero",         "Gestion de pagos y cobros"),
        ("Gerente",        "Supervision general de sucursales"),
    ]
    _exec(
        "INSERT IGNORE INTO rols (nombre, descripcion, created_at, updated_at) "
        "VALUES (%s,%s,NOW(),NOW())",
        roles, "rols"
    )


def seed_sucursals() -> None:
    data = [
        ("Sucursal Central", "Calle Principal #1, Ciudad Dario",  "Carlos Lopez"),
        ("Sucursal Norte",   "Barrio El Carmen, Matagalpa",        "Maria Garcia"),
        ("Sucursal Sur",     "Bo. San Antonio, Managua",           "Jose Martinez"),
        ("Sucursal Este",    "Mercado Oriental, Managua",          "Ana Rodriguez"),
        ("Sucursal Oeste",   "Bo. Las Brisas, Leon",               "Luis Perez"),
    ]
    _exec(
        "INSERT IGNORE INTO sucursals "
        "(Nombre_Sucursal, Direccion, Gerente, created_at, updated_at) "
        "VALUES (%s,%s,%s,NOW(),NOW())",
        data, "sucursals"
    )


def seed_categorias() -> None:
    data = [
        ("Herramientas Manuales",),      ("Herramientas Electricas",),
        ("Materiales de Construccion",), ("Plomeria y Fontaneria",),
        ("Electricidad",),               ("Pintura y Acabados",),
        ("Tornilleria y Fijaciones",),   ("Seguridad Industrial",),
        ("Jardin y Exteriores",),        ("Ferreteria General",),
    ]
    _exec(
        "INSERT IGNORE INTO categorias (Nombre_cat, created_at, updated_at) "
        "VALUES (%s,NOW(),NOW())",
        data, "categorias"
    )


def seed_unidadmedidas() -> None:
    data = [
        ("Unidad",), ("Metro",),    ("Kilogramo",), ("Litro",),
        ("Caja",),   ("Rollo",),    ("Par",),        ("Bolsa",),
    ]
    _exec(
        "INSERT IGNORE INTO unidadmedidas (Nombre_Medida, created_at, updated_at) "
        "VALUES (%s,NOW(),NOW())",
        data, "unidadmedidas"
    )


def seed_tipo_pagos() -> None:
    data = [
        ("Efectivo",),
        ("Tarjeta de Credito",),
        ("Tarjeta de Debito",),
        ("Transferencia Bancaria",),
        ("Credito",),
    ]
    _exec(
        "INSERT IGNORE INTO tipo_pagos (Nombre_pago, created_at, updated_at) "
        "VALUES (%s,NOW(),NOW())",
        data, "tipo_pagos"
    )


def seed_tipo_entregas() -> None:
    data = [
        ("Entrega en tienda",),
        ("Entrega a domicilio",),
        ("Retiro en bodega",),
    ]
    _exec(
        "INSERT IGNORE INTO tipo_entregas (Descripcion, created_at, updated_at) "
        "VALUES (%s,NOW(),NOW())",
        data, "tipo_entregas"
    )


def seed_proveedors(total: int = 30) -> None:
    start = time.time()
    data  = [
        (
            fake.company(),
            fake.phone_number()[:15],
            fake.address()[:100],
            fake.unique.company_email(),
        )
        for _ in range(total)
    ]
    _exec_timed(
        "INSERT INTO proveedors "
        "(Razon_social, Telefono, Direccion, Correo, created_at, updated_at) "
        "VALUES (%s,%s,%s,%s,NOW(),NOW())",
        data, "proveedors", start
    )


def seed_clientes(total: int = 200) -> None:
    start = time.time()
    data  = []
    for _ in range(total):
        limite = round(random.uniform(1000, 50000), 2)
        data.append((
            fake.bothify("###-######-####X"),
            fake.first_name(),
            fake.last_name(),
            fake.phone_number()[:15],
            fake.unique.email(),
            limite,
            round(random.uniform(0, limite), 2),
        ))
    _exec_timed(
        "INSERT INTO clientes "
        "(Cedula, Nombre, Apellido, Telefono, Correo, "
        " Limitecredito, Saldocredito, created_at, updated_at) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())",
        data, "clientes", start
    )


def seed_kits() -> None:
    nombres = [
        "Kit Plomeria Basica",         "Kit Electricidad Residencial",
        "Kit Pintura Interior",        "Kit Construccion Liviana",
        "Kit Jardineria Completo",     "Kit Herramientas Basicas",
        "Kit Tornilleria Completa",    "Kit Seguridad Industrial",
        "Kit Soldadura Basica",        "Kit Acabados Premium",
        "Kit Reparacion Rapida",       "Kit Instalacion Electrica",
        "Kit Fontaneria Avanzada",     "Kit Carpinteria",
        "Kit Albanileria Profesional", "Kit Techado Residencial",
        "Kit Mantenimiento General",   "Kit Perforacion",
        "Kit Medicion y Trazado",      "Kit Organizacion Taller",
    ]
    data = [(n, round(random.uniform(100, 2000), 2), "Activo") for n in nombres]
    _exec(
        "INSERT INTO kits (Nombre_kit, Precio_kit, Estado, created_at, updated_at) "
        "VALUES (%s,%s,%s,NOW(),NOW())",
        data, "kits"
    )