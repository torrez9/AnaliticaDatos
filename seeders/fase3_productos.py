import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faker import Faker
from config.db import get_connection
import time, random

fake = Faker(['es_MX', 'es'])

# ── Helpers ────────────────────────────────────────────────────────────────
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

# ── Pool de nombres ────────────────────────────────────────────────────────
NOMBRES_PRODUCTOS = [
    "Martillo de Carpintero",     "Martillo de Bola",           "Destornillador Plano",
    "Destornillador Phillips",    "Llave Inglesa",               "Llave Allen Set",
    "Alicate de Punta",           "Alicate Universal",           "Sierra Hacksaw",
    "Sierra de Mano",             "Taladro Percutor",            "Taladro de Banco",
    "Pulidora Angular 4.5",       "Pulidora Angular 7",          "Esmeril de Banco",
    "Cemento Portland",           "Cal Hidratada",               "Arena Fina",
    "Bloque de 6",                "Bloque de 8",                 "Ladrillo Cuarteron",
    "Tubo PVC 1/2",               "Tubo PVC 1",                  "Tubo PVC 2",
    "Codo PVC 90 1/2",            "Te PVC 1/2",                  "Reducidor PVC",
    "Llave de Paso 1/2",          "Llave de Chorro",             "Sifon PVC",
    "Cable THW 12",               "Cable THW 10",                "Cable THW 8",
    "Interruptor Sencillo",       "Tomacorriente Doble",         "Breaker 20A",
    "Panel Electrico 12 Circ",    "Conduit 3/4",                 "Tape Electrico",
    "Pintura Latex Blanco",       "Pintura Latex Azul",          "Pintura Anticorrosiva",
    "Sellador Acrilico",          "Rodillo 9",                   "Brocha 3",
    "Tornillo Drywall 1",         "Tornillo Madera 2",           "Perno Galvanizado 1/4",
    "Tuerca Hex 1/4",             "Arandela Plana 1/4",          "Taco Fisher 1/4",
    "Casco de Seguridad",         "Guantes de Cuero",            "Botas Punta de Acero",
    "Lentes de Seguridad",        "Tapones Auditivos",           "Chaleco Reflectivo",
    "Manguera 1/2 x 25m",         "Aspersor Jardinero",          "Rastrillo",
    "Pala Cuadrada",              "Machete",                     "Azadon",
    "Pegamento PVC",              "Silicon Transparente",        "Masilla Plastica",
    "Candado 40mm",               "Candado 60mm",                "Cerradura de Puerta",
    "Bisagra 3",                  "Bisagra 4",                   "Manija de Puerta",
    "Clavo 2",                    "Clavo 3",                     "Clavo 4",
    "Alambre de Amarre",          "Alambre Galvanizado",         "Malla Electrosoldada",
    "Varilla Corrugada 3/8",      "Varilla Corrugada 1/2",       "Perfil Metalico",
    "Lamina de Zinc 8",           "Lamina Aluzinc 10",           "Cumbrera Zinc",
    "Disco de Corte 4.5",         "Disco de Desbaste",           "Broca 3/8",
    "Broca Corona 2",             "Nivel de Burbuja 24",         "Cinta Metrica 5m",
    "Escuadra Metalica",          "Plomada",                     "Compresor 25L",
    "Pistola de Pintura",         "Llave Torque",                "Llave de Corona Set",
    "Llave de Tubo",              "Caja de Herramientas",        "Banco de Trabajo",
]

_POOL = len(NOMBRES_PRODUCTOS)

# ── Seeders ────────────────────────────────────────────────────────────────
def seed_productos(total: int = 500) -> None:
    start      = time.time()
    estados    = ["Activo", "Activo", "Activo", "Inactivo"]
    used_codes = set()
    data       = []

    for i in range(total):
        # Codigo de barra unico
        while True:
            codigo = fake.bothify("##-????-####").upper()
            if codigo not in used_codes:
                used_codes.add(codigo)
                break

        # Nombre: reutiliza el pool con sufijo numerico si supera el limite
        nombre_base = NOMBRES_PRODUCTOS[i % _POOL]
        nombre      = f"{nombre_base} v{i // _POOL + 1}" if i >= _POOL else nombre_base

        costo     = round(random.uniform(5,   500), 2)
        venta     = round(costo  * random.uniform(1.20, 1.80), 2)
        descuento = round(venta  * random.uniform(0.05, 0.15), 2)
        mayorista = round(venta  * random.uniform(0.85, 0.95), 2)

        data.append((
            random.randint(1, 30),      # Idsubcat  — 30 subcategorias
            random.randint(1,  8),      # Id_Medida —  8 unidades
            codigo,
            nombre,
            None,                       # foto
            costo,
            venta,
            descuento,
            mayorista,
            random.choice(estados),
        ))

    _exec_timed(
        """INSERT INTO productos
           (Idsubcat, Id_Medida, Codigo_barra, Nombre, foto,
            Precio_costo, Precio_venta, Precio_descuento, Precio_Mayorista,
            Estado, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "productos", start
    )


def seed_detalle_kits() -> None:
    data = []
    used = set()

    for kit_id in range(1, 21):                          # 20 kits
        n_productos = random.randint(3, 6)
        for prod_id in random.sample(range(1, 501), n_productos):
            if (kit_id, prod_id) not in used:
                used.add((kit_id, prod_id))
                data.append((
                    kit_id,
                    prod_id,
                    round(random.uniform(1, 10), 2),     # cantidad
                ))

    _exec(
        "INSERT IGNORE INTO detalle_kits "
        "(Idkit, Idproducto, Cantidad, created_at, updated_at) "
        "VALUES (%s,%s,%s,NOW(),NOW())",
        data, "detalle_kits"
    )


def seed_productoprovs() -> None:
    data = []
    used = set()

    for prod_id in range(1, 501):                        # 500 productos
        n_provs = random.randint(1, 3)
        for prov_id in random.sample(range(1, 31), n_provs):
            if (prov_id, prod_id) not in used:
                used.add((prov_id, prod_id))
                data.append((
                    prov_id,
                    prod_id,
                    round(random.uniform(5, 450), 2),    # precio proveedor
                ))

    _exec(
        "INSERT INTO productoprovs "
        "(Idproveedor, Idproducto, Precio, created_at, updated_at) "
        "VALUES (%s,%s,%s,NOW(),NOW())",
        data, "productoprovs"
    )