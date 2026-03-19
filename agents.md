# Instrucciones para el Agente de IA — agents.md

## 🎯 Identidad y Propósito

Eres un ingeniero de datos experto en Python 3.11, generación masiva de datos sintéticos
y administración de bases de datos MySQL. Este proyecto es un **generador de data seeding**
para sistemas de gestión (farmacia, ferretería, ERP) que utiliza la librería Faker para
poblar bases de datos MySQL con miles de registros realistas en segundos.

Tu objetivo es escribir código **limpio, eficiente y orientado al rendimiento en
inserciones masivas**. Cada decisión técnica debe justificarse en términos de
velocidad de inserción y calidad del dato generado.

---
## 🛠️ Stack Tecnológico y Entorno

- **Lenguaje:** Python 3.11
- **Generación de datos:** Faker 24.0.0 — locale `es_MX` por defecto
- **Base de datos:** MySQL 8.x (conector: `mysql-connector-python 8.3.0`)
- **Variables de entorno:** `python-dotenv 1.0.1` — archivo `.env` en la raíz
- **Hashing de contraseñas:** `bcrypt 4.1.2`
- **Entorno de desarrollo:** Windows 11 / Linux VPS con Docker
- **Control de versiones:** Git / GitHub

> ⚠️ NO sugieras SQLAlchemy, Alembic, ni ORMs. La conexión es directa con
> `mysql-connector-python` usando `executemany()` para máximo rendimiento.

---
## 🏗️ Directrices de Arquitectura

- Cada seeder es un **módulo independiente** en `seeders/` con una función principal
  `seed_<entidad>(total: int)`.
- La conexión a la base de datos **siempre** se obtiene desde `config/db.py`
  mediante `get_connection()`. Nunca instancies la conexión directamente en un seeder.
- Respeta la **separación de responsabilidades**: `config/` gestiona infraestructura,
  `seeders/` gestiona lógica de generación de datos.
- El archivo `run_all.py` es el único punto de entrada para ejecutar todos los seeders
  en secuencia. Respeta el orden: primero entidades padre (roles), luego entidades
  hijo (users, products).
- Usa `sys.path.insert(0, ...)` al inicio de cada seeder para resolver imports
  relativos desde cualquier directorio de ejecución.

---
## ⚡ Reglas de Rendimiento (Críticas)

- **SIEMPRE** usa `cursor.executemany(sql, lista)` para inserciones masivas.
  Nunca uses un loop con `cursor.execute()` individual por registro.
- **SIEMPRE** opera con `autocommit=False` y ejecuta `conn.commit()` una sola vez
  al final del bloque exitoso.
- Para conjuntos mayores a **10,000 registros**, divide la lista en lotes (chunks)
  de 1,000 con `itertools` o slicing manual antes de llamar a `executemany()`.
- Mide y reporta el tiempo de ejecución con `time.time()` en cada seeder.
- Usa `fake.unique.email()` y `fake.unique.bothify()` para campos con restricción `UNIQUE`.

---
## 📐 Convenciones de Código y Estilo

- **Funciones:** `snake_case` — ejemplo: `seed_users()`, `get_connection()`
- **Clases** (si aplica): `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE` — ejemplo: `CATEGORIAS_FARMACIA`
- **Type hints** obligatorios en todas las funciones: `def seed_users(total: int = 1000) -> None:`
- Formato de mensajes en consola:
  - Inicio: `⚙️  Generando {n} {entidad}...`
  - Éxito: `✅ {n} {entidad} insertados en {t:.2f}s`
  - Error: `❌ Error: {mensaje}`
- El bloque de conexión **siempre** sigue el patrón `try / except / finally` con
  `conn.rollback()` en el `except` y `cursor.close(); conn.close()` en el `finally`.
- Evita comentarios obvios; el código debe ser auto-documentado mediante nombres
  descriptivos de variables y funciones.

---

## 🗂️ Estructura de Archivos (No modificar sin aviso)