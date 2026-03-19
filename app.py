from flask import Flask, render_template, request, jsonify, send_file, Response
import webbrowser, threading, io, time, json

app = Flask(__name__)

# ── Límites por operación ──────────────────────────────────────────────────
LIMITS = {
    'preview':  20,          # Filas mostradas en pantalla
    'generate': 50_000,      # Máx para mostrar en el editor del navegador
    'download': 1_000_000,   # Máx para descarga directa a archivo
}

def _clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(max_val, int(value)))

# ── Rutas ──────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    cfg      = request.get_json()
    tabla    = cfg.get('tabla',    'clientes')
    orden    = cfg.get('orden',    'aleatorio')
    calidad  = cfg.get('calidad',  'limpio')
    formato  = cfg.get('formato',  'sql')
    preview  = bool(cfg.get('preview', False))
    cantidad = _clamp(cfg.get('cantidad', 100), 1, LIMITS['generate'])

    from generator.tables    import generate_table
    from generator.exporters import export_data

    start = time.time()
    rows  = generate_table(tabla, cantidad, orden, calidad)
    full  = export_data(rows, tabla, formato)
    prev  = export_data(rows[:LIMITS['preview']], tabla, formato)
    elapsed = round(time.time() - start, 2)

    return jsonify({
        'preview': prev,
        'full':    full,
        'total':   len(rows),
        'elapsed': elapsed,
        'limit_exceeded': False,
    })

@app.route('/api/download', methods=['POST'])
def api_download():
    cfg      = request.get_json()
    tabla    = cfg.get('tabla',    'clientes')
    orden    = cfg.get('orden',    'aleatorio')
    calidad  = cfg.get('calidad',  'limpio')
    formato  = cfg.get('formato',  'sql')
    cantidad = _clamp(cfg.get('cantidad', 100), 1, LIMITS['download'])

    from generator.tables    import generate_table
    from generator.exporters import export_data, get_extension, get_mimetype

    # Para cantidades grandes (+100K) usar generación en chunks para
    # no saturar memoria RAM
    if cantidad > 100_000:
        return _download_stream(tabla, cantidad, orden, calidad, formato)

    rows     = generate_table(tabla, cantidad, orden, calidad)
    output   = export_data(rows, tabla, formato)
    ext      = get_extension(formato)
    mimetype = get_mimetype(formato)
    filename = f"seed_{tabla}_{cantidad:_}{ext}".replace('_','')

    buf = io.BytesIO(output.encode('utf-8'))
    buf.seek(0)
    return send_file(
        buf,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename,
    )

def _download_stream(tabla, cantidad, orden, calidad, formato):
    """Streaming en chunks de 10K para volúmenes >100K sin explotar RAM."""
    from generator.tables    import generate_table
    from generator.exporters import export_data, get_extension, get_mimetype

    CHUNK   = 10_000
    ext     = get_extension(formato)
    mime    = get_mimetype(formato)
    fname   = f"seed_{tabla}_{cantidad}{ext}"

    def generate():
        remaining = cantidad
        while remaining > 0:
            batch = min(CHUNK, remaining)
            rows  = generate_table(tabla, batch, orden, calidad)
            chunk = export_data(rows, tabla, formato)
            yield chunk + '\n'
            remaining -= batch

    return Response(
        generate(),
        mimetype=mime,
        headers={
            'Content-Disposition': f'attachment; filename={fname}',
            'X-Content-Type-Options': 'nosniff',
        }
    )

@app.route('/api/limits', methods=['GET'])
def api_limits():
    """El frontend consulta esto para mostrar los límites reales."""
    return jsonify(LIMITS)

@app.route('/api/info', methods=['POST'])
def api_info():
    """Estima el tamaño del archivo antes de generar."""
    cfg      = request.get_json()
    tabla    = cfg.get('tabla',   'clientes')
    cantidad = int(cfg.get('cantidad', 100))
    formato  = cfg.get('formato', 'sql')

    # Bytes promedio por fila según formato y tabla
    avg_bytes = {
        'categorias':   {'sql': 80,  'mysql': 75,  'texto': 40},
        'subcategorias':{'sql': 100, 'mysql': 95,  'texto': 50},
        'clientes':     {'sql': 220, 'mysql': 210, 'texto': 120},
        'productos':    {'sql': 300, 'mysql': 290, 'texto': 160},
        'facturas':     {'sql': 250, 'mysql': 240, 'texto': 130},
        'detalle_facs': {'sql': 220, 'mysql': 210, 'texto': 110},
    }
    bpr      = avg_bytes.get(tabla, {}).get(formato, 200)
    est_bytes= cantidad * bpr
    est_mb   = round(est_bytes / 1_048_576, 2)

    return jsonify({
        'estimated_mb':    est_mb,
        'estimated_bytes': est_bytes,
        'rows':            cantidad,
        'warning': est_mb > 50,
        'use_download': cantidad > LIMITS['generate'],
    })

# ── Inicio ─────────────────────────────────────────────────────────────────
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Timer(1.2, open_browser).start()
    print("\n" + "="*50)
    print("  Ferreteria Data Seeder")
    print("  http://127.0.0.1:5000")
    print(f"  Limite editor  : {LIMITS['generate']:,} registros")
    print(f"  Limite descarga: {LIMITS['download']:,} registros")
    print("="*50 + "\n")
    app.run(debug=False, port=5000, use_reloader=False)