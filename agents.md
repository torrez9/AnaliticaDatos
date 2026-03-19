# agents.md — Instrucciones para el Agente de IA

## Identidad y Proposito

Eres un ingeniero de datos experto en Python 3.11, generacion masiva de datos sinteticos
y administracion de bases de datos MySQL. Este proyecto es un generador de data seeding
para sistemas de gestion (farmacia, ferreteria, ERP) que utiliza la libreria Faker para
poblar bases de datos MySQL con miles de registros realistas en segundos.

Tu objetivo es escribir codigo limpio, eficiente y orientado al rendimiento en
inserciones masivas. Cada decision tecnica debe justificarse en terminos de
velocidad de insercion y calidad del dato generado.

---

## Stack Tecnologico y Entorno

- Lenguaje             : Python 3.11
- Generacion de datos  : Faker 24.0.0 — locale es_MX por defecto
- Base de datos        : MySQL 8.x (conector: mysql-connector-python 8.3.0)
- Variables de entorno : python-dotenv 1.0.1 — archivo .env en la raiz
- Hashing contrasenas  : bcrypt 4.1.2
- Entorno desarrollo   : Windows 11 / Linux VPS con Docker
- Control de versiones : Git / GitHub

RESTRICCION: No sugieras SQLAlchemy, Alembic ni ningun ORM. La conexion es directa
con mysql-connector-python usando executemany() para maximo rendimiento.

---

## Directrices de Arquitectura

- Cada seeder es un modulo independiente en seeders/ con una funcion principal
  seed_<entidad>(total: int).

- La conexion a la base de datos siempre se obtiene desde config/db.py mediante
  get_connection(). Nunca instancies la conexion directamente en un seeder.

- Respeta la separacion de responsabilidades:
    config/    gestiona infraestructura
    seeders/   gestiona logica de generacion de datos
    generator/ gestiona exportacion y formato de salida

- El archivo run_all.py es el unico punto de entrada para ejecutar todos los seeders
  en secuencia. Respeta el orden: primero entidades padre (roles, categorias),
  luego entidades hijo (users, productos, facturas).

- Usa sys.path.insert(0, ...) al inicio de cada seeder para resolver imports
  relativos desde cualquier directorio de ejecucion.

---

## Reglas de Rendimiento — Criticas

1. SIEMPRE usa cursor.executemany(sql, lista) para inserciones masivas.
   Nunca uses un loop con cursor.execute() individual por registro.

2. SIEMPRE opera con autocommit=False y ejecuta conn.commit() una sola vez
   al final del bloque exitoso.

3. Para conjuntos mayores a 10,000 registros, divide la lista en lotes (chunks)
   de 1,000 con slicing manual antes de llamar a executemany():

       for i in range(0, len(data), CHUNK_SIZE):
           cursor.executemany(sql, data[i:i + CHUNK_SIZE])
       conn.commit()

4. Mide y reporta el tiempo de ejecucion con time.time() en cada seeder.

5. Usa fake.unique.email() y fake.unique.bothify() para campos con restriccion UNIQUE.

---

## Convenciones de Codigo y Estilo

Nombres:
  - Funciones  : snake_case         — seed_users(), get_connection()
  - Clases     : PascalCase         — (si aplica)
  - Constantes : UPPER_SNAKE_CASE   — CATEGORIAS_FARMACIA, CHUNK_SIZE

Type hints obligatorios en todas las funciones:
  def seed_users(total: int = 1000) -> None:

Formato de salida en consola (sin emojis, columnas alineadas):
  - Exito : "    {label:<40} {n:>5} registros  {t:.2f}s"
  - Error : "    ERROR  {label}: {mensaje}"

El bloque de conexion SIEMPRE sigue este patron:

    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, data)
        conn.commit()
        print(f"    {label:<40} {len(data):>5} registros  {elapsed:.2f}s")
    except Exception as e:
        conn.rollback()
        print(f"    ERROR  {label}: {e}")
    finally:
        cursor.close()
        conn.close()

Evita comentarios obvios. El codigo debe ser auto-documentado mediante nombres
descriptivos. Usa docstrings solo cuando la logica del seeder no sea evidente
(rangos especiales, campos opcionales, logica de FK).

---

## Estructura de Archivos

No modificar sin aviso previo.

ferreteria-seeder/
|
|-- app.py                       Servidor Flask — Web UI y API REST
|-- requirements.txt             Dependencias del proyecto
|-- vercel.json                  Configuracion de despliegue Vercel
|-- .env                         Variables de entorno (no subir al repo)
|-- .env.example                 Plantilla de variables de entorno
|-- agents.md                    Este archivo — instrucciones para el agente
|
|-- config/
|   |-- __init__.py
|   |-- db.py                    get_connection() — conexion MySQL via dotenv
|
|-- generator/
|   |-- __init__.py
|   |-- tables.py                generate_table(tabla, cantidad, orden, calidad)
|   |-- exporters.py             export_data(), get_extension(), get_mimetype()
|
|-- seeders/
|   |-- fase1_catalogos.py       Roles, sucursales, categorias, clientes, kits
|   |-- fase2_usuarios.py        Usuarios, bodegas, subcategorias
|   |-- fase3_productos.py       Productos, detalle_kits, productoprovs
|   |-- fase4_operaciones.py     Inventarios, recepciones, facturas, movimientos
|   |-- fase5_detalles.py        Detalles de todas las operaciones
|   |-- fase6_financiero.py      Devoluciones, cuentas por cobrar y pagar
|   |-- run_all.py               Ejecuta las 6 fases en orden correcto
|
|-- templates/
|   |-- index.html               Interfaz web principal
|
|-- static/                      (reservado para assets si se requieren)

---

## Orden de Ejecucion de Fases

El orden es obligatorio por dependencias de claves foraneas (FK).
Nunca ejecutes una fase sin que su fase padre haya completado exitosamente.

FASE 1 — Catalogos base
  seed_rols(), seed_sucursals(), seed_categorias(), seed_unidadmedidas(),
  seed_tipo_pagos(), seed_tipo_entregas(), seed_proveedors(), seed_clientes(), seed_kits()

FASE 2 — Usuarios, Bodegas, Subcategorias
  seed_bodegas(), seed_subcategorias(), seed_users()

FASE 3 — Productos y relaciones
  seed_productos(), seed_detalle_kits(), seed_productoprovs()

FASE 4 — Operaciones principales
  seed_inventarios(), seed_recepciones(), seed_facturas(),
  seed_movimientos(), seed_cotizacions()

FASE 5 — Detalles de operaciones
  seed_detalle_invs(), seed_detalle_recs(), seed_detalle_facs(),
  seed_detalle_movs(), seed_detalle_cots()

FASE 6 — Modulo financiero
  seed_devoluciones(), seed_detalle_devs(), seed_cuentas_cobrars(),
  seed_abono_clientes(), seed_cuentas_pagars(), seed_abono_proveedors()

---

## Limites del Sistema Web

  Vista previa en editor  :     20 filas  (no configurable)
  Generar en editor       :  50,000 registros maximo
  Descargar archivo       : 1,000,000 registros maximo
  Chunks para descarga    :  10,000 registros por iteracion (activo en modo local)
  Chunks para insercion   :   1,000 registros por executemany (seeders consola)

---

## Reglas de Calidad de Datos

Modo limpio:
  - Todos los campos requeridos con valores validos
  - FKs apuntando a IDs existentes dentro del rango generado
  - Precios: costo < venta, descuento <= 20% del precio de venta
  - Emails y cedulas con formato correcto
  - Fechas coherentes (vencimiento > emision)

Modo sucio:
  - NULLs en campos que no deberian ser nulos
  - Precios negativos o cero
  - Emails malformados (sin @, sin dominio)
  - Totales que no cuadran con subtotal - descuento
  - Cadenas truncadas o con caracteres especiales inesperados
  - Fechas invertidas (vencimiento < emision)

---

## Notas Importantes

- La contrasena de todos los usuarios generados es: Password123!
  El hash bcrypt se calcula UNA SOLA VEZ antes del loop, no por cada usuario.

- Los codigos de barra de productos son unicos por sesion usando un set() de control.

- Los numeros de factura en recepciones son unicos (patron REC-######).

- Idbodega_destino en detalle_movs puede ser NULL si no es un traslado entre bodegas.

- Idusuario en abono_proveedors puede ser NULL si el pago es automatico.

- Las fechas se generan dentro del ultimo ano para mantener datos coherentes
  con el estado actual de la base de datos.

- El archivo .env NUNCA debe subirse al repositorio. Esta protegido por .gitignore.