import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from datetime import datetime

# ── Importaciones por fase ─────────────────────────────────────────────────
from fase1_catalogos   import (seed_rols, seed_sucursals, seed_categorias,
                                seed_unidadmedidas, seed_tipo_pagos,
                                seed_tipo_entregas, seed_proveedors,
                                seed_clientes, seed_kits)
from fase2_usuarios    import seed_users, seed_bodegas, seed_subcategorias
from fase3_productos   import seed_productos, seed_detalle_kits, seed_productoprovs
from fase4_operaciones import (seed_inventarios, seed_recepciones,
                                seed_facturas, seed_movimientos, seed_cotizacions)
from fase5_detalles    import (seed_detalle_invs, seed_detalle_recs,
                                seed_detalle_facs, seed_detalle_movs,
                                seed_detalle_cots)
from fase6_financiero  import (seed_devoluciones, seed_detalle_devs,
                                seed_cuentas_cobrars, seed_abono_clientes,
                                seed_cuentas_pagars, seed_abono_proveedors)

# ── Helpers de consola ─────────────────────────────────────────────────────
W = 58

def header(text: str) -> None:
    print(f"\n  [ {text} ]")
    print("  " + "-" * (W - 2))

def section(title: str) -> None:
    print()
    print("  " + "=" * (W - 2))
    print(f"  {title.upper()}")
    print("  " + "=" * (W - 2))

def run(fn, *args):
    """Ejecuta un seeder mostrando nombre y tiempo individual."""
    name = fn.__name__.replace("seed_", "").replace("_", " ").title()
    t0   = time.time()
    fn(*args)
    elapsed = time.time() - t0
    print(f"    {name:<35} {elapsed:>6.2f}s")

# ── Punto de entrada ───────────────────────────────────────────────────────
if __name__ == "__main__":
    total_start = time.time()

    print()
    print("  " + "=" * (W - 2))
    print(f"  FERRETERIA  —  DATA SEEDING COMPLETO")
    print(f"  Inicio: {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print("  " + "=" * (W - 2))

    # ── FASE 1 — Catalogos base ────────────────────────────────
    section("FASE 1  —  Catalogos base")
    run(seed_rols)
    run(seed_sucursals)
    run(seed_categorias)
    run(seed_unidadmedidas)
    run(seed_tipo_pagos)
    run(seed_tipo_entregas)
    run(seed_proveedors,  30)
    run(seed_clientes,   200)
    run(seed_kits)

    # ── FASE 2 — Usuarios, Bodegas, Subcategorias ──────────────
    section("FASE 2  —  Usuarios, Bodegas, Subcategorias")
    run(seed_bodegas)
    run(seed_subcategorias)
    run(seed_users, 1000)

    # ── FASE 3 — Productos y relaciones ───────────────────────
    section("FASE 3  —  Productos y relaciones")
    run(seed_productos,     500)
    run(seed_detalle_kits)
    run(seed_productoprovs)

    # ── FASE 4 — Operaciones principales ──────────────────────
    section("FASE 4  —  Operaciones principales")
    run(seed_inventarios)
    run(seed_recepciones,  200)
    run(seed_facturas,     300)
    run(seed_movimientos,  150)
    run(seed_cotizacions,  150)

    # ── FASE 5 — Detalles de operaciones ──────────────────────
    section("FASE 5  —  Detalles de operaciones")
    run(seed_detalle_invs)
    run(seed_detalle_recs)
    run(seed_detalle_facs)
    run(seed_detalle_movs)
    run(seed_detalle_cots)

    # ── FASE 6 — Modulo financiero ─────────────────────────────
    section("FASE 6  —  Modulo financiero")
    run(seed_devoluciones)
    run(seed_detalle_devs)
    run(seed_cuentas_cobrars)
    run(seed_abono_clientes)
    run(seed_cuentas_pagars)
    run(seed_abono_proveedors)

    # ── Resumen final ──────────────────────────────────────────
    total = time.time() - total_start
    print()
    print("  " + "=" * (W - 2))
    print(f"  SEEDING COMPLETADO")
    print(f"  Tiempo total : {total:.2f} segundos")
    print(f"  Fin          : {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print("  " + "=" * (W - 2))
    print()