import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faker import Faker
from config.db import get_connection
from datetime import date, timedelta
import random, time

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

def _rand_date(days: int = 365) -> date:
    """Fecha aleatoria dentro de los ultimos `days` dias."""
    return date.today() - timedelta(days=random.randint(0, days))

# ── Seeders ────────────────────────────────────────────────────────────────
def seed_devoluciones() -> None:
    """
    50 devoluciones ligadas a facturas existentes (IDs 1-300).
    Motivos acotados a causas reales de ferreteria.
    """
    motivos = [
        "Producto danado",
        "Error de cobro",
        "Producto incorrecto",
        "Cliente no satisfecho",
        "Vencimiento proximo",
    ]
    data = [
        (
            random.randint(1,  300),        # IdFactura
            random.randint(1, 1000),        # Idusuario
            _rand_date(),                   # Fecha_dev
            round(random.uniform(50, 5000), 2),
            random.choice(motivos),
        )
        for _ in range(50)
    ]
    _exec(
        """INSERT INTO devoluciones
           (IdFactura, Idusuario, Fecha_dev, Total_devuelto, Motivo,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "devoluciones"
    )


def seed_detalle_devs() -> None:
    """
    Entre 1 y 3 lineas por cada una de las 50 devoluciones.
    Id_detallefac referencia lineas de detalle_facs existentes.
    """
    data = []
    for dev_id in range(1, 51):             # 50 devoluciones
        n = random.randint(1, 3)
        for _ in range(n):
            precio   = round(random.uniform(10, 500), 2)
            cant_dev = round(random.uniform(1,    5), 2)
            data.append((
                dev_id,
                random.randint(1, 1500),    # Id_detallefac
                cant_dev,
                precio,
                round(cant_dev * precio, 2),  # Subtotal_dev
            ))

    _exec(
        """INSERT INTO detalle_devs
           (Id_devolucion, Id_detallefac, Cantidad_dev, Precio, Subtotal_dev,
            created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "detalle_devs"
    )


def seed_cuentas_cobrars() -> None:
    """
    120 facturas seleccionadas al azar generan cuentas por cobrar.
    Fecha de vencimiento = emision + 15 a 90 dias.
    Saldo pendiente es un porcentaje aleatorio del total.
    """
    estados = ["Pendiente", "Parcial", "Pagada", "Vencida"]
    data    = []

    for fac_id in random.sample(range(1, 301), 120):
        emision     = _rand_date(180)
        vencimiento = emision + timedelta(days=random.randint(15, 90))
        total       = round(random.uniform(500, 20000), 2)
        saldo       = round(total * random.uniform(0, 1),  2)
        data.append((
            fac_id,
            random.randint(1, 200),         # Idcliente
            random.choice(estados),
            emision,
            vencimiento,
            saldo,
            total,
        ))

    _exec(
        """INSERT INTO cuentas_cobrars
           (IdFactura, Idcliente, Estado, Fecha_emision, Fecha_vencimiento,
            Saldo_pendiente, Total, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "cuentas_cobrars"
    )


def seed_abono_clientes() -> None:
    """
    Entre 1 y 4 abonos por cada una de las 120 cuentas por cobrar.
    Num_abono indica el numero de cuota dentro de la misma cuenta.
    """
    data = []

    for cta_id in range(1, 121):            # 120 cuentas por cobrar
        n_abonos = random.randint(1, 4)
        for num in range(1, n_abonos + 1):
            data.append((
                cta_id,
                random.randint(1, 1000),    # Idusuario
                random.randint(1, 5),       # Id_tipopago
                fake.bothify("REF-######"), # Referencia
                num,                        # Num_abono (cuota)
                _rand_date(150),            # Fecha
                round(random.uniform(100, 5000), 2),
            ))

    _exec(
        """INSERT INTO abono_clientes
           (Id_cuentacobrar, Idusuario, Id_tipopago, Referencia,
            Num_abono, Fecha, Monto_abono, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "abono_clientes"
    )


def seed_cuentas_pagars() -> None:
    """
    80 recepciones seleccionadas al azar generan cuentas por pagar.
    Fecha de vencimiento = emision + 30 a 120 dias (plazos mas largos que cobranza).
    """
    estados = ["Pendiente", "Parcial", "Pagada", "Vencida"]
    data    = []

    for rec_id in random.sample(range(1, 201), 80):
        emision     = _rand_date(180)
        vencimiento = emision + timedelta(days=random.randint(30, 120))
        total       = round(random.uniform(1000, 50000), 2)
        saldo       = round(total * random.uniform(0,  1),  2)
        data.append((
            rec_id,
            random.randint(1, 30),          # Idproveedor
            random.choice(estados),
            emision,
            vencimiento,
            saldo,
            total,
        ))

    _exec(
        """INSERT INTO cuentas_pagars
           (Idrecepcion, Idproveedor, Estado, Fecha_emision, Fecha_vencimiento,
            Saldo_pendiente, Total, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "cuentas_pagars"
    )


def seed_abono_proveedors() -> None:
    """
    Entre 1 y 3 abonos por cada una de las 80 cuentas por pagar.
    Idusuario es opcional — puede ser NULL si el pago es automatico.
    """
    data = []

    for cta_id in range(1, 81):             # 80 cuentas por pagar
        n_abonos = random.randint(1, 3)
        for num in range(1, n_abonos + 1):
            data.append((
                cta_id,
                random.randint(1, 5),                               # Id_tipopago
                random.choice([None, random.randint(1, 1000)]),     # Idusuario opcional
                fake.bothify("PROV-REF-######"),                    # Referencia
                num,                                                 # Num_abono
                _rand_date(150),                                    # Fecha
                round(random.uniform(500, 10000), 2),
            ))

    _exec(
        """INSERT INTO abono_proveedors
           (Id_cuentapagar, Id_tipopago, Idusuario, Referencia,
            Num_abono, Fecha, Monto_abono, created_at, updated_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
        data, "abono_proveedors"
    )


# ── Ejecucion independiente ────────────────────────────────────────────────
if __name__ == "__main__":
    t0 = time.time()
    print()
    print("  " + "=" * 50)
    print("  FASE 6  —  Modulo financiero")
    print("  " + "=" * 50)

    seed_devoluciones()
    seed_detalle_devs()
    seed_cuentas_cobrars()
    seed_abono_clientes()
    seed_cuentas_pagars()
    seed_abono_proveedors()

    print("  " + "-" * 50)
    print(f"  Completado en {time.time() - t0:.2f}s")
    print("  " + "=" * 50)
    print()