from datetime import datetime

TABLE_COLUMNS = {
    'categorias':    ['Nombre_cat','created_at','updated_at'],
    'subcategorias': ['Idcategoria','Nombre_subcat','created_at','updated_at'],
    'clientes':      ['Cedula','Nombre','Apellido','Telefono','Correo',
                      'Limitecredito','Saldocredito','created_at','updated_at'],
    'productos':     ['Idsubcat','Id_Medida','Codigo_barra','Nombre','foto',
                      'Precio_costo','Precio_venta','Precio_descuento',
                      'Precio_Mayorista','Estado','created_at','updated_at'],
    'facturas':      ['Id_tipoentrega','Id_tipopago','Idusuario','Idcliente',
                      'Estado','Fecha','Subtotal','Descuento','Total',
                      'created_at','updated_at'],
    'detalle_facs':  ['IdFactura','Idproducto','Idbodega','Idkit','Producto_Gen',
                      'Cantidad','Descuento','Precio','Importe','Devolucion',
                      'created_at','updated_at'],
}

def _esc(v) -> str:
    if v is None:            return "NULL"
    if isinstance(v, bool):  return "1" if v else "0"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("\\","\\\\").replace("'","''") + "'"

def _csv(v) -> str:
    if v is None: return ""
    return str(v).replace(",",";").replace("\n"," ").replace('"',"'")

def to_sql(rows: list, table: str) -> str:
    if not rows: return "-- Sin datos generados"
    cols    = TABLE_COLUMNS[table]
    col_str = ", ".join(f"`{c}`" for c in cols)
    lines   = [
        f"-- ┌──────────────────────────────────────────────┐",
        f"-- │  Data Seeder · Tabla: {table:<22}│",
        f"-- │  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}              │",
        f"-- │  Registros: {len(rows):<35}│",
        f"-- └──────────────────────────────────────────────┘", "",
    ]
    for row in rows:
        vals = ", ".join(_esc(row.get(c)) for c in cols)
        lines.append(f"INSERT INTO `{table}` ({col_str}) VALUES ({vals});")
    return "\n".join(lines)

def to_mysql_dump(rows: list, table: str) -> str:
    if not rows: return "-- Sin datos generados"
    cols    = TABLE_COLUMNS[table]
    col_str = ", ".join(f"`{c}`" for c in cols)
    header  = [
        "-- ============================================================",
        f"-- MySQL Dump · Ferretería Data Seeder",
        f"-- Tabla: `{table}` · Registros: {len(rows)}",
        f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-- ============================================================", "",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';", "",
        f"LOCK TABLES `{table}` WRITE;", "",
        f"INSERT INTO `{table}` ({col_str}) VALUES",
    ]
    val_lines = []
    for i, row in enumerate(rows):
        vals   = ", ".join(_esc(row.get(c)) for c in cols)
        suffix = "," if i < len(rows) - 1 else ";"
        val_lines.append(f"  ({vals}){suffix}")
    footer = ["", "UNLOCK TABLES;", "SET FOREIGN_KEY_CHECKS = 1;"]
    return "\n".join(header + val_lines + footer)

def to_text(rows: list, table: str) -> str:
    if not rows: return "Sin datos"
    cols  = TABLE_COLUMNS[table]
    lines = [",".join(cols)]
    for row in rows:
        lines.append(",".join(_csv(row.get(c)) for c in cols))
    return "\n".join(lines)

def get_extension(fmt: str) -> str:
    return {'sql':'.sql','mysql':'.sql','texto':'.csv'}.get(fmt,'.txt')

def get_mimetype(fmt: str) -> str:
    return {'sql':'application/sql','mysql':'application/sql','texto':'text/csv'}.get(fmt,'text/plain')

def export_data(rows: list, table: str, formato: str) -> str:
    return {'sql': to_sql, 'mysql': to_mysql_dump, 'texto': to_text}[formato](rows, table)