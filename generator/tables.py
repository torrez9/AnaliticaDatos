from faker import Faker
import random
from datetime import datetime, timedelta, date

fake = Faker(['es_MX', 'es'])

# ── Constantes ─────────────────────────────────────────────────────────────
CATEGORIAS_POOL = [
    "Herramientas Manuales","Herramientas Eléctricas","Materiales de Construcción",
    "Plomería y Fontanería","Electricidad","Pintura y Acabados",
    "Tornillería y Fijaciones","Seguridad Industrial","Jardín y Exteriores",
    "Ferretería General",
]
SUBCATEGORIAS_POOL = [
    "Martillos y Mazas","Destornilladores","Llaves y Alicates",
    "Taladros","Pulidoras","Sierras Eléctricas",
    "Cemento y Mezclas","Bloques y Ladrillos","Arena y Grava",
    "Tuberías PVC","Llaves y Grifos","Accesorios de Tubería",
    "Cables y Conductores","Interruptores y Tomacorrientes","Luminarias",
    "Pintura de Interior","Pintura de Exterior","Selladores y Primers",
    "Tornillos y Pernos","Tuercas y Arandelas","Anclajes y Tacos",
    "Equipos de Protección","Señalización","Guantes y Calzado",
    "Herramientas de Jardín","Mangueras y Aspersores","Macetas y Sustratos",
    "Adhesivos y Sellantes","Cadenas y Candados","Accesorios Varios",
]
PRODUCTOS_POOL = [
    "Martillo Carpintero 16oz","Martillo de Bola 2lb","Destornillador Plano 6\"",
    "Destornillador Phillips #2","Llave Inglesa 12\"","Set Llaves Allen 9pz",
    "Alicate de Punta 8\"","Alicate Universal 8\"","Taladro Percutor 500W",
    "Taladro de Banco 1/2HP","Pulidora Angular 4.5\"","Sierra Circular 7.25\"",
    "Cemento Portland 42.5kg","Cal Hidratada 25kg","Arena Fina Saco 50kg",
    "Bloque de 6\" (unidad)","Tubo PVC 1/2\" x 6m","Tubo PVC 1\" x 6m",
    "Codo PVC 90° 1/2\"","Llave de Paso 1/2\"","Cable THW #12 (metro)",
    "Cable THW #10 (metro)","Interruptor Sencillo","Tomacorriente Doble",
    "Breaker 20A","Panel Eléctrico 12 Circ","Pintura Látex Blanco 1gal",
    "Pintura Látex Azul 1gal","Sellador Acrílico 1gal","Rodillo 9\" Felpa",
    "Brocha 3\"","Tornillo Drywall 1\" (100u)","Tornillo Madera 2\" (100u)",
    "Perno Galvanizado 1/4x2\"","Tuerca Hex 1/4\" (100u)","Casco Seguridad Blanco",
    "Guantes de Cuero Par","Botas Punta Acero #42","Lentes de Seguridad",
    "Manguera 1/2\" x 25m","Rastrillo 14 Dientes","Pala Cuadrada",
    "Machete 18\"","Pegamento PVC 1/4L","Silicón Transparente",
    "Candado 40mm","Bisagra 3\" Par","Clavo 2\" (lb)",
    "Varilla Corrugada 3/8\" x 6m","Varilla 1/2\" x 6m","Lámina de Zinc 8'",
    "Disco de Corte 4.5\"","Broca 3/8\"","Nivel de Burbuja 24\"",
    "Cinta Métrica 5m","Escuadra Metálica 12\"","Compresor 25L 2HP",
]
ESTADOS_FAC  = ["Pagada","Pagada","Pendiente","Anulada"]
ESTADOS_PROD = ["Activo","Activo","Activo","Inactivo"]

# ── Helpers ────────────────────────────────────────────────────────────────
def _dt(days: int = 365) -> str:
    return (datetime.now() - timedelta(days=random.randint(0, days))).strftime("%Y-%m-%d %H:%M:%S")

def _date(days: int = 365) -> str:
    return (date.today() - timedelta(days=random.randint(0, days))).strftime("%Y-%m-%d")

def _dirty_str(v):
    if v is None: return None
    return random.choice([
        v.upper(), v.lower(), v + "  ", "  " + v,
        v[:max(1, len(v)//2)], None, v,
        v.replace("a","@").replace("e","3"),
    ])

def _dirty_num(v):
    if v is None: return None
    return random.choice([v, -abs(v), 0.0, v * 100, None])

# ── Generators ─────────────────────────────────────────────────────────────
def generate_categorias(cantidad: int, orden: str, calidad: str) -> list:
    pool = (CATEGORIAS_POOL * (cantidad // len(CATEGORIAS_POOL) + 1))
    if orden == 'aleatorio': random.shuffle(pool)
    rows = []
    for i in range(cantidad):
        nombre = pool[i]
        if calidad == 'sucio': nombre = _dirty_str(nombre)
        rows.append({'Nombre_cat': nombre, 'created_at': _dt(), 'updated_at': _dt()})
    return rows

def generate_subcategorias(cantidad: int, orden: str, calidad: str) -> list:
    pool = (SUBCATEGORIAS_POOL * (cantidad // len(SUBCATEGORIAS_POOL) + 1))
    if orden == 'aleatorio': random.shuffle(pool)
    rows = []
    for i in range(cantidad):
        nombre = pool[i]
        id_cat = (i % 10) + 1 if orden == 'secuencial' else random.randint(1, 10)
        if calidad == 'sucio':
            nombre = _dirty_str(nombre)
            id_cat = random.choice([id_cat, None, 999])
        rows.append({'Idcategoria': id_cat, 'Nombre_subcat': nombre,
                     'created_at': _dt(), 'updated_at': _dt()})
    return rows

def generate_clientes(cantidad: int, orden: str, calidad: str) -> list:
    rows = []
    used_emails = set()
    for i in range(cantidad):
        nombre   = fake.first_name()
        apellido = fake.last_name()
        if orden == 'secuencial':
            email  = f"cliente{i+1:04d}@ferreteria.com"
            cedula = f"{i+1:03d}-{i+1:06d}-{i+1:04d}X"
        else:
            while True:
                email = fake.email()
                if email not in used_emails: used_emails.add(email); break
            cedula = fake.bothify("###-######-####X")
        limite = round(random.uniform(1000, 50000), 2)
        saldo  = round(random.uniform(0, limite), 2)
        if calidad == 'sucio':
            nombre   = _dirty_str(nombre)
            apellido = _dirty_str(apellido)
            email    = random.choice([email, email.replace("@",""), None])
            cedula   = random.choice([cedula, "N/A", None, ""])
            limite   = _dirty_num(limite)
            saldo    = _dirty_num(saldo)
        rows.append({'Cedula': cedula, 'Nombre': nombre, 'Apellido': apellido,
                     'Telefono': fake.phone_number()[:15], 'Correo': email,
                     'Limitecredito': limite, 'Saldocredito': saldo,
                     'created_at': _dt(), 'updated_at': _dt()})
    return rows

def generate_productos(cantidad: int, orden: str, calidad: str) -> list:
    rows = []
    used_codes = set()
    pool = (PRODUCTOS_POOL * (cantidad // len(PRODUCTOS_POOL) + 1))
    if orden == 'aleatorio': random.shuffle(pool)
    for i in range(cantidad):
        while True:
            codigo = f"FERR-{i+1:05d}" if orden == 'secuencial' else fake.bothify("##-????-####").upper()
            if codigo not in used_codes: used_codes.add(codigo); break
        nombre    = pool[i] + (f" v{i//len(PRODUCTOS_POOL)+1}" if i >= len(PRODUCTOS_POOL) else "")
        costo     = round(random.uniform(5, 500), 2)
        venta     = round(costo * random.uniform(1.2, 1.8), 2)
        descuento = round(venta * random.uniform(0.05, 0.2), 2)
        mayorista = round(venta * random.uniform(0.8, 0.95), 2)
        id_sub    = (i % 30) + 1 if orden == 'secuencial' else random.randint(1, 30)
        id_med    = (i % 8)  + 1 if orden == 'secuencial' else random.randint(1, 8)
        if calidad == 'sucio':
            nombre    = _dirty_str(nombre)
            costo     = _dirty_num(costo)
            venta     = _dirty_num(venta)
            descuento = random.choice([descuento, None, -descuento])
            mayorista = random.choice([mayorista, None])
            codigo    = random.choice([codigo, codigo.lower(), None])
        rows.append({
            'Idsubcat': id_sub, 'Id_Medida': id_med, 'Codigo_barra': codigo,
            'Nombre': nombre, 'foto': None,
            'Precio_costo': costo, 'Precio_venta': venta,
            'Precio_descuento': descuento, 'Precio_Mayorista': mayorista,
            'Estado': random.choice(ESTADOS_PROD),
            'created_at': _dt(), 'updated_at': _dt(),
        })
    return rows

def generate_facturas(cantidad: int, orden: str, calidad: str) -> list:
    rows = []
    for i in range(cantidad):
        sub   = round(random.uniform(100, 20000), 2)
        desc  = round(sub * random.uniform(0, 0.15), 2)
        total = round(sub - desc, 2)
        estado    = ESTADOS_FAC[i % 4] if orden == 'secuencial' else random.choice(ESTADOS_FAC)
        idusuario = (i % 1000) + 1 if orden == 'secuencial' else random.randint(1, 1000)
        idcliente = (i % 200)  + 1 if orden == 'secuencial' else random.randint(1, 200)
        if calidad == 'sucio':
            sub   = _dirty_num(sub)
            desc  = random.choice([desc, None, -desc])
            total = random.choice([total, None, sub])
            estado = random.choice([estado, "", None, estado.lower()])
        rows.append({
            'Id_tipoentrega': (i%3)+1 if orden=='secuencial' else random.randint(1,3),
            'Id_tipopago':    (i%5)+1 if orden=='secuencial' else random.randint(1,5),
            'Idusuario': idusuario, 'Idcliente': idcliente,
            'Estado': estado, 'Fecha': _dt(),
            'Subtotal': sub, 'Descuento': desc, 'Total': total,
            'created_at': _dt(), 'updated_at': _dt(),
        })
    return rows

def generate_detalle_facs(cantidad: int, orden: str, calidad: str) -> list:
    rows = []
    for i in range(cantidad):
        precio  = round(random.uniform(10, 2000), 2)
        cant    = round(random.uniform(1, 20), 2)
        desc    = round(precio * random.uniform(0, 0.1), 2)
        importe = round(cant * (precio - desc), 2)
        idfac   = (i%300)+1 if orden=='secuencial' else random.randint(1, 300)
        idprod  = (i%500)+1 if orden=='secuencial' else random.randint(1, 500)
        idbodega= (i%10)+1  if orden=='secuencial' else random.randint(1, 10)
        if calidad == 'sucio':
            precio  = _dirty_num(precio)
            cant    = random.choice([cant, 0, -cant, None])
            desc    = random.choice([desc, None, precio * 2 if precio else None])
            importe = random.choice([importe, None, 0])
        rows.append({
            'IdFactura': idfac, 'Idproducto': idprod, 'Idbodega': idbodega,
            'Idkit': random.choice([None, None, random.randint(1,20)]),
            'Producto_Gen': None, 'Cantidad': cant,
            'Descuento': desc, 'Precio': precio, 'Importe': importe,
            'Devolucion': random.choice(["No","No","No","Si"]),
            'created_at': _dt(), 'updated_at': _dt(),
        })
    return rows

TABLE_GENERATORS = {
    'categorias':    generate_categorias,
    'subcategorias': generate_subcategorias,
    'clientes':      generate_clientes,
    'productos':     generate_productos,
    'facturas':      generate_facturas,
    'detalle_facs':  generate_detalle_facs,
}

def generate_table(table: str, cantidad: int, orden: str, calidad: str) -> list:
    return TABLE_GENERATORS[table](cantidad, orden, calidad)