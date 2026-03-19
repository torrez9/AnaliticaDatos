import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.db import get_connection
import random, time

# ── Helpers ────────────────────────────────────────────────────────────────
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
def seed_detalle_invs() -> None:
    """
    Genera entre 30 y 60 productos por cada uno de los 10 inventarios.
    Evita duplicados (inv_id, prod_id) con un set de control.
    """
    start = time.time()
    data  = []
    used  = set()

    for inv_id in range(1, 11):                             # 10 inventarios
        n = random.randint(30, 60)
        for prod_id in random.sample(range(1, 501), n):
            if (inv_id, prod_id) not in used:
                used.add((inv_id, prod_id))
                data.append((
                    inv_id,
                    prod_id,
                    round(random.uniform(0, 500), 2),       # Cantidad
                    random.randint(5, 20),                  # Min_stock
                ))

    _exec_timed(
        """INSERT INTO detalle_invs
           (Id_inventario, Idproducto, Cantidad, Min_stock,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,NOW(),NOW())""",
        data, "detalle_invs", start
    )


def seed_detalle_recs() -> None:
    """
    Genera entre 2 y 6 productos por cada una de las 200 recepciones.
    Idbodega es opcional (puede ser NULL).
    """
    start = time.time()
    data  = []

    for rec_id in range(1, 201):                            # 200 recepciones
        n = random.randint(2, 6)
        for prod_id in random.sample(range(1, 501), n):
            costo = round(random.uniform(5, 500), 2)
            cant  = round(random.uniform(1,  50), 2)
            data.append((
                rec_id,
                prod_id,
                random.choice([None, random.randint(1, 10)]),  # Idbodega opcional
                random.randint(1, 5),                           # Id_tipopago
                cant,
                costo,
                round(cant * costo, 2),                        # Importe
            ))

    _exec_timed(
        """INSERT INTO detalle_recs
           (Idrecepcion, Idproducto, Idbodega, Id_tipopago,
            Cantidad, Precio_costo, Importe, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "detalle_recs", start
    )


def seed_detalle_facs() -> None:
    """
    Genera entre 1 y 5 lineas por cada una de las 300 facturas.
    Idkit y Producto_Gen son NULL por defecto.
    Devolucion inicia siempre en 'No'.
    """
    start = time.time()
    data  = []

    for fac_id in range(1, 301):                            # 300 facturas
        n = random.randint(1, 5)
        for prod_id in random.sample(range(1, 501), n):
            precio = round(random.uniform(10, 2000), 2)
            cant   = round(random.uniform(1,   20), 2)
            desc   = round(precio * random.uniform(0, 0.10), 2)
            data.append((
                fac_id,
                prod_id,
                random.randint(1, 10),                      # Idbodega
                None,                                       # Idkit
                None,                                       # Producto_Gen
                cant,
                desc,
                precio,
                round(cant * (precio - desc), 2),           # Importe
                "No",                                       # Devolucion
            ))

    _exec_timed(
        """INSERT INTO detalle_facs
           (IdFactura, Idproducto, Idbodega, Idkit, Producto_Gen,
            Cantidad, Descuento, Precio, Importe, Devolucion,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "detalle_facs", start
    )


def seed_detalle_movs() -> None:
    """
    Genera entre 2 y 5 productos por cada uno de los 150 movimientos.
    Idbodega_destino es NULL en movimientos que no son traslados.
    """
    start = time.time()
    data  = []

    for mov_id in range(1, 151):                            # 150 movimientos
        n = random.randint(2, 5)
        for prod_id in random.sample(range(1, 501), n):
            cant    = round(random.uniform(1,  50), 2)
            importe = round(cant * random.uniform(10, 500), 2)
            origen  = random.randint(1, 10)
            destino = random.choice([None, random.randint(1, 10)])  # NULL si no es traslado
            data.append((
                mov_id,
                prod_id,
                origen,
                destino,
                cant,
                importe,
            ))

    _exec_timed(
        """INSERT INTO detalle_movs
           (Id_movimiento, Idproducto, Idbodega_origen, Idbodega_destino,
            Cantidad, Importe_mov, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "detalle_movs", start
    )


def seed_detalle_cots() -> None:
    """
    Genera entre 1 y 5 productos por cada una de las 150 cotizaciones.
    Tipo_precio puede ser Normal, Mayorista o Descuento.
    Idkit es NULL — las cotizaciones aplican a productos individuales.
    """
    start        = time.time()
    tipos_precio = ["Normal", "Mayorista", "Descuento"]
    data         = []

    for cot_id in range(1, 151):                            # 150 cotizaciones
        n = random.randint(1, 5)
        for prod_id in random.sample(range(1, 501), n):
            precio = round(random.uniform(10, 2000), 2)
            cant   = round(random.uniform(1,   20), 2)
            desc   = round(precio * random.uniform(0, 0.20), 2)
            data.append((
                cot_id,
                prod_id,
                None,                                       # Idkit
                cant,
                precio,
                desc,
                random.choice(tipos_precio),
                round(cant * (precio - desc), 2),           # Importe
            ))

    _exec_timed(
        """INSERT INTO detalle_cots
           (Id_Cotizacion, Idproducto, Idkit,
            Cantidad, Precio, Descuento, Tipo_precio, Importe,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "detalle_cots", start
    )


# ── Ejecucion independiente ────────────────────────────────────────────────
if __name__ == "__main__":
    t0 = time.time()
    print()
    print("  " + "=" * 50)
    print("  FASE 5  —  Detalles de operaciones")
    print("  " + "=" * 50)

    seed_detalle_invs()
    seed_detalle_recs()
    seed_detalle_facs()
    seed_detalle_movs()
    seed_detalle_cots()

    print("  " + "-" * 50)
    print(f"  Completado en {time.time() - t0:.2f}s")
    print("  " + "=" * 50)
    print()