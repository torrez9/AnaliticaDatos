import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faker import Faker
from config.db import get_connection
import bcrypt, time, random

fake = Faker(['es_MX', 'es'])

# ── Helper base ────────────────────────────────────────────────────────────
def _exec(sql: str, data: list, label: str) -> None:
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
def seed_users(total: int = 1000) -> None:
    start  = time.time()

    # Hash único calculado una sola vez — todos comparten la misma clave base
    pw     = bcrypt.hashpw(b"Password123!", bcrypt.gensalt()).decode()
    estados = ["Activo", "Activo", "Activo", "Inactivo"]

    data = []
    for _ in range(total):
        data.append((
            fake.first_name(),
            fake.last_name(),
            fake.unique.user_name(),
            fake.unique.email(),
            None,                                   # email_verified_at
            pw,
            random.choice(estados),
            fake.phone_number()[:15],
            None,                                   # foto_perfil
            random.randint(1, 5),                   # Idrol
            round(random.uniform(0, 15), 2),        # Comision %
        ))

    _exec_timed(
        """INSERT INTO users
           (name, Apellido, Usuario, email, email_verified_at, password,
            Estado, Telefono, foto_perfil, Idrol, Comision,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "users", start
    )


def seed_bodegas() -> None:
    # 2 bodegas por cada una de las 5 sucursales = 10 bodegas
    data = []
    for suc_id in range(1, 6):
        data.append((f"Bodega Principal  S{suc_id}", f"Area principal  sucursal {suc_id}", suc_id))
        data.append((f"Bodega Secundaria S{suc_id}", f"Area secundaria sucursal {suc_id}", suc_id))

    _exec(
        "INSERT INTO bodegas "
        "(Nombre_bodega, Direccion, Idsucursal, created_at, updated_at) "
        "VALUES (%s,%s,%s,NOW(),NOW())",
        data, "bodegas"
    )


def seed_subcategorias() -> None:
    # 3 subcategorias por cada una de las 10 categorias = 30 subcategorias
    mapa = {
        1:  ["Martillos y Mazas",            "Destornilladores",               "Llaves y Alicates"],
        2:  ["Taladros",                     "Pulidoras",                      "Sierras Electricas"],
        3:  ["Cemento y Mezclas",            "Bloques y Ladrillos",            "Arena y Grava"],
        4:  ["Tuberias PVC",                 "Llaves y Grifos",                "Accesorios de Tuberia"],
        5:  ["Cables y Conductores",         "Interruptores y Tomacorrientes", "Luminarias"],
        6:  ["Pintura de Interior",          "Pintura de Exterior",            "Selladores y Primers"],
        7:  ["Tornillos y Pernos",           "Tuercas y Arandelas",            "Anclajes y Tacos"],
        8:  ["Equipos de Proteccion",        "Senalizacion",                   "Guantes y Calzado"],
        9:  ["Herramientas de Jardin",       "Mangueras y Aspersores",         "Macetas y Sustratos"],
        10: ["Adhesivos y Sellantes",        "Cadenas y Candados",             "Accesorios Varios"],
    }
    data = [
        (cat_id, nombre)
        for cat_id, subs in mapa.items()
        for nombre in subs
    ]

    _exec(
        "INSERT IGNORE INTO subcategorias "
        "(Idcategoria, Nombre_subcat, created_at, updated_at) "
        "VALUES (%s,%s,NOW(),NOW())",
        data, "subcategorias"
    )