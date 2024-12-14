from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
from cone import obtener_clientes, obtener_productos, obtener_sucursales, insertar_compra, insertar_producto, obtener_todos_productos,insertar_cliente,obtener_compras, insertar_devolucion,insertar_sucursal,obtener_ubi_clientes,obtener_ubi_sucursales, obtener_sucursales_cercanas# Importar la función para obtener el reporte
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import mysql.connector
import decimal
from datetime import datetime
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

#Ruta para obtener compras
@app.route("/obtener_compras", methods=["GET"])
def api_obtener_compras():
    try:
        sucursales = obtener_compras()  # Llamamos a la función que obtiene las compras
        return jsonify(sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Ruta para obtener clientes
@app.route("/obtener_clientes", methods=["GET"])
def api_obtener_clientes():
    try:
        clientes = obtener_clientes()  # Llamamos a la función que obtiene los clientes
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener productos
@app.route("/obtener_productos", methods=["GET"])
def api_obtener_productos():
    try:
        productos = obtener_productos()   # Llamamos a la función que obtiene los productos
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener sucursales
@app.route("/obtener_sucursales", methods=["GET"])
def api_obtener_sucursales():
    try:
        sucursales = obtener_sucursales()  # Llamamos a la función que obtiene las sucursales
        return jsonify(sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para insertar una compra
@app.route("/insertar_compra", methods=["POST"])
def api_insertar_compra():
    try:
        data = request.json
        compra_id = data["compraId"]
        cliente_id = data["clienteId"]
        producto_id = data["productoId"]
        sucursal_id = data["sucursalId"]
        
        insertar_compra(compra_id, cliente_id, producto_id, sucursal_id)
        return jsonify({"message": "Compra registrada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/insertar_producto", methods=["POST"])
def api_insertar_producto():
    try:
        data = request.json
        producto_id = data["productoId"]
        nombre = data["nombre"]
        descripcion = data["descripcion"]
        precio = data["precio"]
        stock = data["stock"]
        
        insertar_producto(producto_id, nombre, descripcion, precio, stock)
        return jsonify({"message": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/obtener_todos_productos", methods=["GET"])
def api_obtener_todos_productos():
    try:
        productos = obtener_todos_productos()  # Llamamos a la función que obtiene los clientes
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/insertar_cliente", methods=["POST"])
def api_insertar_cliente():
    try:
        data = request.json
        cliente_id = data["clienteId"]
        nombre = data["nombre"]
        correo = data["correo"]
        latitud = data["latitud"]
        longitud = data["longitud"]
        
        insertar_cliente(cliente_id, nombre, correo, latitud, longitud)
        return jsonify({"message": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/insertar_devolucion", methods=["POST"])
def api_insertar_devolucion():
    try:
        data = request.json
        devolucion_id = data["devolucionId"]
        compra_id = data["compraId"]
        sucursal_id = data["sucursalId"]
        fecha_devolucion = data["fechaDevolucion"]
        motivo = data ["motivo"]
        
        insertar_devolucion(devolucion_id, compra_id, sucursal_id, fecha_devolucion, motivo)
        return jsonify({"message": "Devolucion registrada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/insertar_sucursal", methods=["POST"])
def api_insertar_sucursal():
    try:
        data = request.json
        sucursal_id = data["sucursalId"]
        nombre = data["nombre"]
        latitud = data["latitud"]
        longitud = data["longitud"]
        
        insertar_sucursal(sucursal_id, nombre, latitud, longitud)
        return jsonify({"message": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener clientes y sucursales con sus ubicaciones
@app.route("/get_locations", methods=["GET"])
def get_locations():
    try:
        # Obtener los clientes
        clientes = obtener_ubi_clientes()  # Asegúrate de que esta función retorne una lista de clientes con latitud y longitud

        # Obtener las sucursales
        sucursales = obtener_ubi_sucursales()  # Asegúrate de que esta función retorne una lista de sucursales con latitud y longitud

        # Devuelve los clientes y sucursales como JSON
        return jsonify(clientes=clientes, sucursales=sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sucursales_cercanas", methods=["GET"])
def api_obtener_sucursales_cercanas():
    try:
        resultados = obtener_sucursales_cercanas()
        # Formatear los resultados para la respuesta JSON
        sucursales_por_cliente = {}
        for resultado in resultados:
            cliente_id = resultado['cliente_id']
            if cliente_id not in sucursales_por_cliente:
                sucursales_por_cliente[cliente_id] = {
                    'cliente_id': cliente_id,
                    'nombre_cliente': resultado['nombre_cliente'],
                    'sucursales': []
                }
            sucursales_por_cliente[cliente_id]['sucursales'].append({
                'sucursal_id': resultado['sucursal_id'],
                'nombre_sucursal': resultado['nombre_sucursal'],
                'distancia_km': float(resultado['distancia_km'])
            })
        
        return jsonify(list(sucursales_por_cliente.values())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500














    

mongo_uri = "mongodb+srv://johanlinares2312:2312@entregafinal.ucptk.mongodb.net/?ssl=true&tlsAllowInvalidCertificates=true"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["entregaFinal"]

# Configuración de MySQL
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "2312",
    "database": "entrega"
}
mysql_conn = mysql.connector.connect(**mysql_config)
cursor = mysql_conn.cursor(dictionary=True)

# Función para convertir valores de tipo decimal a float
def convert_decimal_to_float(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    elif isinstance(value, dict):
        return {k: convert_decimal_to_float(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_decimal_to_float(v) for v in value]
    return value

# Migración de datos desde MySQL a MongoDB
@app.route("/migrar", methods=["POST"])
def migrar_datos():
    try:
        # Migrar Clientes
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        mongo_db["Clientes"].insert_many(
            [{k: convert_decimal_to_float(v) for k, v in row.items()} for row in clientes]
        )

        # Migrar Productos
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        mongo_db["Productos"].insert_many(
            [{k: convert_decimal_to_float(v) for k, v in row.items()} for row in productos]
        )

        # Migrar Sucursales
        cursor.execute("SELECT * FROM Sucursales")
        sucursales = cursor.fetchall()
        mongo_db["Sucursales"].insert_many(
            [{k: convert_decimal_to_float(v) for k, v in row.items()} for row in sucursales]
        )

        # Migrar Compras con relaciones
        cursor.execute("SELECT * FROM Compras")
        compras = cursor.fetchall()
        for row in compras:
            row["Cliente"] = get_cliente(row.pop("cliente_id"))
            row["Producto"] = get_producto(row.pop("producto_id"))
            row["Sucursal"] = get_sucursal(row.pop("sucursal_id"))
            mongo_db["Compras"].insert_one({k: convert_decimal_to_float(v) for k, v in row.items()})

        return jsonify({"mensaje": "Migración completada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para obtener datos relacionados
def get_cliente(cliente_id):
    cursor.execute("SELECT * FROM Clientes WHERE cliente_id = %s", (cliente_id,))
    return cursor.fetchone()

def get_producto(producto_id):
    cursor.execute("SELECT * FROM Productos WHERE producto_id = %s", (producto_id,))
    return cursor.fetchone()

def get_sucursal(sucursal_id):
    cursor.execute("SELECT * FROM Sucursales WHERE sucursal_id = %s", (sucursal_id,))
    return cursor.fetchone()

def get_compra(compra_id):
    cursor.execute("SELECT * FROM Compras WHERE compra_id = %s", (compra_id,))
    return cursor.fetchone()





@app.route("/comentarios", methods=["POST"])
def insertar_comentario():
    try:
        data = request.json
        comentario_doc = {
            "comentarioId": str(datetime.timestamp(datetime.now())),
            "productoId": data.get("productoId"),
            "clienteId": data.get("clienteId"),
            "comentario": data.get("comentario"),
            "calificacion": data.get("calificacion"),
            "fecha": datetime.now()
        }
        mongo_db.Comentarios.insert_one(comentario_doc)
        return jsonify({"mensaje": "Comentario insertado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Insertar calificación de un producto
@app.route("/productos", methods=["POST"])
def insertar_producto_calificado():
    data = request.json
    producto_doc = mongo_db.ProductosCalificados.find_one({"productoId": data["productoId"]})

    if producto_doc:
        mongo_db.ProductosCalificados.update_one(
            {"productoId": data["productoId"]},
            {"$push": {"calificaciones": {"clienteId": data["clienteId"], "calificacion": data["calificacion"]}}}
        )
    else:
        mongo_db.ProductosCalificados.insert_one({
            "productoId": data["productoId"],
            "calificaciones": [{"clienteId": data["clienteId"], "calificacion": data["calificacion"]}]
        })
    return jsonify({"mensaje": "Producto calificado con éxito"}), 201

# Consultar comentarios de un producto
@app.route("/comentarios/<productoId>", methods=["GET"])
def consultar_comentarios(productoId):
    comentarios = list(mongo_db.Comentarios.find({"productoId": productoId}, {"_id": 0}))
    return jsonify(comentarios), 200


@app.route("/comentarios", methods=["GET"])
def obtener_comentarios():
    try:
        comentarios = list(mongo_db.Comentarios.find({}, {"_id": 0}))  # Obtener todos los comentarios sin el campo _id
        return jsonify(comentarios), 200
    except Exception as e:
        print(f"Error al obtener comentarios: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
