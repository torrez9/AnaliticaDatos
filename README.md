# Ferreteria Data Seeder

Herramienta web con Flask para generar datos de prueba en MySQL.
Soporta 6 fases de seeding, formatos SQL / MySQL Dump / CSV y hasta 1,000,000 registros.

---

## Requisitos

- Python 3.10+
- MySQL 8.x

---

## Instalacion

    git clone https://github.com/torrez9/AnaliticaDatos.git
    cd AnaliticaDatos
    python -m venv venv
    venv\Scripts\activate        # Windows
    source venv/bin/activate     # Linux / Mac
    pip install -r requirements.txt
    cp .env.example .env         # editar con tus credenciales

Crear la base de datos:

    CREATE DATABASE ferreteria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

---

## Uso

    # Interfaz web
    python app.py                          # abre http://127.0.0.1:5000

    # Todas las fases por consola
    python seeders/run_all.py

    # Fase individual
    python seeders/fase1_catalogos.py

---

## Estructura

    app.py
    config/db.py
    generator/tables.py
    generator/exporters.py
    seeders/fase1_catalogos.py     Roles, sucursales, categorias, clientes, kits
    seeders/fase2_usuarios.py      Bodegas, subcategorias, usuarios (bcrypt)
    seeders/fase3_productos.py     Productos, kits, proveedores
    seeders/fase4_operaciones.py   Inventarios, recepciones, facturas, movimientos
    seeders/fase5_detalles.py      Detalles de todas las operaciones
    seeders/fase6_financiero.py    Devoluciones, cuentas por cobrar y pagar
    seeders/run_all.py
    templates/index.html

---

## Fases y Volumenes

    Fase 1   Catalogos base         ~270 registros
    Fase 2   Usuarios y bodegas     1,040 registros
    Fase 3   Productos              ~600 registros
    Fase 4   Operaciones            810 registros
    Fase 5   Detalles               ~2,500 registros
    Fase 6   Financiero             ~700 registros

Ejecutar siempre en orden — cada fase depende de los IDs de la anterior.

---

## Notas

- Contrasena de usuarios generados : Password123!
- Codigos de barra                 : unicos por sesion
- Idbodega_destino en movimientos  : puede ser NULL
- Idusuario en abono_proveedors    : puede ser NULL

---

## Limites Web

    Vista previa     20 filas
    Editor           50,000 registros
    Descarga         1,000,000 registros

---

## Licencia

MIT License — Copyright (c) 2026 Darwin Torrez