# Ferreteria Data Seeder

Herramienta web para generar datos de prueba (seed) para el sistema de
gestion de ferreteria. Permite insertar registros sinteticos en la base
de datos MySQL desde una interfaz grafica en el navegador o ejecutando
los seeders directamente desde consola.

---

## Caracteristicas

- Interfaz web con Flask para generar y previsualizar datos
- Soporte para 6 fases de seeding ordenadas por dependencias FK
- Generacion de hasta 1,000,000 registros con descarga en streaming
- Formatos de exportacion: SQL, MySQL Dump y CSV
- Datos limpios o sucios (dirty) para pruebas de validacion
- Vista previa de 20 filas antes de generar el total
- Estimacion de tamano del archivo antes de descargar
- Ejecucion independiente por fase o completa con run_all.py

---

## Requisitos

- Python 3.10 o superior
- MySQL 8.x
- pip

---

## Estructura del proyecto

ferreteria-seeder/
|
|-- app.py                      Servidor Flask — Web UI
|-- requirements.txt            Dependencias del proyecto
|-- .env                        Variables de entorno (no subir al repo)
|-- .env.example                Plantilla de variables de entorno
|
|-- config/
|   |-- db.py                   Conexion a MySQL con python-dotenv
|
|-- generator/
|   |-- tables.py               Logica de generacion por tabla
|   |-- exporters.py            Exportacion a SQL / MySQL Dump / CSV
|
|-- seeders/
|   |-- fase1_catalogos.py      Roles, sucursales, categorias, clientes, kits
|   |-- fase2_usuarios.py       Usuarios, bodegas, subcategorias
|   |-- fase3_productos.py      Productos, detalle_kits, productoprovs
|   |-- fase4_operaciones.py    Inventarios, recepciones, facturas, movimientos
|   |-- fase5_detalles.py       Detalles de todas las operaciones
|   |-- fase6_financiero.py     Devoluciones, cuentas por cobrar y pagar
|   |-- run_all.py              Ejecuta las 6 fases en orden correcto
|
|-- templates/
    |-- index.html              Interfaz web principal

---

## Instalacion

1. Clonar el repositorio

   git clone https://github.com/tu-usuario/ferreteria-seeder.git
   cd ferreteria-seeder

2. Crear entorno virtual

   python -m venv venv

3. Activar el entorno virtual

   Windows:
   venv\Scripts\activate

   Linux / Mac:
   source venv/bin/activate

4. Instalar dependencias

   pip install -r requirements.txt

5. Configurar variables de entorno

   Copiar el archivo de ejemplo y editar con tus datos:

   cp .env.example .env

   Contenido del .env:

   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ferreteria
   DB_USER=root
   DB_PASSWORD=tu_password

6. Crear la base de datos en MySQL

   CREATE DATABASE ferreteria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

---

## Uso

### Opcion 1 — Interfaz Web

Iniciar el servidor Flask:

   python app.py

Se abrira automaticamente el navegador en:

   http://127.0.0.1:5000

Desde la interfaz puedes:
- Seleccionar la tabla a poblar
- Configurar la cantidad de registros (1 hasta 1,000,000)
- Elegir orden aleatorio o secuencial
- Elegir calidad de datos: limpio o sucio
- Elegir formato de salida: SQL, MySQL Dump o CSV
- Ver una preview de 20 filas antes de generar
- Descargar el archivo directamente

### Opcion 2 — Consola, todas las fases

Ejecuta las 6 fases en el orden correcto de dependencias FK:

   python seeders/run_all.py

### Opcion 3 — Consola, fase individual

Cada fase puede ejecutarse de forma independiente:

   python seeders/fase1_catalogos.py
   python seeders/fase2_usuarios.py
   python seeders/fase3_productos.py
   python seeders/fase4_operaciones.py
   python seeders/fase5_detalles.py
   python seeders/fase6_financiero.py

---

## Fases de seeding

Las fases deben ejecutarse en orden. Cada fase depende de los IDs
generados en la fase anterior para respetar las claves foraneas.

FASE 1 — Catalogos base
   seed_rols              5 roles del sistema
   seed_sucursals         5 sucursales
   seed_categorias        10 categorias de productos
   seed_unidadmedidas     8 unidades de medida
   seed_tipo_pagos        5 tipos de pago
   seed_tipo_entregas     3 tipos de entrega
   seed_proveedors        30 proveedores generados con Faker
   seed_clientes          200 clientes con cedula y credito
   seed_kits              20 kits de productos

FASE 2 — Usuarios, Bodegas, Subcategorias
   seed_bodegas           10 bodegas (2 por sucursal)
   seed_subcategorias     30 subcategorias (3 por categoria)
   seed_users             1000 usuarios con hash bcrypt

FASE 3 — Productos y relaciones
   seed_productos         500 productos con precios y codigos unicos
   seed_detalle_kits      3 a 6 productos por kit
   seed_productoprovs     1 a 3 proveedores por producto

FASE 4 — Operaciones principales
   seed_inventarios       1 inventario por bodega (10 total)
   seed_recepciones       200 recepciones de proveedores
   seed_facturas          300 facturas de ventas
   seed_movimientos       150 movimientos de stock
   seed_cotizacions       150 cotizaciones a clientes

FASE 5 — Detalles de operaciones
   seed_detalle_invs      30 a 60 productos por inventario
   seed_detalle_recs      2 a 6 productos por recepcion
   seed_detalle_facs      1 a 5 lineas por factura
   seed_detalle_movs      2 a 5 productos por movimiento
   seed_detalle_cots      1 a 5 productos por cotizacion

FASE 6 — Modulo financiero
   seed_devoluciones      50 devoluciones de ventas
   seed_detalle_devs      1 a 3 lineas por devolucion
   seed_cuentas_cobrars   120 cuentas por cobrar
   seed_abono_clientes    1 a 4 abonos por cuenta cobrar
   seed_cuentas_pagars    80 cuentas por pagar
   seed_abono_proveedors  1 a 3 abonos por cuenta pagar

---

## Limites de generacion Web

   Vista previa          20 filas en pantalla
   Generar en editor     50,000 registros maximo
   Descargar archivo     1,000,000 registros maximo
   Streaming chunks      Activado automaticamente para +100,000 registros

---

## Dependencias principales

   faker==24.0.0                  Generacion de datos sinteticos
   mysql-connector-python==8.3.0  Conexion a MySQL
   python-dotenv==1.0.1           Lectura de variables de entorno
   bcrypt==4.1.2                  Hash seguro de contrasenas
   flask==3.0.3                   Servidor web y API REST

---

## Notas importantes

- Ejecutar siempre las fases en orden para evitar errores de FK
- La contrasena de todos los usuarios generados es: Password123!
- Los codigos de barra de productos son unicos por sesion de seeding
- Los numeros de factura en recepciones son unicos (REC-######)
- Idbodega_destino en movimientos puede ser NULL si no es traslado
- Idusuario en abono_proveedors puede ser NULL si el pago es automatico
- Las fechas se generan dentro del ultimo año para datos realistas

---

## Licencia

MIT License — libre para uso en proyectos de desarrollo y pruebas.