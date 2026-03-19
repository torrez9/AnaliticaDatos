import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faker import Faker
from config.db import get_connection
from datetime import datetime, timedelta
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

def _rand_dt(days: int = 365) -> str:
    """Fecha/hora aleatoria dentro de los ultimos `days` dias."""
    return (
        datetime.now() - timedelta(days=random.randint(0, days))
    ).strftime("%Y-%m-%d %H:%M:%S")

# ── Seeders ────────────────────────────────────────────────────────────────
def seed_inventarios() -> None:
    # 1 inventario por cada una de las 10 bodegas
    data = [(bodega_id,) for bodega_id in range(1, 11)]

    _exec(
        "INSERT INTO inventarios (Idbodega, created_at, updated_at) "
        "VALUES (%s,NOW(),NOW())",
        data, "inventarios"
    )


def seed_recepciones(total: int = 200) -> None:
    start   = time.time()
    estados = ["Pagada", "Pendiente", "Parcial"]
    used    = set()
    data    = []

    for _ in range(total):
        # Numero de factura unico
        while True:
            num = fake.bothify("REC-######")
            if num not in used:
                used.add(num)
                break

        sub  = round(random.uniform(500, 50000), 2)
        iva  = round(sub * 0.15, 2)
        desc = round(sub * random.uniform(0, 0.10), 2)

        data.append((
            random.randint(1,   30),        # Idproveedor
            random.randint(1, 1000),        # Idusuario
            random.randint(1,    5),        # Id_tipopago
            num,                            # Num_Factura unico
            _rand_dt(),                     # Fecha
            random.choice(estados),
            sub,
            iva,
            desc,
            round(sub + iva - desc, 2),    # Total
        ))

    _exec_timed(
        """INSERT INTO recepciones
           (Idproveedor, Idusuario, Id_tipopago, Num_Factura, Fecha, Estado,
            Subtotal, IVA, Descuento, Total, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "recepciones", start
    )


def seed_facturas(total: int = 300) -> None:
    start   = time.time()
    estados = ["Pagada", "Pagada", "Pendiente", "Anulada"]
    data    = []

    for _ in range(total):
        sub  = round(random.uniform(100, 20000), 2)
        desc = round(sub * random.uniform(0, 0.15), 2)

        data.append((
            random.randint(1,    3),        # Id_tipoentrega
            random.randint(1,    5),        # Id_tipopago
            random.randint(1, 1000),        # Idusuario
            random.randint(1,  200),        # Idcliente
            random.choice(estados),
            _rand_dt(),                     # Fecha
            sub,
            desc,
            round(sub - desc, 2),           # Total
        ))

    _exec_timed(
        """INSERT INTO facturas
           (Id_tipoentrega, Id_tipopago, Idusuario, Idcliente, Estado,
            Fecha, Subtotal, Descuento, Total, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "facturas", start
    )


def seed_movimientos(total: int = 150) -> None:
    start   = time.time()
    tipos   = ["Entrada", "Salida", "Traslado", "Ajuste"]
    motivos = [
        "Compra proveedor",
        "Venta cliente",
        "Traslado entre bodegas",
        "Ajuste de inventario",
        "Devolucion",
        "Merma",
        "Inventario inicial",
    ]

    data = [
        (
            random.randint(1, 1000),
            random.choice([None, random.randint(1, 30)]),   # Idproveedor opcional
            random.choice(motivos),
            random.choice(tipos),
            round(random.uniform(50, 10000), 2),            # Total_Mov
        )
        for _ in range(total)
    ]

    _exec_timed(
        """INSERT INTO movimientos
           (Idusuario, Idproveedor, Motivo, Tipo_mov, Total_Mov,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "movimientos", start
    )


def seed_cotizacions(total: int = 150) -> None:
    start   = time.time()
    estados = ["Pendiente", "Aprobada", "Rechazada", "Vencida"]
    data    = []

    for _ in range(total):
        sub  = round(random.uniform(100, 30000), 2)
        desc = round(sub * random.uniform(0, 0.20), 2)

        data.append((
            random.randint(1,  200),        # Idcliente
            random.randint(1, 1000),        # Idusuario
            random.choice(estados),
            _rand_dt(),                     # Fecha
            sub,
            desc,
            round(sub - desc, 2),           # Total
        ))

    _exec_timed(
        """INSERT INTO cotizacions
           (Idcliente, Idusuario, Estado, Fecha,
            subtotal, Descuento, Total, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "cotizacions", start
    )


# ── Ejecucion independiente ────────────────────────────────────────────────
if __name__ == "__main__":
    import time as _t
    t0 = _t.time()
    print()
    print("  " + "=" * 50)
    print("  FASE 4  —  Operaciones principales")
    print("  " + "=" * 50)

    seed_inventarios()
    seed_recepciones(200)
    seed_facturas(300)
    seed_movimientos(150)
    seed_cotizacions(150)

    print("  " + "-" * 50)
    print(f"  Completado en {_t.time() - t0:.2f}s")
    print("  " + "=" * 50)
    print()